#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import unittest
import datetime

class testinterface(unittest.TestCase):
    def test_interface(self):
        global num_total,total_time,pass_rate
        num_pass=0
        num_total=0
        val=1
        start_time = datetime.datetime.now()
        for testdata in testinterface.TestDataList:
            with self.subTest(msg=testdata["testCaseName"]):
                num_total=num_total+1
                print(testdata["testCaseName"])
                url = testdata["url"]
                headers = {"Content-Type":"application/json"}
                data = json.loads(testdata["data"])
                if testdata["url"]!="http://test.joinpay.co:8098/property/user/login/":
                    token = self.login()
                    headers = {"Content-Type": "application/json",
                               "X-Authorization-Token": token}
                if testdata["data"]!="null":
                    r = requests.post(url=url, json=data, headers=headers)
                else:
                    r = requests.post(url=url, headers=headers)
                testdata["response"]=r.json()
                print(testdata["response"])
                if r.status_code==200:
                    num_pass += 1
                    testdata["test_result"]="PASS"
                else:
                    print("FAIL")
                    testdata["test_result"]="FAIL"
                self.report(testdata,val)
                val += 1
                self.assertIn(r.json()["errmsg"],testdata["errmsg"])
        end_time = datetime.datetime.now()
        total_time = (end_time - start_time).seconds
        pass_rate=num_pass/num_total
        self.send_mail()

if __name__ == "__main__":
    unittest.main()