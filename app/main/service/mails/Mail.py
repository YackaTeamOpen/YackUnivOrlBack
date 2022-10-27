import smtplib
from main.config import environments,config_name
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os


class Mail:

    def __init__(self,mail):
        # This is to avoid being stuck in case server is unreachable, which already occurred !
        time_out = 2
        self.mailserver = smtplib.SMTP(environments[config_name]["smtp_server"], 587, None, time_out)
        # self.mailserver.ehlo()
        self.mailserver.starttls()
        # self.mailserver.ehlo()
        self.mailserver.login(environments[config_name]["mail"], environments[config_name]["mail_pass"])
        self.mail = mail

    def load_mail(self,data):
        path = environments[config_name]["api_app_path"] + "/main/public/mails/" + self.mail
        try:
            with open(path, 'r') as mail_file:
                content = mail_file.read().replace('\n', '')
                for key,value in data.items():
                    content = content.replace('$'+key,value)
            return content
        except Exception as e:
            print(e)
            return ""

    def send_mail(self,data,email,subject):
        msg = MIMEMultipart()
        msg['From'] = environments[config_name]["mail"]
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(self.load_mail(data),"html"))
        self.mailserver.sendmail(environments[config_name]["mail"], email, msg.as_string())
        self.mailserver.quit()


    def send_mail_no_quit(self,data,email,subject):
        msg = MIMEMultipart()
        msg['From'] = environments[config_name]["mail"]
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(self.load_mail(data),"html"))
        self.mailserver.sendmail(environments[config_name]["mail"], email, msg.as_string())

    # def quit(self):
    #     self.mailserver.quit()
