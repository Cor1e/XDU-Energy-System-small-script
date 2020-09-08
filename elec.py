from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import json
import re
import requests
from libxduauth import EnergySession
import time

class Mail:
    def __init__(self, json_data):
        self.host_server = json_data["host_server"]
        self.sender_qq = json_data["sender_qq"]
        self.pwd = json_data["pwd"]
        self.sender = json_data["sender"]
        self.mail_subject = json_data["mail_subject"]
        self.receivers = json_data["receivers"]

    def send(self, name, balance):
        try:
            # ssl登录
            smtp = SMTP_SSL(self.host_server)
            smtp.ehlo(self.host_server)
            smtp.login(self.sender_qq, self.pwd)
            mail_content=""
            # 定义邮件内容
            for n, m in zip(name, balance):
                mail_content = mail_content + "表名称：" + n + "剩余量：" + m
            mail_content = mail_content+time.strftime("%Y-%m-%d %H:%M:%S")
            msg = MIMEText(mail_content, "plain", "utf-8")
            msg["Subject"] = Header(self.mail_subject, "utf-8")
            msg["From"] = self.sender
            msg["To"] = self.receivers
            # 发送邮件
            smtp.sendmail(self.sender, self.receivers.split(","), msg.as_string())
            smtp.quit()
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败")
            print(e)

    def senderror(self):
        try:
            smtp = SMTP_SSL(self.host_server)
            smtp.ehlo(self.host_server)
            smtp.login(self.sender_qq, self.pwd)
            mail_content = "Something wrong happened when chatching the webpage, please deal with it."
            msg = MIMEText(mail_content, "plain", "utf-8")
            msg["Subject"] = Header(self.mail_subject, "utf-8")
            msg["From"] = self.sender
            msg["To"] = self.receivers
            # 发送邮件
            smtp.sendmail(self.sender, self.receivers.split(","), msg.as_string())
            smtp.quit()
            print("爬虫异常邮件发送成功")
        except Exception as e:
            print("爬虫异常邮件发送失败")
            print(e)

def Webpage(json_data):
    ses = EnergySession(json_data["ELEC_USERNAME"], json_data["ELEC_PASSWD"])

    balance_page = ses.get('http://10.168.55.50:8088/searchWap/webFrm/met.aspx').text
    pattern_name = re.compile('表名称：(.*?)  ', re.S)
    name = re.findall(pattern_name, balance_page)
    pattern_balance = re.compile('剩余量：(.*?) </td>', re.S)
    balance = re.findall(pattern_balance, balance_page)
    print("电费账号：", json_data["ELEC_USERNAME"])
    for n, b in zip(name, balance):
        print(" 表名称：", n, "剩余量：", float(b))
    return name, balance


fp = open('./credentials.json', 'r', encoding='utf8')
json_data = json.load(fp)

try:
    name, balance = Webpage(json_data)
except:
    errordealmail = Mail(json_data)
    errordealmail.senderror()

amount = re.sub("\D", "", list(balance)[2])
if amount<'15':
    mail = Mail(json_data)
    mail.send(name,balance)
