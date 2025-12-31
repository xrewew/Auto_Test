import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests  #导入对应的发送接口请求文件
from common.recordlog import logs  #导入对应的日志模块
from base.apiutil import BaseRequests #导入对应的类模块

@allure.feature('登录接口')
class TestLogin:  # 类名建议使用驼峰命名法，以Test开头

    #测试用例
    @allure.story('用户名和密码登录正常校验')
    @pytest.mark.parametrize('params', get_testcase_yaml('../testcase/login/login.yaml')) #这里使用get_testcase_yaml方法读取yaml相关信息后返回给params传入下面的函数
    def test_login01(self,params):
        base_Rquests = BaseRequests()
        base_Rquests.specification_yaml(params)
    #测试用例二
    @allure.story('用户名和密码登录错误校验')
    @pytest.mark.parametrize('params', get_testcase_yaml('../testcase/login/login.yaml')) #这里使用get_testcase_yaml方法读取yaml相关信息后返回给params传入下面的函数
    def test_login02(self,params):
        base_Rquests = BaseRequests()
        base_Rquests.specification_yaml(params)

    #测试用例三
    @allure.story('用户名正确但密码输入错误')
    @pytest.mark.parametrize('params', get_testcase_yaml('../testcase/login/login.yaml')) #这里使用get_testcase_yaml方法读取yaml相关文件信息给params传到给对应的函数接口当中
    def test_login03(self,params):
        base_Rquests = BaseRequests() #实例化类方法
        base_Rquests.specification_yaml(params)

