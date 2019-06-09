import requests
import json
import time
import random
from run import *
from lxml import etree
from bin.func import *
from fake_useragent import UserAgent
UA = UserAgent()
from multiprocessing import Pool
from threading import Thread
import sys


class ProxyGet():
    def __init__(self):
        self.url_list = []
        self.Err_url_list = []
        self.proxy_list = []

    def run(self):
        urls_list = self.get_req_urls(PAGES)

        for i in urls_list:
            self.get_proxy(i)

        # for i in urls_list:
        #     t = Thread(target=self.get_proxy,args=(i,))
        #     t.start()
        # t.join()

        # pool = Pool()
        # pool.map(self.get_proxy,urls_list)
        # pool.close()
        # pool.join()

        # proxy_list = list(set(self.proxy_list))
        # self.proxy_list = []




    def get_proxy(self,data):

        data = data.split(';')
        parse = 'self.parse_' + data[0]
        url = data[1]
        headers = {
            'User-Agent': UA.random
        }

        try:
            time.sleep(random.randint(100, 200) * 0.01)
            re = requests.get(url, headers)
            if re.status_code == 200:
                res = eval(parse)(re)
                print('{} || {} || {}'.format(get_time(), '获取成功', data))
                # self.proxy_list += res
                try:
                    write_data(res)
                    print("{} || {}".format(get_time(), 'proxy存储成功'))
                except Exception as err:
                    print("{} || {} || {}".format(get_time(), '请求的proxy数据存储失败', err))
        except Exception as e:
            # self.Err_url_list.append(data)
            print('{} || {} || {} || {}\n'.format(get_time(), '获取失败', e, data))
            # print(get_time(),'\n',e,'\n',url,'\n')


    def get_err_list(self):
        return self.Err_url_list

    def get_req_urls(self, pages=5):
        #产生获取proxy列表
        base_url = {
            'kuaidaili': 'https://www.kuaidaili.com/free/inha/{}/'
        }
        req_urls_list = []
        for key in base_url.keys():
            data_func = lambda x: '{name};{url}'.format(name=key,url=base_url[key].format(x))
            req_urls_list += [data_func(i) for i in range(1,pages+1)]
            print(key)
        return req_urls_list



    def parse_kuaidaili(self, response):
        result = etree.HTML(response.text)
        com = '//*[@id="list"]/table/tbody/tr/td[@data-title = "{}"]/text()'
        ip = result.xpath(com.format('IP'))
        port = result.xpath(com.format('PORT'))
        ipport = zip(ip, port)
        func = lambda x:'{};{}:{}'.format(LEVEL_INIT,x[0],x[1])
        return [func(i) for i in ipport]


class ProxyCheck():
    def __init__(self):
        pass

    def run(self):
        proxys = self.get_proxys()

        pool = Pool()
        pool.map(self.get_check,proxys)
        pool.close()
        pool.join()

        # for i in proxys:
        #     self.get_check(i)


    def get_check(self, data, urls='https://www.baidu.com'):
        num = int(data.split(';')[0])
        ipport = data.split(';')[1]
        proxies = {
            'http': ipport,
            'https': ipport,
        }
        headers = {
            'User-Agent': UA.random
        }
        useful = False
        try:
            time.sleep(random.randint(10, 50) * 0.1)
            res = requests.get(url=urls, headers=headers, proxies=proxies)
            if res.status_code == 200:
                # if eval('self.parse_{}'.format(urls.split(';')[0]))(res,ipport):
                if num != LEVEL_MAX:
                    num += 1
                    print('{} || proxy使用成功 || {}'.format(get_time(), ipport))
                    useful = True

        except Exception as e:
            if num != LEVEL_MIN:
                num -= 1
                useful = True
            print("{} || {} || {} || {}".format(get_time(),sys._getframe().f_code.co_name,ipport,e))
        if useful:
            write_data('{};{}'.format(str(num), data.split(';')[1]))
        else:
            print('丢弃：{}'.format(data))
        # self.over_list.append()

    def get_proxys(self):
        data = read_all().strip('\n').split('\n')
        write_data('',mode='w')
        return data

    def parse_httpbin(self,res,ipport):
        data = json.loads(res.text)
        recv_ip = data['origin'].split(',')[0]
        send_ip = ipport.split(':')[0]
        print(recv_ip, send_ip)
        if send_ip == recv_ip:
            return True



if __name__ == '__main__':
    get_proxy_save = ProxyGet()
    get_proxy_save.run()


    # check = ProxyCheck()
    # check.run()
    # check.run()