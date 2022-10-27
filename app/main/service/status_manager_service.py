# Définit et gère le workflow d'un shared_trip et du wtrip_list associé.
# L'intérêt du présent code est de traiter "comme dans une boîte noire"
# les différents aspects de l'évolution d'un shared_trip, tant pour simplifier
# les niveaux supérieurs que pour concentrer en un seul lieu les détails
# du workflow, afin de le modifier plus facilement en cas de besoin.
# Il aurait été plus simple de faire tenir ce code dans le modèle de Shared_trip
# si on avait été sûr qu'à un conducteur correspondrait toujours un seul wtrip_list
# (car alors shared_trip et wtrip_list auraient été regroupés dans un seul objet).
# Mais on peut à l'avenir avoir à gérer plusieurs passagers pour un même conducteur,
# et certaines parties du code ont été écrites en ce sens (notamment les deux
# modèles d'objet, l'algorithme path_matching,...).
# Cea nous oblige donc de gérer le workflow séparément de la définition des modèles.
#
# Ne vaut donc à ce stade que pour le cas où 1 conducteur = 1 passager
# (l'objet sht_wtl serait une liste et non un objet simple dans l'optique
# 1 conducteur = plusieurs passagers).
# Olivier - février 2021
#

import logging
from datetime import datetime
from main import db
from main.model.wtrip_list import Wtrip_list
from main.model.shared_trip import Shared_trip
from main.service.message_service import warn_users
from main.service.history_service import insert_new_history

log = logging.getLogger(__name__)
YACKA_USER_ID = 1


def initial_sht_wtl_status(initial_trip_type) :
    """ Retourne les éléments de statut initial d'un shared_trip/wtrip_list """
    return {
        "shared_trip_status" : "pending",
        "driver_status" : "proposed" if initial_trip_type == "driver"
        else "not informed yet",
        "passenger_status" : "not informed yet" if initial_trip_type == "driver"
        else "proposed"
    }


def unavailable_status_list() :
    """ Retourne les statuts d'un shared_trip qui rendent les trip/waiting_trip associés indisponibles """
    return ["both-accepted", "when-modified"]
    # return ["both-accepted", "when-modified", "terminated", "canceled", "declined"]


def user_visible_shared_trip_status_exception_list() :
    """ Retourne les shared_trip_status pour lesquels ne pas afficher le shared_trip d'un utilisateur """
    return ["terminated"]


def user_visible_driver_status_exception_list() :
    """ Retourne les driver_status pour lesquels ne pas afficher le shared_trip d'un utilisateur """
    return ["not informed yet", "unwilling", "has canceled"]


def user_visible_passenger_status_exception_list() :
    """ Retourne les passenger_status pour lesquels ne pas afficher le shared_trip d'un utilisateur """
    return ["not informed yet", "unwilling", "has canceled"]


def bydate_displayable_shared_trip_status_list() :
    """ Retourne les shared_trip_status pour lesquels on affichera les occurrences du shared_trip """
    return ["both-accepted", "when-modified"]


def phone_displayable_driver_status_list() :
    """ Retourne les shared_trip_status pour lesquels on affichera les occurrences du shared_trip """
    return ["waiting for passenger"]


def phone_displayable_passenger_status_list() :
    """ Retourne les shared_trip_status pour lesquels on affichera les occurrences du shared_trip """
    return ["waiting for driver"]


def terminated_candidate_status_list() :
    """ Retourne les shared_trip_status précédant le statut "terminated" """
    return ["both-accepted", "when-modified"]


def not_alive_status_list() :
    """ Retourne les shared_trip_status pour lesquels ne pas alerter un utilisateur avant modification """
    return ["terminated", "canceled", "declined"]


def rank_status(status) :
    """ Retourne un rang de priorité d'affichage du statut driver (ou passenger) d'un shared_trip """
    return {
        "proposed" : 0,
        "notified of refusal" : 1,
        "notified of cancellation" : 1,
        "notified of request" : 2,
        "waiting for passenger" : 3,
        "waiting for driver" : 3
    }.get(status, 10)


