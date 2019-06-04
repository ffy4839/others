import serial
import configparser
import os
import binascii
import sys
import re
import time
import threading
import serial.tools.list_ports as LP


def get_config(sections):
    data = {}
    config = configparser.ConfigParser()
    path = os.getcwd() + os.path.sep
    if 'setConfig.ini' in os.listdir(path):
        config.read(path + 'setConfig.ini', encoding='UTF-8')
        for i in config.items(section=sections):
            data[i[0]] = i[1]
        return data

    else:
        config['configs'] = {}
        config['configs']['baudrate'] = '9600'
        config['configs']['frozen_hour'] = '24'
        config['configs']['frozen_day'] = '3'
        config['configs']['frozen_month'] = '2'
        config['configs']['interval'] = '20'
        config['configs']['month_frozen_day'] = 'false'

        with open(path + 'setConfig.ini', 'w') as f:
            config.write(f)
        input('创建成功')
        sys.exit()


config_data = get_config('configs')

BAUDRATE = int(config_data['baudrate'])  # 波特率

FROZEN_HOUR_TIMES = int(config_data['frozen_hour'])  # 小时冻结次数
FROZEN_DAY_TIMES = int(config_data['frozen_day'])  # 天冻结次数
FROZEN_MONTH_TIME = int(config_data['frozen_month'])  # 月冻结次数

INTERVAL = int(config_data['interval'])              # 两次设置间隔
MONTH_FROZEN_DAY = config_data['month_frozen_day']   # 月冻结时间

PATH = os.getcwd() + os.path.sep + '运行记录.txt'

def choose_port():
    s = lambda x:str(x).split('-')[0].strip(' ').upper()
    pl = list(LP.comports())

    port_list = [s(i) for i in pl]
    nb_port_list = [s(i)[3:] for i in pl]

    port_in = input('{}\n输入端口号：'.format(str(port_list)[1:-1].replace("'",''))).upper()

    if port_in in port_list:
        return port_in

    elif port_in in nb_port_list:
        return 'com' + port_in

    else:
        print('串口输入错误，请重新输入\n')

def save(data):
    '''数据存储'''
    try:
        with open(PATH, 'a') as f:
            f.write(data)
            f.write('\n')
    except Exception as e:
        print('{},存储失败'.format(e))


def quit():
    input('按任意键退出')
    sys.exit()


def timen(d='%Y-%m-%d,%H:%M:%S'):
    return time.strftime(d, time.localtime(time.time()))


class ser(serial.Serial):
    def __init__(self,port):
        super(ser, self).__init__()
        self.port = port
        self.open_ser()

    def open_ser(self):

        self.baudrate = BAUDRATE
        self.timeout = 0.5
        self.open()

    def send(self, data):
        '''串口发送数据'''
        data = binascii.unhexlify(data)
        if self.is_open:
            try:
                self.flushOutput()
                self.write(data)
            except Exception as e:
                print('{};{},串口发送错误'.format(timen(), e))
                quit()
        else:
            self.open_ser()

    def recv(self, times=6):
        self.isopened()
        self.flushInput()
        for i in range(times):
            inwaiting = self.in_waiting
            if inwaiting:
                recv = self.read_all()
                return self.recv_parse(recv)
            time.sleep(1)

    def recv_parse(self, data):
        try:
            datas = binascii.hexlify(data).decode('utf-8').upper()

            re_com = re.compile('68.*16')
            datas = re.findall(re_com, datas)[0]

        except:
            try:
                datas = data.decode('ascii')
            except:
                datas = data
        return datas

    def sopen(self):
        if not self.is_open:
            self.open()

    def sclose_ser(self):
        if self.is_open:
            self.close()

    def isclosed(self):
        if self.is_open:
            self.close()

    def isopened(self):
        if not self.is_open:
            self.open()


