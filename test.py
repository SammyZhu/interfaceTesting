import requests
import hashlib
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from urllib import parse


# pip3 install Crypto和 pycryptodome,Python36/Lib/site-package/crypto修改为Crypto

# 请求公钥
def request_pubic():
    url = 'xxx'
    r = requests.get(url=url)
    return r.json()['publicKey']

# # sha256加密
# def sha256encode(str):
#     sha256 = hashlib.sha256()
#     sha256.update(str.encode('utf-8'))
#     res = sha256.hexdigest()
#     return res


# RSA加密
def RSAencode(pwd):
    message = pwd  # 密码加密
    print(message + '\n')
    # timestamp = int(round(time.time()))  # 时间戳
    # message = "10" + "92653589" + str(timestamp) + data  # 拼接
    # RSA加密
    # with open(pemFile, 'rb') as f:
    #     key = f.read()
    #     print(key)
    pub_key = request_pubic()
    key = '-----BEGIN PUBLIC KEY-----\n' + pub_key + '\n-----END PUBLIC KEY-----'
    print(key + '\n')
    rsakey = RSA.importKey(key)  # 导入读取到的公钥
    cipher = PKCS1_OAEP.new(rsakey, hashAlgo=SHA256)  # 生成对象
    cipher_text = base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))
    print(cipher_text.decode("utf-8"))

    return parse.quote(cipher_text.decode("utf-8"))


def login():
    username = "xxx"
    pwd = "xxx"
    url = "https://hokajp.dev.dexpo.deckers.com/cxf/home/login"
    password = RSAencode(pwd)
    print(password)
    data = {"pwd": password,
            "uid": username}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url=url, headers=headers, data=data)
    print(r.text)
    return r.cookies


if __name__ == "__main__":
    login()
