import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests
from common.recordlog import logs
from base.apiutil import BaseRequests

@allure.feature('商品管理')
class TestLogin:  # 类名建议使用驼峰命名法，以Test开头

    #测试用例
    @allure.story('获取商品列表')
    @pytest.mark.parametrize('params', get_testcase_yaml('../testcase/productManger/getProductList.yaml')) #这里使用get_testcase_yaml方法读取yaml相关信息后返回给params传入下面的函数
    def test_get_productList01(self,params):
        base_Rquests = BaseRequests()
        base_Rquests.specification_yaml(params)

    # @allure.story('获取商品详情信息')
    # @pytest.mark.parametrize('params', get_testcase_yaml('../testcase/productManger/ProductDetail.yaml')) #这里使用get_testcase_yaml方法读取yaml相关信息后返回给params传入下面的函数
    # def test_get_productDetail02(self,params):
    #     base_Rquests = BaseRequests()
    #     base_Rquests.specification_yaml(params)