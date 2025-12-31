import operator
import os

import jsonpath
import requests
import allure

from common.recordlog import logs
from common.connectData import ConnectData

class assertions:
    """
    接口断言模式封装，支持：1.字符串包含 2，结果相等断言 3，结果不相等 4，断言接口返回值里面的任意一个值 5.数据库断言
    """
    #断言状态标识，0代表成功否则其他代表失败
    def contanins_assert(self,value,response,status_code):
        """
        第一种模式，字符串包含断言，断言预期结果的字符串是否包含在接口的实际返回结果当中
        :param value:预期结果yaml文件当中volidation关键字下的结果
        :param response:
        :param status_code:
        :return:
        """
        flag = 0
        for assert_key,assert_value in value.items():
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f'预期结果：{assert_value}\n实际结果为：{status_code}','响应代码断言结果：失败',allure.attachment_type.TEXT)
                    logs.error('contains断言失败，接口实际返回值[%s]不等于[%s]'%(status_code,assert_value))
                else:
                    resp_list = jsonpath.jsonpath(response,'$..%s'%assert_key)
                    if isinstance(resp_list[0],str):
                        resp_list = ''.join(resp_list)
                    if resp_list:
                        if assert_value in resp_list:
                            logs.info('字符串包含断言成功：预期结果为：【%s】,实际结果为：【%s】' % (assert_value,resp_list))
                        else:
                            flag = flag + 1
                            logs.error('响应文本断言失败：预期结果为：【%s】,实际结果为：【%s】' % (assert_value,resp_list))
                            allure.attach(f'预期结果：{assert_value}\n实际结果为：{resp_list}', '响应文本断言结果：失败',
                                          allure.attachment_type.TEXT)
                print(flag)
        return flag


    def equals_assert(self,value,response):
        """
        相等断言模式
        :param value:预期结果，也就是yaml里面的volidation下的参数
        :param response:接口实际返回结果，必须为dict类型
        :return: flag 标识，0表示测试通过，非0表示测试不通过
        """
        flag = 0
        res_lst = []
        if isinstance(value,dict) and isinstance(response,dict): #判断value与response返回的值是否是字典类型的

            #处理实际结果的数据结果，保持与预期结果的数据结构一致
            for res in response: #循环实际结果的key值
                if list(value.keys())[0] != res:
                    res_lst.append(res) #将读取到的世界值跟预期值不相等的值加入到res_lst当中
            for rt in res_lst:
                del response[rt]
            print(f"实际结果：{response}")
            #operator(a,b) 这个函数是用来比较两个列表，字符串，字典大小、等于关系
            """
            operator.lt(a, b)判断a<b
            operator.le(a,p)判断a<=b
            operator.eq(a, b)判断a=b
            operator.ne(a, b)判断a!=b
            operator.ge(a, b)判断a>b 等
            """
            eq_result = operator.eq(response,value)
            if eq_result:
                logs.info(f'相等断言成功：接口的实际结果为：{response},等于预期结果：{str(value)}')
            else:
                flag = flag + 1
                logs.error(f'相等断言失败：接口的实际结果为：{response},不等于预期结果：{str(value)}')
        else:
            raise TypeError('相等断言失败--类型错误，预期结果和接口实际返回结果数据类型不是dict类型数据')

    def not_equals_assert(self,value,response,status_code):
        """
        不相等断言模式
        :param value:预期结果，也就是yaml里面的volidation下的参数
        :param response:接口实际返回结果，必须为dict类型
        :return: flag 标识，0表示测试通过，非0表示测试不通过
        """
        flag = 0
        res_lst = []
        if isinstance(value,dict) and isinstance(response,dict): #判断value与response返回的值是否是字典类型的

            #处理实际结果的数据结果，保持与预期结果的数据结构一致
            for res in response: #循环实际结果的key值
                if list(value.keys())[0] != res:
                    res_lst.append(res) #将读取到的世界值跟预期值不相等的值加入到res_lst当中
            for rt in res_lst:
                del response[rt]
            print(f"实际结果：{response}")
            #operator(a,b) 这个函数是用来比较两个列表，字符串，字典大小、等于关系
            """
            operator.lt(a, b)判断a<b
            operator.le(a,p)判断a<=b
            operator.eq(a, b)判断a=b
            operator.ne(a, b)判断a!=b
            operator.ge(a, b)判断a>b 等
            """
            eq_result = operator.ne(response,value)
            if eq_result:
                logs.info(f'不相等断言成功：接口的实际结果为：{response},不等于预期结果：{str(value)}')
            else:
                flag = flag + 1
                logs.error(f'不相等断言失败：接口的实际结果为：{response},等于预期结果：{str(value)}')
        else:
            raise TypeError('相等断言失败--类型错误，预期结果和接口实际返回结果数据类型不是dict类型数据')


    def assert_mysql(self,expected_sql):
        """
        数据库断言
        :param expected_sql: yaml文件的yaml的Sql语句
        :return: 返回fla标识，0表示测试通过，非0表示失败
        """
        flag = 0
        conn = ConnectData()
        db_value = conn.query(expected_sql)
        if db_value is not None:
            logs.info('数据库断言成功')
        else:
            flag = flag + 1
            logs.error('数据库断言失败，请检查数据库是否存在该数据')
        return flag



    def assert_result(self,expected,response,status_code):
        """
        断言模式通过all_flag
        :param expected: 预期结果
        :param response: 接口实际返回结果,需要json格式
        :param status_code: 接口实际返回状态码
        :return:
        """
        all_flag = 0 #总的标记码 0代表成功其他表示失败
        try:
            for yq in expected:  #循环预期结果
                for key,value in yq.items():
                    if key == 'content':  #如果是包含模式 调用第一种包含函数进行断言判断
                        flag = self.contanins_assert(value,response,status_code)
                        all_flag = all_flag + flag
                    elif key == 'eq':  #如果是相等模式就调用相等模式进行判断
                        self.equals_assert(value,response)
                        all_flag = all_flag + flag
                    elif key == 'ne':
                        self.not_equals_assert(value,response)
                        all_flag = all_flag + flag
                    elif key == 'db':
                        self.assert_mysql(value)
                        all_flag = all_flag + flag
            assert all_flag == 0
            logs.info('测试成功！')
        except Exception as e:
            logs.error(f"异常信息：{e}")
            logs.error(e)#打印异常信息



if __name__ == '__main__':
    from common.readyaml import get_testcase_yaml

    data = get_testcase_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)),r'testcase\login','login.yaml'))[0]
    print(data)
    value = data['testCase'][0]['validation']

    print(value)