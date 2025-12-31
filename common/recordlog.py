import datetime
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler # 按文件大小进行滚动备份
from conf import setting


log_path = setting.FILE_PATH.get('log')
if not os.path.exists(log_path):
    os.mkdir(log_path) #创建log文件

logfile_name = log_path + r'\test.{}.log'.format(time.strftime('%Y%m%d-%H%M%S'))

class RecordLog:
    """
    封装日志 ,打印日志
    """

    def autoput_logging(self):
        """
        获取logger对象
        :return:
        """
        logger = logging.getLogger(__name__) #获取到对应文件名
        #防止打印重复的log日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s'
            )
            #日志输出的指定文件
            fh = RotatingFileHandler(filename=logfile_name,mode='a',maxBytes=5242880,backupCount=7,encoding="utf-8")#maxBytes:控制文件的大小，单位是字节，backupCount：用于控制日志文件的数量
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)

            #在将相应的handler添加到logger
            logger.addHandler(fh)

            #将日志输出到控制台上面
            sh = logging.StreamHandler()
            sh.setLevel(setting.LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)


        return logger

    def handle_overdue_log(self):
        """处理过期日志文件"""
        # 获取系统的当前时间
        now_time = datetime.datetime.now()
        # 日期偏移30天，最多保留30的日志文件，超过自动清理
        offset_date = datetime.timedelta(days=-30)
        # 获取前一天时间戳
        before_date = (now_time + offset_date).timestamp()
        # 找到目录下的文件
        files = os.listdir(log_path)
        for file in files:
            if os.path.splitext(file)[1]:
                filepath = log_path + "\\" + file
                file_create_time = os.path.getctime(filepath)  # 获取文件创建时间,返回时间戳
                # dateArray = datetime.datetime.fromtimestamp(file_createtime) #标准时间格式
                # print(dateArray.strftime("%Y--%m--%d %H:%M:%S"))
                if file_create_time < before_date:
                    os.remove(filepath)
                else:
                    continue

apilog = RecordLog()
logs = apilog.autoput_logging()
