import os
import time


LEVEL_MAX = 100
LEVEL_MIN = 0
LEVEL_INIT = 10

PATH = os.path.dirname(os.getcwd()) + os.path.sep + 'docs'+ os.path.sep +'proxyPool.txt'

RETRY = 3
PAGES = 3

GET_INTERVAL = 24 #获取proxy间隔 h
CHECK_INTERVAL = 12 #检查proxy有效性间隔 h

