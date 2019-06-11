#!-*- coding:utf-8 -*-
from flask import Flask
from setting import *
import random
import socket
import os


app = Flask(__name__)

proxys = ['100;{}'.format(socket.gethostbyname(socket.getfqdn(socket.gethostname())))]
Err = None

# path = os.getcwd() + os.sep + 'docs' + os.sep + 'proxyPool.txt'
try:
    with open(PATH) as f:
        proxys = f.read().strip('\n').split('\n')
except Exception as e:
    Err = str(e)

#随机获取有效性分数大于10的proxy
def get_random_proxy(): return random.choice([i for i in proxys if int(i.split(';')[0])>10])

@app.route('/random')
def get_proxy():
    proxy = get_random_proxy()
    return proxy.split(';')[1]

@app.route('/')
@app.route('/index')
def index():
    if Err:
        res = Err
    else:
        res = 'Hello World'
    return res


if __name__ == '__main__':
    app.run(debug=True)
