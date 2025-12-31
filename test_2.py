import requests
from requests import session

# -------------------------------------post请求------------------------
# url = 'http://127.0.0.1:8787/dar/user/login'
#
# headers = {'Content-Type': 'application/x-www-formurlencoded;charset=UTF-8'}
#
data = {'user_name': 'test01', 'passwd': 'admin123'}
#
# res = requests.post(url,data=data)
#
# print(res.text)

def test_login():
    resp=requests.request(
        method="POST",
        url="http://127.0.0.1:8787/dar/user/login",
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
        data={'user_name': 'test01', 'passwd': 'admin123'}
    )
    # print(resp.text) #返回文本数据，返回的是字符串类型的数据（辨别快速方式为双引号为字符串，单引号为 字典）
    print(resp)  #默认返回状态码
    # print(resp.text.encode().decode('unicode-escape')) 如果返回的数据出现乱码或者其他，则需要解码成中文
    # print(resp.content) #返回二进制
    # print(resp.json()) #返回json，数据为字典数据类型

# if __name__ == "__main__":  #这个代码的意思是必须调用下面的函数
#     test_login()
test_login()
# ----------------------------------get请求--------------------------------------
url="http://127.0.0.1:8787/coupApply/cms/goodsList"
headers={'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}
json={"msgType": "getHandsetListOfCust","page":1,"size":20}
def test_goodlist():
    resp = requests.request(
        method="GET",   #get的方式请求时，上传的参数只有params这一种数据类型方式，其他方式均会出现错误
        url="http://127.0.0.1:8787/coupApply/cms/goodsList",
        headers={'Content-Type':'application/x-www-formurlencoded;charset=UTF-8'},
        params={"msgType": "getHandsetListOfCust","page":1,"size":20}
    )
    # print(resp) 默认返回接口的状态码
    print(resp.text,type(resp.text)) #type查看返回的数据类型

# test_goodlist()

# resp2 = requests.get(url=url, params=json,headers=headers)
# print(resp2.text)

# -----------------------delete请求---------------------------


# ------------------------put请求-----------------------------


# --------------------------requests.session 创建会话------------------------
session = requests.session()

resp3 = session.request(method="GET",url=url,params=json,headers=headers)
print(resp3)

#---------------------------cookie（存储用户的账号信息，不需要重复的登陆，当网页需要重新验证身份信息后可直接使用cookie进行验证，无需写重新登录）-------------------------------
resp4 = session.request(method="POST",url="http://127.0.0.1:8787/dar/user/login",data=data,headers=headers) #登录操作

cookie = requests.utils.dict_from_cookiejar(resp4.cookies) #获取前一次登录的cookie

print(cookie)
print(resp4.text)