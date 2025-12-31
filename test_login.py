import pytest
import requests

@pytest.mark.skip
def test_user_login():
    print("开始测试登录...")

    # 先测试服务器是否可达
    try:
        # 测试GET请求看看服务器是否运行
        test_resp = requests.get("http://127.0.0.1:8787", timeout=5)
        print(f"服务器可达，状态码: {test_resp.status_code}")
    except:
        print("警告: 无法连接到服务器 http://127.0.0.1:8787")

    # 执行登录请求
    try:
        resp = requests.post(  # 使用post方法更简洁
            url="http://127.0.0.1:8787/dar/user/login",
            data={"user_name": "test01", "password": "admin123"},
            headers={"Content-Type": "application/x-www-formurlencoded;charset=UTF-8 "},
            timeout=10
        )

        print(f"\n登录请求结果:")
        print(f"状态码: {resp.status_code}")
        print(f"响应内容长度: {len(resp.text)} 字符")

        if resp.text:
            print("响应内容:")
            print("-" * 50)
            print(resp.text)
            print("-" * 50)
        else:
            print("响应内容为空！")

    except Exception as e:
        print(f"请求失败: {e}")