class pro():
    def __init__(self):
        self.pro = self.initinput()

    def initinput(self):
        xuanze = input('{}\n{}\n{}\n{}'.format(
            '1、民用物联网', '2、商业物联网', '3、自定义', '输入序号选择：'))

        if xuanze == '1':
            ts = '190313010203'
            inp_a = '68 00 00 00 01 00 00 68 04 10 00 {} 16 21 C6 00 {} 3F 16'.format(
                timen('%y%m%d%H%M%S'), ts).replace(' ', '')
            inp_b = ts
        elif xuanze == '2':
            ts = '190313010203'
            inp_a = '68 FF FF FF FF FF FF 68 04 10 00 {} 02 03 AA 00 {} CF 16'.format(
                timen('%y%m%d%H%M%S'), ts).replace(' ', '')
            inp_b = ts
        else:
            inp_a = input('输入发送帧部分：').replace(' ', '')
            inp_b = input('输入帧时间部分：').replace(' ', '')
        try:
            coordinate_set = re.search(inp_b, inp_a).span()
        except:
            coordinate_set = None
        timenow = timen('%y%m%d%H')
        try:
            cc = re.compile(timenow + '.{4}')
            coordinate_time = re.search(cc, inp_a).span()
        except:
            coordinate_time = (0, 0)
        try:
            part_1 = inp_a[:coordinate_time[0]]
            part_2 = inp_a[coordinate_time[1]:coordinate_set[0]]
            part_3 = inp_a[coordinate_set[1]:-4]
            return part_1, part_2, part_3
        except:
            print('数据输入错误,即将退出程序', end='')
            for i in range(5):
                print('.', end='', flush=True)
                time.sleep(1)
            sys.exit()

    def run(self, settime):
        part_1 = self.pro[0]
        part_2 = self.pro[1]
        part_3 = self.pro[2]

        timenow = timen('%y%m%d%H%M%S')
        part = part_1 + timenow + part_2 + settime + part_3
        data = part + self.checkSum(part) + '16'
        return data.upper()

    def checkSum(self, data):
        data = data.replace(' ', '')
        check = 0x00
        L = len(data)
        for i in range(0, L, 2):
            check = int(data[i:(i + 2)], 16) + check
            if check > 0xff:
                check -= 0x100
        check_hex = hex(check)[2:]
        return ('0' * (2 - len(check_hex)) + check_hex).upper()


class setTimeList():
    def __init__(self):
        self.set_struct = '5955'
        self.last_time_list = []

    def run(self, th, td, tm):
        set_time_list = []
        self.creat_formerly_time_list(15)

        time_list = self.last_time_list
        if th:
            while True:
                if th == 0:
                    break
                set_time_list.append(time_list.pop())
                th -= 1
        if td:
            while True:
                if td == 0:
                    break
                get_time = time_list.pop()
                if '23' + self.set_struct in get_time:
                    set_time_list.append(get_time)
                    td -= 1
        if tm:
            while True:
                if tm == 0:
                    break
                # print(len(time_list),tm)
                get_time = time_list.pop()
                get_time_mdh = get_time[2:8]
                get_time_y = '20' + get_time[0:2]

                mdh_list =self.deal_with_month_frozen(get_time_y)

                if get_time_mdh in mdh_list:
                    set_time_list.append(get_time)
                    tm-=1

        self.result = set_time_list
        return set_time_list

    def deal_with_month_frozen(self,mtime):
        frozen_day = MONTH_FROZEN_DAY
        if frozen_day == '' or frozen_day == 'false' or len(frozen_day) != 6:
            mdh_list = ('013123','022823','033123','043023','053123','063023','073123','083123','093023','103123','113023','123123')
            mdh_list_1 = ('013123','022923','033123','043023','053123','063023','073123','083123','093023','103123','113023','123123')
            if not int(mtime) % 4 and int(mtime) % 100 or not int(mtime) % 400:
                mdh_list = mdh_list_1
        else:
            mdh_list = []
            str_frozen = timen('%y%m') + frozen_day + '00'
            stamp_frozen = self.str_time2stamp_time(str_frozen) - 5
            str_frozen_last = self.stamp_time2str_time(stamp_frozen,'%d')
            for i in range(1,13):
                add_data = str(i).rjust(2,'0') + str_frozen_last + '23'
                mdh_list.append(add_data)
        return mdh_list


    def creat_formerly_time_list(self, years=12):
        # 创建12年零点
        struct = self.set_struct
        now_time = self.get_now_time()
        now_time = now_time[:8] + struct

        n = years * 365 * 24
        while n:
            self.last_time_list.append(now_time)
            self.last_hour(now_time)
            now_time = self.last_hour(now_time)
            n -= 1

        self.last_time_list.reverse()

    def last_hour(self, intime_str):
        # 获取上一个小时的时间点
        stamptime = self.str_time2stamp_time(intime_str)
        last_stamptime = stamptime - 60 * 60
        outtime_str = self.stamp_time2str_time(last_stamptime)
        # print(outtime_str)
        return outtime_str

    def str_time2stamp_time(self, strtime, struct='%y%m%d%H%M%S'):
        # 将格式化时间转为时间戳
        return time.mktime(time.strptime(strtime, struct))

    def stamp_time2str_time(self, stamptime, struct='%y%m%d%H%M%S'):
        # 将时间戳转为格式化时间
        return time.strftime(struct, time.localtime(stamptime))

    def get_now_time(self, struct='%y%m%d%H%M%S'):
        return time.strftime(struct, time.localtime(time.time()))


