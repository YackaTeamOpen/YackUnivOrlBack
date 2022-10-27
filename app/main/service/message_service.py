from flask_login import current_user
from main import db
from main.model.message import Message
from main.service.user_service import getUserById
from main.service.mails.Mail import Mail
import datetime
import smtplib


# Début de définition d'une table de messages système. A associer
# à une "vraie" table, bien sûr...
system_message_ids = {
    "passenger_shared_trip_deleted": 1,
    "driver_shared_trip_deleted": 2,
    "passenger_request_for_acceptance": 3,
    "driver_request_for_acceptance": 4,
    "passenger_notification_of_acceptance": 5,
    "driver__notification_of_acceptance": 6,
    "passenger_notification_of_refusal": 7,
    "driver__notification_of_refusal": 8,
    "passenger_notification_of_modification": 9,
    "driver__notification_of_modification": 10,
    "passenger_notification_of_cancellation": 11,
    "driver__notification_of_cancellation": 12,
    "passenger_notification_of_refusal_before_accept": 13,
    "driver__notification_of_refusal_before_accept": 14,
}

# Ce sont les dictionnaires suivants qui pourraient être remplacés par une table dans la BDD...
system_message_intros = {
    1: "Malheureusement, ",
    2: "Malheureusement, ",
    3: "Tadaam !\n",
    4: "Tadaam !\n",
    5: "Bonne nouvelle !\n",
    6: "Bonne nouvelle !\n",
    7: "Malheureusement, ",
    8: "Malheureusement, ",
    9: "Attention !\n",
    10: "Attention !\n",
    11: "Malheureusement, ",
    12: "Malheureusement, ",
    13: "Malheureusement, ",
    14: "Malheureusement, ",
}
system_message_labels = {
    1: "n'a pas pu accepter votre demande de partage.",
    2: "n'a pas pu accepter votre proposition de partage.",
    3: "vous a proposé de partager un trajet.",
    4: "vous a demandé de partager un trajet.",
    5: "a accepté votre demande de partage de trajet. Veuillez prendre connaissance des dates des différents trajets validés dans votre vue agenda.",
    6: "a accepté votre proposition de partage de trajet. Veuillez prendre connaissance des dates des différents trajets validés dans votre vue agenda.",
    7: "n'a pas pu accepter votre demande de partage de trajet",
    8: "n'a pas pu accepter votre proposition de partage de trajet",
    9: "a dû modifier certaines dates de partage de son trajet.  Veuillez prendre connaissance des modifications dans votre vue agenda.",
    10: "a dû modifier certaines de partage de son trajet.  Veuillez prendre connaissance des modifications dans votre vue agenda.",
    11: "a dû annuler le partage de son trajet pour l'ensemble des dates restant à venir.",
    12: "a dû annuler le partage de son trajet pour l'ensemble des dates restant à venir.",
    13: "a dû annuler sa proposition de partage de trajet.",
    14: "a dû annuler sa demande de partage de trajet.",
}

SMTP_server = None


def getMessageById(message_id):
    message = Message.query.filter_by(id=message_id).first()
    if message != None:
        message.user1db = getUserById(message.user1)
        message.user2db = getUserById(message.user2)
    return message


def getLastMessageId(user_id, other_message_id):
    """Retourne le dernier message de conversation entre 2 utlisateurs
    None si rien
    """
    messages1 = Message.query.filter_by(user1=user_id, user2=other_message_id)
    messages2 = Message.query.filter_by(user2=user_id, user1=other_message_id)
    last_message = messages1.union(messages2).order_by(Message.send_date.desc()).first()
    return last_message.id if last_message != None else None


def create_new_message(data):
    send_message_to_user(
        current_user.id,
        data["other_user_id"],
        data["message"],
        send_date=datetime.datetime.now(),
    )
    return {"status": "success", "message": "message inserted"}, 201


def send_message_to_user(
    from_user_id,
    to_user_id,
    message_content,
    send_date=None,
    send_email=True,
    send_notification=True,
    notification_title=None,
):
    """
    Send a message to a user,
    by default, send_date = the current date
    also send the message by email and using onesignal for notifications
    """

    # Create message in database
    # it will be displayed in conversations
    message = Message(
        user1=from_user_id,
        user2=to_user_id,
        message=message_content,
        send_date=datetime.datetime.now() if send_date is None else send_date,
        read_date=None,  # unread
    )
    save_changes(message)

    # Send a notification using onesignal
    if send_notification:
        from_user = getUserById(from_user_id)
        notification_title = ""
        if from_user is not None and from_user.surname:
            notification_title = "Nouveau message d"
            if from_user.surname.lower()[0] in "aeiouyh":
                notification_title = notification_title + "'" + from_user.surname + " !"
            else:
                notification_title = (
                    notification_title + "e " + from_user.surname + " !"
                )

    # Send an email
    if send_email:

        from_user = getUserById(from_user_id)
        to_user = getUserById(to_user_id)

        if to_user.email != "":

            title = "Nouveau message d"
            if from_user.surname.lower()[0] in "aeiouyh":
                title = title + "'" + from_user.surname + " !"
            else:
                title = title + "e " + from_user.surname + " !"

            data = {
                "title": title,
                "senderusername": from_user.surname,
                "messagecontent": message_content,
            }

            try:
                Mail("notification").send_mail(data, to_user.email, title)
            except Exception as e:
                print("Failed to send email-notification", e)
    return message


