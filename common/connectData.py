"""
mysql数据库连接
"""
from idlelib.debugobj import myrepr

from common.recordlog import logs

import pymysql

from conf.operationConfig import OperationConfig

conf = OperationConfig()

class ConnectData:
    """
    链接mysql数据库
    """
    def __init__(self):

        mysql_conf = {
            'host': conf.get_mysql_conf('host'),
            'port': int(conf.get_mysql_conf('port')),
            'user':conf.get_mysql_conf('username'),
            'password': conf.get_mysql_conf('password'),
            'database': conf.get_mysql_conf('database')
        }

    # 链接数据库，使用pymysql
        try:
            self.conn = pymysql.connect(**mysql_conf,charset='utf8')
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor) #cursor=pymysql.cursors.DictCursor将数据库表字段显示，以key-value显示
            logs.info("""成功连接到Mysql数据库
            host：{host}
            port:{port}
            db:{database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def close(self):
        """
        连接完后关闭数据库
        :return:
        """
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()

    def query(self,sql):
        """
         查询数据库
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql) #使用游标去执行传入的sql方法
            self.conn.commit() #提交sql执行到数据库
            res = self.cursor.fetchall() #获取到数据库返回的数据
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.close() # 不管上面的连接是正确还是错误，最终数据库都会被关闭

    def insert(self,sql):
        """
        新增
        :param sql:
        :return:
        """

    def updata(self,sql):
        """
        修改数据库
        :param sql:
        :return:
        """
    def delete(self,sql):
        """
        删除数据库
        :param sql:
        :return:
        """

#调试代码调试代码调试代码调试代码调试代码调试代码调试代码

if __name__ == '__main__':
    connect = ConnectData()
    sql = "select * from tb_vehicle_info limit 5"
    print(connect.query(sql))