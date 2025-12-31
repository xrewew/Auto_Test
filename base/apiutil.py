import re

from common.readyaml import ReadYamlData,get_testcase_yaml
from common.debugtalk import DbugTalk
import json
import allure
import jsonpath

from common.sendrequests import SendRequests
from conf.operationConfig import OperationConfig
from test_2 import cookie
from common.recordlog import logs
from common.assertions import assertions

assert_res = assertions()

class BaseRequests:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequests()

    def replace_load(self,data):
        """
        yaml文件替换解析有${}这种的数据
        :return:
        """
        str_data = data
        cookie = None
        if not isinstance(data,str): #判断是否为字符串类型,如果不是字符串类型
            str_data = json.dumps(data,ensure_ascii=False) #转换为字符串类型
        #通过字符串索引将${}的值取出来替换
        for i in range(str_data.count('${')): #遍历这个提取到的数据
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("$") #找到该含有${}再字符串的索引位置,这里是开头的位置
                end_index = str_data.index("}",start_index) #结尾部分
                ref_all_params = str_data[start_index:end_index + 1]
                #取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')] #从第二个索引开始提取到‘（’结束
                #取出函数里面的参数值
                func_params = ref_all_params[ref_all_params.index('(')+1:ref_all_params.index(')')]
                #传入替换的参数获取对应的值
                # print("yaml文件替换解析之前：", str_data)
                extract_data = getattr(DbugTalk(),func_name)(*func_params.split(",") if func_params else '') #加个*表示传参数量未知，得加这个
                #将提取到的结果替换原来的信息
                str_data = str_data.replace(ref_all_params,str(extract_data))
                # print("yaml文件替换之后：",str_data)
        #还原数据
        if data and isinstance(data,dict):
            data = json.loads(str_data)
        else:
            data = str_data

        return data

    def specification_yaml(self,case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info: list 类型 ，调试取得case_info[0]
        :return:
        """
        cookie = None
        params_type = ['params','data','json']  #请求参数类型列表，实现发送接口请求时只支持这三种
        try:
            base_url  = self.conf.get_envi('host')
            url = base_url + case_info['baseInfo']['url']
            allure.attach(url,f'接口地址：{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name,f'接口名称：{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method,f'请求方法：{method}')
            header = case_info['baseInfo']['header']
            allure.attach(str(header),f'请求头：{header}',allure.attachment_type.TEXT)
            try:
                cookie = self.replace_load(case_info['baseInfo']['cookies'])
            except:
                pass

            for tc in case_info['testCase']: #循环yaml里得测试用例
                case_name = tc.pop('case_name') #。pop函数为先返回case_name给case_name后返回从tc例表中删除case_name的新的列表数据
                allure.attach(case_name,f'测试用例名称：{case_name}')
                validation = tc.pop('validation')
                extract = tc.pop('extract',None)
                extract_list = tc.pop('extract_list',None)
                for key,value in tc.items():
                    if key in params_type:
                        tc[key] = self.replace_load(value)
                res = self.send.run_main(name=api_name,url=url,case_name=case_name,header=header,method=method,cookies=cookie,file=None,**tc)
                res_text = res.text #接口实际的返回值
                allure.attach(res.text,f'接口响应的信息',allure.attachment_type.TEXT)
                allure.attach(str(res.status_code),f'接口的状态码：{res.status_code}',allure.attachment_type.TEXT)
                res_json = res.json()
                if extract is not None:
                    self.extract_data(extract,res_text)
                if extract_list is not None:
                    self.extract_data_list(extract_list,res_text)

                #处理json断言
                assert_res.assert_result(validation,res_json,res.status_code) #validation预期结果，res_json接口实际返回结果，res.status_code获取到接口实际返回的状态码信息
        except Exception as e:
            logs.error(e)
            raise e  ##这里必须加这个。不然allure生成的报告即使测试用例不通过，也会给显示痛过

    def extract_data(self,textcase_extract,response):
        """
        提取接口的返回值，支持正则表达式提取及json提取器
        :param taxtcase_extract:
        :param response:
        :return:
        """
        prttenr_lst = ['(.+?)','(.*?)',r'(\d+)',r'(\d*)']
        try:
            for key,value in textcase_extract.items():
                #处理正则表达式的提取
                for pat in prttenr_lst:
                    if pat in value:
                        ext_list = re.search(value,response)
                        if pat in [r'(\d+)',r'(\d*)']:
                            extract_data = {key:int(ext_list.group(1))}
                        else:
                            extract_data = {key:ext_list.group(1)}
                        logs.debug(f'正则表达式提取到的token参数：{extract_data}')
                        self.read.write_yaml_data(extract_data)
                #处理json提取器
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response),value)[0]  #json.load将字符串转化为json格式
                    print(ext_json)
                    if ext_json:
                        extract_data = {key:ext_json}
                    else:
                        extract_data = {key:'未提取到数据，该接口返回值为空或者json提取表达式有误'}
                    logs.info(f'json提取到的参数为：{extract_data}')
                    self.read.write_yaml_data(extract_data)
        except :
            logs.error('接口返回值提取异常，请检查yaml文件的extract表达式是否正确')

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    data = get_testcase_yaml("../testcase/login/login.yaml")[0]
    data2 = get_testcase_yaml("../testcase/login/login.yaml")

    base = BaseRequests()
    # res = base.replace_load(data)

    base.specification_yaml(data)
