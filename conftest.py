import pytest
from common.recordlog import logs
from common.readyaml import ReadYamlData
import requests


read = ReadYamlData()

@pytest.fixture(scope="session",autouse=True)
def serverWasNormalOrNot():
    """
    测试服务器是否可达
    :return:
    """
    try:
        # 测试GET请求看看服务器是否运行
        test_resp = requests.get("http://127.0.0.1:8787", timeout=5)
        print(f"服务器可达，状态码: {test_resp.status_code}")
    except:
        print("警告: 无法连接到服务器 http://127.0.0.1:8787")

#启动测试之前进行清除yaml数据
@pytest.fixture(scope='session',autouse=True)
def clear_yaml_data():
    read.clear_yaml_data()

# 每个测试用例执行前后进行日志记录
@pytest.fixture(scope="session", autouse=True)
def fixture_test(request):
    """
    前后置处理
    :return: 
    """
    logs.info("--------------开始测试---------------")
    yield
    logs.info("--------------结束测试---------------")


# 测试服务器是否可达
if __name__ == "__main__":
    serverWasNormalOrNot()