class main():
    def __init__(self):

        # self.addtime = addtime()
        self.timeset = setTimeList()
        self.times_n = 0
        self.times_sum = 0
        self.send_time = time.time()
        self.recv_time = time.time()

    def run(self):

        p = threading.Thread(target=self.timeset.run, args=(FROZEN_HOUR_TIMES,
                                                            FROZEN_DAY_TIMES,
                                                            FROZEN_MONTH_TIME))

        p.start()
        while True:
            PORT = choose_port()  # 串口
            if PORT:
                break
        self.ser = ser(PORT)
        self.pro = pro()

        p.join()
        # print(time.time()-xxx)
        time_list = self.timeset.result
        # print(len(time_list))
        #print(time_list)

        self.print_save('\n起始时间：{}，停止时间:{}\n'.format(self.parse_struct_time(
            time_list[-1]), self.parse_struct_time(time_list[0])))

        lasttime = 0

        while True:
            nowtime = time.time()

            if len(time_list) == 0:
                break
            get_time = time_list.pop()  # 本次设置的时间
            p_get_time = self.print_get_time(get_time)  # 格式化本次设置的时间用于打印
            data = self.pro.run(get_time)  # 数据帧
            self.ser.send(data)  # 串口发送
            ll = len(time_list)  # 剩余次数

            sysj = self.shengyushijian(ll, nowtime, lasttime)  # 预计剩余时间
            lasttime = nowtime

            self.print_data(ll, p_get_time, sysj, data)  # 打印存储数据
            self.send_time = time.time()
            self.wait_recv()  # 等待接收

        print('运行结束')
        quit()

    def print_save(self, data):
        print(data)
        save(data)

    def print_data(self, ll, p_get_time, sysj, data):
        p_datas = '剩余次数：{a}, 设置的时间：{b}\n预计剩余时间：{c}\n[{d}], 发送: {e}'.format(
            a=str(ll), b=p_get_time, c=sysj, d=timen(), e=data)
        self.print_save(p_datas)

    def print_get_time(self, x):
        try:
            xs = '20{}-{}-{},{}:{}:{}'.format(
                x[0:2],
                x[2:4],
                x[4:6],
                x[6:8],
                x[8:10],
                x[10:12]
            )
            return xs
        except:
            return '计算错误'

    def shengyushijian(self, data, nowtime, lasttime):
        if lasttime == 0:
            return self.parse_time(data * INTERVAL)
        times = nowtime - lasttime
        self.times_sum += times
        self.times_n += 1
        xx = int(self.times_sum / self.times_n)
        x = self.parse_time(data * xx)
        return x

    def parse_struct_time(self, data):
        return time.strftime('%Y-%m-%d,%H:%M:%S', time.strptime(data, '%y%m%d%H%M%S'))

    def parse_time(self, data):
        data = int(data)
        # d = int(data/3600/24)
        h = str(int(data / 3600))
        m = str(int(data % 3600 / 60))
        s = str(int(data % 3600 % 60))

        return '{}时,{}分,{}秒'.format(h, m, s)

    def wait_recv(self):
        recv = ''
        data = self.ser.recv()
        recv = '[{}], 接收: {}\n'.format(timen(), data)
        print(recv)
        save(recv)
        self.recv_time = time.time()
        time.sleep(INTERVAL - (self.recv_time - self.send_time))

if __name__ == '__main__':
    try:
        m = main()
        m.run()
    except Exception as e:
        print(e)
        time.sleep(60)
