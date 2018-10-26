#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import unittest
import pyexcel
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import xlwt


class testinterface(unittest.TestCase):
    #新建测试报告表格
    global worksheet, workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1',cell_overwrite_ok=True)

    worksheet.write(0, 0, label='testCaseName')
    worksheet.write(0, 1, label='url')
    worksheet.write(0, 2, label='errmsg')
    worksheet.write(0, 3, label='data')
    worksheet.write(0, 4, label='response')
    worksheet.write(0, 5, label='test_result')

    #打开测试数据表格
    TestDataList = pyexcel.get_records(file_name="testData.xlsx")

    def test_interface(self):
        global num_total,total_time,pass_rate
        num_pass=0
        num_total=0
        start_time = datetime.datetime.now()
        for testdata in testinterface.TestDataList:
            with self.subTest(msg=testdata["testCaseName"]):
                num_total=num_total+1
                print(testdata["testCaseName"])
                url = testdata["url"]
                headers = {"Content-Type":"application/json"}
                data = json.loads(testdata["data"])
                if testdata["data"]!="null":
                    r = requests.post(url=url, json=data, headers=headers)
                else:
                    token = self.login()
                    headers = {"Content-Type": "application/json",
                               "X-Authorization-Token":token}
                    r = requests.post(url=url, headers=headers)
                self.assertIn(r.json()["errmsg"],testdata["errmsg"])
                #testdata["response"]=r.json()
                # if r.status_code==200:
                #     num_pass=num_pass+1
                #     testdata["test_result"]="PASS"
                # else:
                #     print("FAIL")
                #     testdata["test_result"]="FAIL"
                # print(testdata)
                self.report(testdata)
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).seconds
        pass_rate=num_pass/num_total
        #self.send_mail()

    #登录接口取token
    def login(self):
        url = "http://test.joinpay.co:8098/property/user/login/"
        headers = {"Content-Type": "application/json"}
        data = {"password": "1",
                "username": "zxy222@qq.com"}
        r = requests.post(url=url, json=data, headers=headers)
        return r.json()["result"]["token"]



    #测试结果写入excel
    def report(self,data):
        val=1
        for key, value in data.items():
            if key == "testCaseName":
                worksheet.write(val, 0, value)
            elif key == "url":
                worksheet.write(val, 1, value)
            elif key == "errmsg":
                worksheet.write(val, 2, value)
            elif key == "data":
                worksheet.write(val, 3, value)
            elif key == "response":
                worksheet.write(val, 4, value)
            elif key == "test_result":
                worksheet.write(val, 5, value)
            else:
                pass
        val += 1
        workbook.save('OK.xlsx')

    #邮件发送测试报告
    def send_mail(self):
        mail_host = "smtp.mxhichina.com"  # 设置服务器
        mail_user = "zhuxinyi@joinpay.cn"  # 用户名
        mail_pass = "Qdv1Bji3"

        sender = 'zhuxinyi@joinpay.cn'
        receiver = 'zhuxinyi@joinpay.cn'

        message = MIMEMultipart()
        message['From'] = formataddr(["zhuxinyi", sender])
        message['To'] = formataddr(["测试", receiver])
        message['Subject'] = "邮件测试"

        message.attach(
            MIMEText('本次共测试' + str(num_total) + '个用例，'\
                    '通过率为' + str(pass_rate) + ','\
                    '耗时' + str(total_time) + '秒，详细请见附件。', 'plain', 'utf-8'))

        att1 = MIMEApplication(open("testReport.xlsx", 'rb').read())
        att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', "testReport.xlsx"))
        att1["Content-Disposition"] = 'attachment; filename="test.txt"'
        message.attach(att1)

        try:
            server = smtplib.SMTP_SSL(mail_host, 465)
            server.login(mail_user, mail_pass)
            server.sendmail(sender, receiver, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


if __name__ == "__main__":
    unittest.main()