#将前面的get、post的方法封装成类的形式，后面进行框架搭建的时候都是使用封装好的类去实现
import json
from idlelib.mainmenu import menudefs
import allure

import pytest
import requests
from common.recordlog import logs
from requests import utils
from common.readyaml import ReadYamlData


class SendRequests(object):
    """
    封装接口的请求
    """

    def __init__(self):
        self.read = ReadYamlData()

    def send_request(self,**kwargs):
        """
        发送请求
        :param kwargs:
        :return:
        """
        cookie = {}
        session = requests.session()
        result = {}
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml_data(set_cookie)
                logs.info(f"cookie:{cookie}")
            logs.info(f"接口的实际返回信息:{result}")
        except requests.exceptions.ConnectionError:
            logs.error('接口链接服务器异常！')
            pytest.fail('接口请求异常，可能是request的链接数过多或者请求速度过快导致程序报错！')
        except requests.exceptions.HTTPError:
            logs.error('Http异常')
            pytest.fail('Http请求异常')
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail('请求异常，请检查系统或者数据是否正常！')
        return result


    def run_main(self,name,url,case_name,header,method,cookies=None,file=None,**kwargs):
        """
        接口请求主函数

        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :param method: 请求方法
        :return:
        """
        try:
            #搜集报告日志信息
            logs.info(f'接口名称：{name}')
            logs.info(f'接口请求地址：{url}')
            logs.info(f'请求方法:{method}')
            logs.info(f'测试用例方法:{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'Cookies{cookies}')
            #处理请求参数
            req_params = json.dumps(kwargs,ensure_ascii=False)
            if 'data' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
                allure.attach(req_params,f'请求参数：{req_params}',allure.attachment_type.TEXT)
            elif 'json' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)
            elif 'params' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)
        except Exception as e:
            logs.error(e)
        resp = self.send_request(url=url,method=method,headers=header,cookies=None,files=file,verify=False,**kwargs)
        return resp






    # url = 'http://127.0.0.1:8787/dar/user/login'
    # data = {"user_name": "test01", "passwd": "admin123"}
    # header = None
    # method = "POST"

    # res = send.run_main()
    # print(res)