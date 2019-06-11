import os
import time


LEVEL_MAX = 100
LEVEL_MIN = 0
LEVEL_INIT = 10

PATH = os.getcwd() + os.sep + 'docs' + os.sep + 'proxyPool.txt'

RETRY = 3
PAGES = 3

GET_INTERVAL = 24 #获取proxy间隔 h
CHECK_INTERVAL = 12 #检查proxy有效性间隔 h

