#这里负责实现对于yaml里面所需要的功能
import random

from common.readyaml import ReadYamlData
class DbugTalk:

    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self,data,randoms):
        """
        获取extract.yaml数据，不为0，-1，-2的情况。直接顺序读取key里面的内容数据
        :param data:
        :param randoms:
        :return:
        """
        if randoms not in [0,-1,-2]:
            return data[randoms -1]



    def get_extract_data_list(self,node_name,randoms=None):
        """
        获取到extract.yaml的数据
        :param node_name: extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数值
        :return:
        """
        data = self.read.get_extract_data(node_name) #拿到extract.yaml中的数据
        if randoms is not None: #根据有没有传入randoms的参数进行下面的代码
            randoms = int(randoms) #转化为整形
            data_value = { #定义一个字典
                randoms : self.get_extract_order_data(data,randoms), #循序读取data里面的内容
                0 : random.choice(data), #传入0的话就会随机读取一个商品的id
                -1:','.join(data), #等于-1返回全部数据
                -2:','.join(data).split(',') #等于-2返回处理过的数据
            }
            data = data_value[randoms]
        return data

    def get_extract_data(self,node_name,sec_node_name):
        data = self.read.get_extract_data(node_name,sec_node_name)
        return data


    def md5_params(self,params):
        return 'ABCDEFGHIJK' + str(params)

if __name__ == '__main__':
    debug = DbugTalk()
    print(debug.get_extract_data("product_id",-1))