class Sht_wtl_whole :
    """ Intègre un ensemble shared_trip/wtrip_list en un seul objet pour gérer son workflow. """
    #
    # L'objet contient le shared_trip et le wtrip_list dont il est issu, ainsi que
    # des attributs facilitant la gestion de l'état du couple qu'ils forment :
    # - les 3 indicateurs sht_status, drv_status et pass_status, qui permettent à tout
    #   instant de savoir le positionnement du conducteur et du passager par rapport
    #   au trajet partagé. Ce sont leurs valeurs, et la manière dont on les fait
    # évoluer, qui matérialise le workflow.
    # - un indicateur is_ok, qui permet de vérifier que la méthode appliquée
    # sur l'objet s'est correctement déroulée.
    #

    def __init__(self, sht, wtl) :
        self.sht = sht
        self.wtl = wtl
        # On extrait les informations de statut à partir d'un couple shared_trip/wtrip_list
        sht_status = sht.shared_trip_status
        drv_status = sht.driver_status
        pass_status = wtl.passenger_status
        # Vérification de la validité et la cohérence des paramètres
        self.sht_status, self.drv_status, self.pass_status = None, None, None
        if sht_status == "pending"\
            and ((drv_status == "proposed" and pass_status == "not informed yet")
                 or (drv_status == "not informed yet" and pass_status == "proposed")) :
            self.sht_status = "pending"
        if sht_status == "half-accepted"\
            and ((drv_status == "waiting for passenger" and pass_status == "notified of request")
                 or (drv_status == "notified of request" and pass_status == "waiting for driver")) :
            self.sht_status = "half-accepted"
        if sht_status == "both-accepted" and drv_status == "to drive"\
                and pass_status == "to be driven" :
            self.sht_status = "both-accepted"
        if sht_status == "declined"\
            and ((drv_status == "unwilling" and pass_status == "notified of refusal")
                 or (drv_status == "notified of refusal" and pass_status == "unwilling")) :
            self.sht_status = "declined"
        if sht_status == "canceled"\
            and ((drv_status == "has canceled" and pass_status == "notified of cancellation")
                 or (drv_status == "notified of cancellation" and pass_status == "has canceled")) :
            self.sht_status = "canceled"
        if sht_status == "when-modified"\
            and ((drv_status == "has modified" and pass_status == "notified of modification")
                 or (drv_status == "notified of modification" and pass_status == "has modified")) :
            self.sht_status = "when-modified"
        if sht_status == "terminated" and drv_status == "drove"\
                and pass_status == "was driven" :
            self.sht_status = "terminated"
        if self.sht_status is not None :
            self.drv_status = drv_status
            self.pass_status = pass_status
            self.is_ok = True
        else :
            self.is_ok = False

    def __repr__(self) :
        return "<Sht_wtl_whole object " + repr(self.sht_status) + " ; " + repr(self.drv_status) + " ; " + repr(self.pass_status) + " ; " + repr(self.is_ok) + ">"

    def archive_no_commit(self) :
        """ Effectue une sauvegarde horodatée de l'état d'un shared_trip. """
        # Rassemble les données à sauvegarder et appelle insert_new_history
        data_to_save = {
            "driver_id" : self.sht.trip.driver_id,
            "passenger_id" : self.wtl.waiting_trip.passenger_id,
            "path" : self.sht.path_json,
            "occ_details" : self.sht.occ_details_pickle,
            "shared_trip_status" : self.sht_status,
            "driver_status" : self.drv_status,
            "passenger_status" : self.pass_status,
            "when" : self.wtl.pickled_when,
            "shared_distance" : self.wtl.shared_distance,
            "yacka_points_amount" : self.wtl.yacka_points_amount,
            "status_set_date" : datetime.now(),
            "shared_trip_id" : self.sht.id,
            "wtrip_list_id" : self.wtl.id
        }
        return insert_new_history(data_to_save)

    def next_state(self, action, user_id, occurrence_list = None, no_warn = False) :
        """ Fait progresser un shared_trip dans son workflow à partir d'une action. """
        #
        # occurrence_list est une liste d'occurrences à substituer dans le pickled_when
        # du wtrip_list associé au shared_trip (si ACCEPT ou WHEN-MODIFY), dont les
        # datetimes sont au format iso 8601
        #
        # Cette méthode effectue aussi une sauvegarde horodatée de l'état du shared_trip
        # pour en conserver l'historique des modifications.
        #
        # Retourne None en cas de suppression du shared_trip, ou l'objet lui-même sinon.
        #
        # On suppose dans cette méthode que l'action en paramètre est effectuée par le bon acteur
        # (passager ou conducteur) et que la vérification est faite au préalable.
        # On pourrait renforcer ce contrôle le cas échéant, en comparant la valeur de actor
        # ci-dessous par rapport au statut actuel du shared_trip, au regard des possibilités
        # permises par le schéma shared_trip_workflow.png
        #
        # print("In next_state, action/user_id/occurrence_list : {} / {} / {}".format(action, user_id, occurrence_list))
        # print("In next_state, self : {}".format(self))

        # On détermine si le user en paramètre est conducteur ou passager du share_trip
        if user_id == YACKA_USER_ID :
            actor = "system"
        else :
            actor = "driver" if self.sht.trip.driver_id == user_id else "passenger"
        # On parcourt les différentes possibilités du workflow
        self.is_ok = False
        warning_dict = {"user_id_list_list" : [], "message_id_list" : [],
                        "additional_info_list": [], "alert_level": []}
        if (self.sht_status == "both-accepted" or self.sht_status == "when-modified")\
                and action == "TERMINATE" and actor == "system" :
            drv_status = "drove"
            pass_status = "was driven"
            sht_status = "terminated"
            self.is_ok = True

        if self.is_ok :
            # On met à jour l'objet dans la BDD
            self.sht.shared_trip_status = self.sht_status = sht_status
            self.sht.modification_date = datetime.now()
            self.sht.driver_status = self.drv_status = drv_status
            self.wtl.passenger_status = self.pass_status = pass_status
            # On conserve dans l'historique une trace de la présente avancée du
            # shared_trip dans son workflow
            self.archive_no_commit()
            # On commet les modifications
            db.session.commit()
            if len(warning_dict["user_id_list_list"]) != 0 :
                # Si la liste des listes d'utilisateurs à prévenir n'est pas vide, on les
                # prévient
                try :
                    warn_users(
                        user_id,
                        warning_dict["user_id_list_list"],
                        warning_dict["message_id_list"],
                        warning_dict["additional_info_list"],
                        warning_dict["alert_level"],
                        yacka_messages_only = no_warn
                    )
                except Exception as e:
                    log.exception(e, exc_info=True)
        return self


