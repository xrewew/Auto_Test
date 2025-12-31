import os
import sys
import logging
from time import process_time

DIR_Path = os.path.dirname(os.path.dirname(__file__))  #获取当前文件的根目录
sys.path.append(DIR_Path) #添加到环境变量里面去

#log日志的输出级别
LOG_LEVEL = logging.DEBUG #日志输出到文件的级别
STREAM_LOG_LEVEL = logging.DEBUG #输出日志到控制台


#文件路径
FILE_PATH = {
    'extract' : os.path.join(DIR_Path, 'extract.yaml'),
    'conf' : os.path.join(DIR_Path,'conf','config.ini'),
    'log' : os.path.join(DIR_Path,'log','test.log')
}
