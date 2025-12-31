"""
    读取yaml文件
"""
import os
import yaml
import json
from conf.setting import FILE_PATH

class ReadYamlData:
    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = "login.yml"

    def write_yaml_data(self, value):
        """
        写入数据到yaml文件
        :param value: dict 写入的数据
        :return:
        """
        file = None
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path): # 当文件不存在时
            os.makedirs(os.path.dirname(file_path), exist_ok=True) # 创建目录

        try:
            file = open(file_path, mode='a', encoding='utf-8') # mode = a 模式表示每次登录后都追加重新写一次token值到extract.yaml
            if isinstance(value, dict): # 判断传入的value的值是否为dict数据类型
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False) # yaml.dump写入数据，allow_unicode=True允许使用中文
                file.write(write_data)
            else:
                print("写入到【extract.yaml】的数据必须为字典结构！")
        except Exception as e:
            print(f"写入YAML文件错误: {e}")
        finally:
            if file:
                file.close()


    def get_extract_data(self, node_name,sec_node_name=None):
        """
        读取extract.yaml中的变量值
        :param node_name: yaml中的key值
        :param sec_node_name: 第二层key值
        :return:
        """
        file_path = FILE_PATH['extract']
        if not os.path.exists(file_path):
            print("extract.yaml文件不存在")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write("") # 创建空文件
            print("extract.yaml创建成功")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                extract_data = yaml.safe_load(f)
                if extract_data is None:
                    return None
                if sec_node_name is None:
                    return extract_data.get(node_name) # 使用get方法避免KeyError
                else:
                    if node_name in extract_data:
                        return extract_data[node_name].get(sec_node_name)
                    return None
        except Exception as e:
            print(f"读取extract.yaml错误: {e}")
            return None

    def clear_yaml_data(self):
        with open(FILE_PATH['extract'], 'w') as f:
            f.truncate() #将文件数据清除


def get_testcase_yaml(file):
    """
    获取yaml文件的数据
    :param file: yaml文件的路径
    :return: 返回读取到的数据
    """
    try:
        # 如果文件路径是相对路径，转换为绝对路径
        if not os.path.isabs(file):
            # 获取当前文件的目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 回到项目根目录
            project_root = os.path.dirname(current_dir)
            # 构建完整路径
            file = os.path.join(project_root, file.lstrip('./'))

        print(f"读取YAML文件: {file}")

        if not os.path.exists(file):
            print(f"错误: YAML文件不存在 - {file}")
            return []

        with open(file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data is None:
                print(f"警告: YAML文件为空 - {file}")
                return []
            # 确保返回的是列表
            return yaml_data if isinstance(yaml_data, list) else [yaml_data]
    except Exception as e:
        print(f"读取YAML文件错误: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    # 测试代码
    try:
        # 添加项目根目录到路径
        import sys
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        sys.path.insert(0, project_root)

        from common.sendrequests import SendRequests

        res = get_testcase_yaml('./testcase/login/login.yaml')
        print("返回的实际数据类型：",type(res))
        if res:
            res = res[0] # yaml中的数据为列表，所以以索引的方式提取
            print(f"测试数据: {res}")

            url = res['baseInfo']['url']
            new_url = 'http://127.0.0.1:8787' + url
            method = res['baseInfo']['method']
            data = res['testCase'][0]['data']
            case_name = res['testCase'][0]['case_name']
            name = res['baseInfo']['api_name']

            print(f"请求URL: {new_url}")
            print(f"请求方法: {method}")
            print(f"请求数据: {data}")
            print(f"请求的测试用例名称: {case_name}")
            print(f"请求的接口名称: {name}")

            #这里可以取消注释进行实际测试
            send = SendRequests()
            res2 = send.run_main(name=name,url=new_url,case_name=case_name,header=None,method=method,cookies=None,file=None)
            print(f"响应结果: {res2}")
            print("返回的实际数据类型：",type(res2))
    except Exception as e:
        print(f"测试运行错误: {e}")
        import traceback
        traceback.print_exc()