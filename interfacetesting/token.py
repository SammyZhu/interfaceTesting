import requests

def login():
    url = "http://test.joinpay.co:8098/property/user/login/"
    headers = {"Content-Type": "application/json"}
    data = {"password": "1",
            "username": "zxy222@qq.com"}
    r = requests.post(url=url, json=data, headers=headers)
    return r.json()["result"]["token"]