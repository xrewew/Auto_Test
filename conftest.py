import pytest
from common.recordlog import logs
from common.readyaml import ReadYamlData


read = ReadYamlData()
@pytest.fixture(scope='session',autouse=True)
def clear_yaml_data():
    read.clear_yaml_data()

@pytest.fixture(scope="session", autouse=True)
def fixture_test(request):
    """
    前后置处理
    :return: 
    """
    logs.info("--------------开始测试---------------")
    yield
    logs.info("--------------结束测试---------------")
