import requests
import json
import unittest
import pyexcel


class testlogin(unittest.TestCase):
    TestDataList=[]
    def test_login(self):
        TestDataList=pyexcel.get_records(file_name="testData.xlsx")
        for testdata in TestDataList[0:3]:
            with self.subTest(msg=testdata["testCaseName"]):
                print(testdata["testCaseName"])
                url = testdata["url"]
                headers = {"Content-Type":testdata["Content-Type"]}
                data = {"password":testdata["password"],
                        "username":testdata["username"]}
                r = requests.post(url=url, json=data, headers=headers)
                self.assertIn(testdata["errmsg"],r.json()["errmsg"])
                print(r.json())
        return r.json()["result"]["token"]


    # 登出接口
    def test_logout(self):
        token = testlogin.test_login(self)
        TestDataList=pyexcel.get_records(file_name="testData.xlsx")
        testdata = TestDataList[3]
        with self.subTest(msg=testdata["testCaseName"]):
            print(testdata["testCaseName"])

            url = testdata["url"]
            headers = {"Content-Type": testdata["Content-Type"],
                       "X-Authorization-Token": token}
            r = requests.post(url=url, headers=headers)  # 发送请求
            print(r.json())



if __name__ == "__main__":
    unittest.main()