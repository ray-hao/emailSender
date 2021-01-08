#!/usr/bin/env python3

import threading
import smtplib
import time
from datetime import datetime, timedelta

to_addr = ' ' #Replace with Target Email Address
email_body1 = '''  ''' #Replace with Email Text

time_fmt = "%y%b%d %H:%M:%S"

class SendGmail:
    def __init__(self, from_addr, app_passwd, subject, message, time_from, delay = 0):
        self.Done = False
        self.from_addr = from_addr
        self.app_passwd = app_passwd
        self.subject = subject
        self.time_from = datetime.strptime(time_from, time_fmt)
        self.delay = delay
        self.login_id = self.from_addr.split('@')[0]

        msg  = "From: {}\n".format(self.from_addr)
        msg += "To: {}\n".format(to_addr)
        msg += "Subject: {}\n".format(self.subject)
        msg += message
        self.message = msg

        thrd = threading.Thread(target=self.run)
        thrd.start()

    def send_gmail(self):
        print("SMTP_SSL: {}".format(datetime.now().strftime("%M:%S.%f")))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        print("SMTP_login: {}".format(datetime.now().strftime("%M:%S.%f")))
        server.login(self.login_id, self.app_passwd)
        print("SMTP_sendmail: {}".format(datetime.now().strftime("%M:%S.%f")))
        server.sendmail(self.from_addr, [to_addr], self.message)
        print("SMTP_Done: {}".format(datetime.now().strftime("%M:%S.%f")))
        server.quit()

    def run(self):
        while True:
            if datetime.now() >= self.time_from:
                if self.delay:
                    time.sleep(self.delay)
                self.send_gmail()
                self.Done = True
                return
            else:
                time.sleep(0.01)

sg1 = SendGmail("",               # email address
                "",               # password for first email account
                "",               # subject
                email_body1,      # Email body
                "",               # start time, donot change format
                0)                # interval                               
                            
while not sg1.Done:
    time.sleep(5)