def terminate_obsolete_shared_trips() :
    """ Fait avancer au statut "terminated" les shared_trips dont toutes les occurrences sont passées """

    # On recherche tous les shared_trips susceptibles de passer au statut "terminated"
    shared_trips_wtrip_lists = db.session.query(Shared_trip, Wtrip_list).\
        join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id).\
        filter(Shared_trip.shared_trip_status.in_(terminated_candidate_status_list())).all()
    # On n'inclut dans une liste que ceux dont les occurrences sont toutes passées
    if len(shared_trips_wtrip_lists) == 0 :
        return None
    obsolete_sht_wtl_list = []
    now = datetime.now()
    for sht, wtl in shared_trips_wtrip_lists :
        when = wtl.pickled_when
        if when.is_recurring :
            occ_list = [dt for dt in when.rruleset if dt >= now]
            if occ_list == []:
                obsolete_sht_wtl_list.append([sht, wtl])
        else :
            # if startdate_dt <= when.dtstart <= enddate_dt :
            if when.dtstart < now :
                obsolete_sht_wtl_list.append([sht, wtl])
    # On applique l'action TERMINATE à tous les shared_trips de obsolete_sht_wtl_list
    for sht, wtl in obsolete_sht_wtl_list :
        sht_wtl_whole = Sht_wtl_whole(sht, wtl)
        sht_wtl_whole.next_state(
            action = "TERMINATE",
            user_id = YACKA_USER_ID
        )
    # On retourne le nombre de shared_trips ainsi modifiés
    return len(obsolete_sht_wtl_list)


def terminate_a_shared_trip(sh_id) :
    """
    Fait avancer au statut "terminated" un shared_trip si son statut le permet,
    quelles que soient les dates de ses occurrences (à des fins de test)
    """

    # On vérifie que le shared_trips est susceptible de passer au statut "terminated"
    shared_trip_wtrip_list = db.session.query(Shared_trip, Wtrip_list).\
        join(Wtrip_list, Shared_trip.id == Wtrip_list.shared_trip_id).\
        filter(Shared_trip.id == sh_id).first()
    if len(shared_trip_wtrip_list) == 0 :
        return None
    if shared_trip_wtrip_list[0].shared_trip_status not in terminated_candidate_status_list() :
        return None
    # On applique l'action TERMINATE au shared_trip
    sht_wtl_whole = Sht_wtl_whole(shared_trip_wtrip_list[0], shared_trip_wtrip_list[1])
    sht_wtl_whole.next_state(
        action = "TERMINATE",
        user_id = YACKA_USER_ID
    )
    return True