def get_message(user_id):
    user = getUserById(current_user.id)
    other_user = getUserById(user_id)
    conversation = get_conversation(user.id, other_user.id, read=True)
    return {"user": user, "other_user": other_user, "conversation": conversation}


def get_conversation(current_user_id, user2_id, read=True):
    messages1 = Message.query.filter_by(user1=current_user_id, user2=user2_id)
    messages2 = Message.query.filter_by(user2=current_user_id, user1=user2_id)
    if read:
        for message in messages2:
            message.read_date = datetime.datetime.now()
            db.session.add(message)
    db.session.commit()
    conversation = messages1.union(messages2).order_by(Message.send_date).all()
    for i, message in enumerate(conversation):
        conversation[i].current_user_id = current_user_id
    return conversation


def update_message(message_id, data):
    pass


def delete_message(message_id):
    pass


def warn_users(
    actor_id,
    user_id_list_list,
    message_id_list,
    additional_info_list,
    alert_level_list,
    yacka_messages_only = False
) :
    # Envoie, de la part de Yacka, et pour chaque liste de users de la première liste,
    # le message correspondant de la seconde.
    #
    yacka_user_id = 1
    actor_surname = getUserById(actor_id).surname
    for user_list, message_id, additional_info, alert_level in zip(user_id_list_list,
                                                                   message_id_list, additional_info_list, alert_level_list) :
        # On envoie le message à la liste d'utilisateurs concernés
        for uid in user_list :
            # print("--> before adding msg to DB ({})".format(datetime.datetime.now()))
            # crée une trace du message dans la base
            message = Message(
                user1 = yacka_user_id,
                user2 = uid,
                message = system_message_intros[message_id] + actor_surname + " " + system_message_labels[message_id],
                alert_level = alert_level,
                send_date = datetime.datetime.now(),
                read_date = None,  # unread
            )
            db.session.add(message)
            if not yacka_messages_only :
                notification_title = "Nouveau message de Yacka"
                # Preparer les infos à envoyer par email
                to_user_email = getUserById(uid).email
                if to_user_email != "":
                    data = {
                        "title": notification_title,
                        "senderusername": "Yacka",
                        "messagecontent": system_message_intros[message_id] + actor_surname + " " + system_message_labels[message_id],
                    }
                    global SMTP_server
                    if SMTP_server is None:
                        SMTP_server = Mail("notification")
                    try:
                        # essaie d'envoyer un email sans se connecter au préalable, une connexion
                        # étant peut-être déjà initialisée, ce qui permet de gagner du temps
                        # print("--> before 1st send_mail try to {} ({})".format(datetime.datetime.now(), to_user_email))
                        SMTP_server.send_mail_no_quit(
                            data, to_user_email, notification_title
                        )
                    except smtplib.SMTPException:
                        # Erreur SMTP : il faut réinitialiser la connexion, puis relancer l'envoi
                        # print("--> before SMTP exception dealing to {} ({})".format(datetime.datetime.now(), to_user_email))
                        SMTP_server = Mail("notification")
                        SMTP_server.send_mail_no_quit(
                            data, to_user_email, notification_title
                        )
    # On commet les changements de la BDD
    commit()
    # On compte que la connexion SMTP se fermera par timeout; donc pas de
    # SMTP_server.quit()


def get_conversations(user_id):
    # Retourne la liste de toutes les conversations en relation avec
    # L'utlisateur courant
    # Cette liste contient notamment le dernier message envoyé
    # pour qu'il soit affiché
    other_ids1 = Message.query.filter(Message.user1 == user_id).all()
    other_ids2 = Message.query.filter(Message.user2 == user_id).all()
    other_ids = list(set([o.user2 for o in other_ids1] + [o.user1 for o in other_ids2]))
    convs = list()
    for other_id in other_ids:
        last_conv_other_msg_id = getLastMessageId(user_id, other_id)
        if last_conv_other_msg_id is not None:
            msg = getMessageById(last_conv_other_msg_id)
            msg.current_user_id = user_id
            convs.append(msg)

    return {"conversations": sorted(convs, key=lambda m: m.send_date, reverse=True)}


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def commit():
    db.session.commit()


# Remplacer message ==> "nom_de_la_table"
# Remplacer Message ==> "Nom_de_la_table"
