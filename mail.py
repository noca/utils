# -*- coding: utf-8 -*-

# import sys
# import email
# import mimetypes
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEImage import MIMEImage
# import smtplib
# import copy


# CONT_MAIL_LIST = ['',
#                   ]

# MAIL_MAP = {'server': "smtp.mailgun.org",
#                       'port': 587,
#                       'user': "",
#                       'password': "",
#                       'from': ""}


# def sendmail(paramMap):
#     smtp = smtplib.SMTP()
#     if paramMap.has_key("server") and paramMap.has_key("user") and paramMap.has_key("password"):
#         try:
#             # smtp.set_debuglevel(1)
#             smtp.connect(paramMap["server"], paramMap["port"])
#             smtp.ehlo()
#             smtp.starttls()
#             smtp.login(paramMap["user"], paramMap["password"])
#         except Exception, e:
#             print "smtp login exception:" + str(e)
#             return False
#     else:
#         print "Parameters incomplete!"
#         return False

#     if (paramMap.has_key("subject") and paramMap.has_key("from") and paramMap.has_key("to")) == False:
#         print "Parameters incomplete!"
#         return False

#     if paramMap["type"] == "html":
#         msg = MIMEText(paramMap["content"], 'html', 'utf-8')
#     else:
#         msg = MIMEText(paramMap["content"], 'plain', 'utf-8')

#     msg['subject'] = paramMap["subject"]
#     msg['from'] = paramMap["from"]
#     msg['to'] = paramMap["to"]
#     TempAddTo = paramMap["to"]
#     if TempAddTo.find(",") != - 1:
#         FinallyAdd = TempAddTo.split(",")
#     else:
#         FinallyAdd = TempAddTo

#     # 群发地址需要使用列表，不能用逗号隔开的字符串。
#     smtp.sendmail(paramMap["from"], FinallyAdd, msg.as_string())
#     smtp.quit()
#     # print "send mail success!"
#     return True


# def mail(mailto, subject, content):
#     mail_content = content

#     tmp_mail_map = copy.deepcopy(MAIL_MAP)
#     if mailto:
#         tmp_mail_map["to"] = ",".join(CONT_MAIL_LIST) + "," + mailto
#     else:
#         tmp_mail_map["to"] = ",".join(CONT_MAIL_LIST)
#     # print tmp_mail_map

#     tmp_mail_map["subject"] = subject
#     # tmp_mail_map["type"] = "json"
#     tmp_mail_map["type"] = "html"
#     tmp_mail_map["content"] = mail_content
#     return sendmail(tmp_mail_map)


# if __name__ == '__main__':
#     mail(None, "物理机创建完毕", "美丽的宝贝,这只是一个测试而已,你感动了么？")



import email
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


SMTP_HOST = ""
SMTP_PORT = 25


CONT_MAIL_LIST = [
    '',
]


def mail(mailto, subject, content):
    mail_from = ''
    mail_cc = None
    mail_body_type = 'html'

    msg = MIMEMultipart('alternative')
    msg['subject'] = subject
    msg['from'] = mail_from
    # assert(isinstance(mailto, list))

    if isinstance(mailto, list):
        mailto.extend(CONT_MAIL_LIST)
        msg['to'] = ','.join(mailto)
    elif isinstance(mailto, str):
        msg['to'] = ",".join(CONT_MAIL_LIST) + "," + mailto
        mailto = msg['to'].split(",")
        # print mailto
    else:
        mailto = CONT_MAIL_LIST
        msg['to'] = ",".join(CONT_MAIL_LIST)

    if mail_cc:
        assert(isinstance(mail_cc, list))
        msg['cc'] = ','.join(mail_cc)
    body = MIMEText(content, mail_body_type)
    msg.attach(body)
    smtp = smtplib.SMTP()
    smtp.connect(SMTP_HOST, SMTP_PORT)
    smtp.sendmail(mail_from, mailto, msg.as_string())


if __name__ == '__main__':
    mail(None, "物理机创建完毕", "1. 美丽的宝贝,这只是一个测试而已,你感动了么？")
    mail(["tawateer@gmail.com"], "物理机创建完毕", "2. 美丽的宝贝,这只是一个测试而已,你感动了么？")
    mail("tawateer@gmail.com", "物理机创建完毕", "3. 美丽的宝贝,这只是一个测试而已,你感动了么？")
    mail("tawateer@gmail.com, tawateer@gmail.com", "物理机创建完毕", "4. 美丽的宝贝,这只是一个测试而已,你感动了么？")
