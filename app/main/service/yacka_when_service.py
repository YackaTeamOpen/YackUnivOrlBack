# Définition du conteneur des contraintes de temps des usagers pour les trajets Yacka
# Olivier - V0 - décenmbre 2020

from datetime import datetime, date, timedelta
from dateutil.rrule import *
from dateutil.parser import *
#from dateutil.tz import *
import re


class Yacka_when :
    """ Définition du conteneur servant à représenter l'information temporelle associée à un trip (pour un conducteur)

    ou une trip_request (pour un passager), et des méthodes permettant de les stocker, de les retrouver, de les comparer.
    """

    def __init__(self, title = None, dtstart = None, dtend = None, duration = None, allday = False, is_recurring = False, rrule_str = None) :
        """ title : string, dtstart, dtend : datetimes, allday, is_recurring : booléens, rruleset_str : rrule string au format  RFC5545 """

        self.title = title
        # breakpoint()
        #now_dt = datetime.now(tzlocal())
        if dtstart is None :
            #self.dtstart = now_dt
            self.dtstart = datetime.now()
        else :
            #self.dtstart = dtstart.replace(tzinfo = tzlocal())
            self.dtstart = dtstart
        if is_recurring and (rrule_str is not None) :
            self.is_recurring = True
            # si pas indiquée, duration est fixée à 1 heure. Dans le cas d'une récurrence,
            # duration est prioritaire par rapport à dtend (duration sert à fixer dtend).
            # duration est également prioritaire sur la clause UNTIL pour définir l'heure
            # de dtend.
            if duration is None :
                self.duration = 3600
            else :
                self.duration = duration
            # On est dans le cas d'une récurrence, on crée un objet rruleset, qu'on initialise en
            # s'assurant qu'il a une limite et un dtstart
            self.rruleset = rruleset()
            dtstart_match = re.search("(DTSTART:)", rrule_str)
            until_match = re.search(";(UNTIL)=(\d{8}T\d{6})", rrule_str)
            count_match = re.search(";(COUNT)=(\d+)", rrule_str)
            if until_match :
                # On initialise le rruleset du yacka_when, éventuellement complété
                # du dtstart manquant
                if dtstart_match is None :
                    self.rruleset.rrule(rrulestr(rrule_str, dtstart = self.dtstart))
                else :
                    self.rruleset.rrule(rrulestr(rrule_str))
                # Détermination de l'heure de fin
                if self.rruleset.count() > 1 :
                    end_time = self.rruleset[0] + timedelta(seconds = self.duration)
                    # S'il y a une clause UNTIL, on s'en sert en priorité pour déterminer
                    # le dtend par défaut, mais on corrige la partie horaire
                    #self.dtend = parse(until_match.group(2) + now_dt.tzname())
                    self.dtend = parse(until_match.group(2)).replace(
                        hour = end_time.hour,
                        minute = end_time.minute,
                        second = end_time.second
                    )
                elif self.rruleset.count() == 1 :
                    # On retransforme l'objet en un objet de type ponctuel, avec comme base
                    # le contenu de la rrule
                    self.dtstart = self.rruleset[0]
                    self.dtend = self.dtstart + timedelta(seconds = self.duration)
                    self.is_recurring = False
                    self.rruleset = None
                else :
                    # La clause UNTIL ne permet pas la création d'au moins une instance
                    # de la règle de récurrence. On retransforme l'objet en un objet
                    # de type ponctuel, à partir de dtstart.
                    self.is_recurring = False
                    self.rruleset = None
                    if dtend is None :
                        self.dtend = self.dtstart + timedelta(seconds = self.duration)
                    else :
                        # dans un contexte de non récurrence, à partir du moment où dtend est définie,
                        # on la considère comme prioritaire et on en déduit duration
                        #self.dtend = dtend.replace(tzinfo = tzlocal())
                        self.dtend = dtend
                        self.duration = (self.dtend - self.dtstart).total_seconds()

            elif count_match :
                # On initialise le rruleset du yacka_when, éventuellement complétée du dtstart manquant
                if dtstart_match is None :
                    self.rruleset.rrule(rrulestr(rrule_str, dtstart = self.dtstart))
                else :
                    self.rruleset.rrule(rrulestr(rrule_str))
                # S'il n'y a qu'une clause COUNT, on donne par défaut au dtend la valeur
                # du dernier datetime du rruleset auquel on ajoute la "duration"
                #self.dtend = (self.rruleset[-1]).replace(tzinfo = tzlocal())
                self.dtend = (self.rruleset[-1]) + timedelta(seconds = self.duration)
            else :
                if dtend is None :
                    # si ni UNTIL ni COUNT, par défaut, la date de fin est une année après dtstart + duration
                    #self.dtend = (dtstart + timedelta(days = 365)).replace(tzinfo = tzlocal())
                    self.dtend = (dtstart + timedelta(days = 365, seconds = self.duration))
                else :
                    #self.dtend = dtend.replace(tzinfo = tzlocal())
                    self.dtend = dtend
                # on ajoute au rruleset passé en paramètre cette limite ainsi calculée
                rrule_str += ";UNTIL={rend_date}T{rend_time}".format(
                    rend_date = self.dtend.strftime("%Y%m%d"), rend_time = self.dtend.strftime("%H%M%S"))
                # et on initialise le rruleset du yacka_when avec la rrule_str ainsi modifiée, , éventuellement
                # complétée du dtstart manquant
                if dtstart_match is None :
                    self.rruleset.rrule(rrulestr(rrule_str, dtstart = self.dtstart))
                else :
                    self.rruleset.rrule(rrulestr(rrule_str))

        else :
            self.is_recurring = False
            self.rruleset = None
            if dtend is None :
                if duration is None :
                    self.duration = 3600
                else :
                    self.duration = duration
                # self.dtend = (self.dtstart + timedelta(seconds = self.duration)).replace(tzinfo = tzlocal())
                self.dtend = self.dtstart + timedelta(seconds = self.duration)
            else :
                # dans un contexte de non récurrence, à partir du moment où dtend est définie,
                # on la considère comme prioritaire et on en déduit duration
                # self.dtend = dtend.replace(tzinfo = tzlocal())
                self.dtend = dtend
                self.duration = (self.dtend - self.dtstart).total_seconds()
        self.allday = allday

    def __repr__(self) :
        if self.is_None() :
            return ("<Yacka_when_None object>")
        else :
            return ("<Yacka_when object "
                    + repr(self.title) + " ; "
                    + repr(self.dtstart) + " ; "
                    + repr(self.dtend) + " ; "
                    + repr(self.duration) + " ; "
                    + repr(self.allday) + " ; "
                    + ("recurring ; " if self.is_recurring else "non-recurring")
                    + (repr(list(self.rruleset)) if self.is_recurring else "")
                    + ">")

    def is_None(self) :
        return (
            self.title == None
            and self.dtstart == None
            and self.dtend == None
            and self.duration == None
            and self.allday == None
            and self.is_recurring == None
            and self.rrule_str == None
        )

    def set_to_None(self) :
        self.title = None
        self.dtstart = None
        self.dtend = None
        self.duration = None
        self.allday = None
        self.is_recurring = None
        self.rrule_str = None

    def nb_occurrences(self) :
        if self.is_None() :
            return None
        elif self.is_recurring :
            return self.rruleset.count()
        else :
            return 1

    def is_all_before(self, end_dt) :
        """ Retourne True si toutes les occurrences de self sont strictement antérieures à end_dt """
        if self.is_recurring :
            return (self.rruleset.after(end_dt, inc = True) is None)
        else :
            return (self.dtstart < end_dt)

    def count_after(self, start_dt) :
        """ Retourne le nombre d'occurrences de self qui sont strictement postérieures à start_dt """
        if self.is_recurring :
            return len([dt for dt in self.rruleset if dt > start_dt])
        else :
            return (1 if self.dtstart > start_dt else 0)

    def list(self) :
        """ Retourne sous forme de liste toutes les occurrences associées à l'objet """
        if self.is_None() :
            return
        elif self.is_recurring :
            return list(self.rruleset)
        else :
            return [self.dtstart]

    def time_close(self, start_dt, gap) :
        """ Retourne True si la différence entre l'heure de départ self et celle de start_dt est inférieure à max_time_gap"""
        today_dt = date.today()
        dt1 = start_dt.replace(day = today_dt.day, month = today_dt.month, year = today_dt.year)
        dt2 = self.dtstart.replace(day = today_dt.day, month = today_dt.month, year = today_dt.year)
        time_diff = dt1 - dt2
        return True if (abs(time_diff.total_seconds() / 60) < gap) else False
