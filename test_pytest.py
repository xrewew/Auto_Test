import pytest
import requests
import jsonpath

#创建用例的基本要求 1.创建test_开头的py文件 2.创建test_开头的函数 3.在函数中使用断言
@pytest.mark.skip #表示跳过不执行这个用例
def test_abc():
    assert 1 == 2

@pytest.mark.skip
def test_baidu():
    resp = requests.request(  #这里的resp表示我们向对方发送数据后，对方响应返回的数据保存在resp当中
        method="GET", #HTTP的请求方法，必填
        url="http://baidu.com", #接口地址，必填
        data={"a":1,"b":2},#接口参数，选填，类型有多种
        json={}, #接口参数类型，选填，类型有多种
        files={}, #接口参数类型，选填，类型有多种
        headers={}  #接口参数类型，选填，类型有多种
    )  #基本用法也是统一用法，调用requets的get方法进行发送请求

    print(resp.status_code) #状态码为整型
    print(resp.headers) #字典
    print(resp.text) #字符串
    print(resp.json()) #json

    #进行断言,对结果判断是否成功
    assert resp.status_code == 200
    assert 'baidu' in resp.text

#---------发送表单数据用例 --主要使用在web项目 1.参数只能是字符串类型 2.请求头中包含form  技巧：如果data参数是一个字典，则自动将其识别为表单，并且自动添加请求头
user_infom = {
    "username" : "xixixin",
    "password" : "Xer20020516"
}
def test_api_form():
    resp = requests.request(
        method="post",
        url="http://http://api.fbi.com:9225/rest-v1/login/with_form",
        # data="username=xiexixin&password=Xer20020516",
        data=user_infom
        # headers={
        #     "Content-Type": "application/x-www-form-urlencoded",
        # } #没有请求头
    )
    assert resp.status_code == 200

#-----JSON参数 --主要用在各类项目中，1.参数类型很多：字符串、数字、布尔值、空值、数组 2-请求头中包含json  request技巧：如果传递json参数，自动识别为json参数类型，自动添加请求头
def test_api_json():
    resp = requests.request(
        method="post",
        url="http://api.fbi.com:9225/rest/v1/login/with_json",
        # data=user_infom #表单的方式传参，json接口传表单参数会报错
        json=user_infom #要以json方式传参，传字典数据结构
    )
    assert resp.status_code == 200
#文件上传（常用场景）----1,上传方式有2种：-boby直传 -表单  2.注意请求头说明使用那种方式 request技巧：1.如果传递files参数，自动识别为表单文件上传，自动添加请求头
def test_api_file_upload():
    path = r"E:pyProJect\1234\beifan.txt"  #字符串
    f = open(path,"r") #将字符串文件打开变成文件对象才能进行上传，不对字符串地址进行打开处理的话，就会以字符串的方式进行上传，系统就会报错
    resp = requests.request(
        method="post",
        url="http://api.fbi.com:9225/rest/v1/upload/one_file",
        files={"file":f} #这里是已字典的方式上传文件内容，
    )
    assert resp.status_code == 200

#接口关联(依赖关系）如登录接口跟上传文件接口，上传的时候必须验证用户身份检验登陆时的taken数据后才能上传，此时登录跟上传就是关联关系，登录关联上传，而上传则就依赖登录接口
def test_api_token():
    resp = requests.request(
        method="post",
        url="http://api.fbi.com:9225/rest/v1/login",
        data=user_infom #用户账号密码数据表单
    )
    assert resp.status_code == 200
    print(resp.text) #打印接口的返回值，发现会返回token值，也就是身份的凭据
#变量提取
# 如何从上一个接口中提取出变量：1.re 2.jsonpath：针对json接口 3.xpath
# 如果是一个接口响应返回的值为json数据，则可使用jsonpath方式提取变量，步骤1.先导入jsonpath：import jsonpath 步骤2：
    token = jsonpath.jsonpath(resp.json(),'$.token')[0] #使用jsonpath将resp返回值中的token返回值保存在token[0]的位置

    resp = requests.request(
        method="get",
        url="http://api.fbi.com:9225/rest/v1/auth/token_with_headers", #这里的接口受到保护，需要在请求头中加入token才能正常访问
        # headers={"token": "123231231"} #需要传递正确的登录凭据token
        headers={"token":token}
    )
    assert resp.status_code == 200
#参数化测试----数据驱动测试 = 参数化测试 + 数据文件（scy、json、yaml、execl、mysql）

#日志、报告、插件等框架封装
#pytest是一个专注用例执行的框架
#如果需要增加新的供，需要借助第三方插件
#I-P-O ：输入简单：用例不是代码，只是数据-----输出简单：不是文本，是精美网页-----处理灵活：记录日志、发送通知

if __name__ == '__main__':
    pytest.main()