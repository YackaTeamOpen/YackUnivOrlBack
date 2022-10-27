from main.model.mail import Mail


def getAllMails():
    return Mail.query.all()


def getMailByLabel(label):
    return Mail.quey.filter_by(label=label).first()
