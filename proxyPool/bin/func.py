
from setting import *


def get_time(st = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(st,time.localtime(time.time()))

def write_data(data, mode='a'):
    if isinstance(data,str):
        data = [data]
    for i in data:
        with open(PATH, mode) as f:
            f.write(i + '\n')

def read_all(mode='r'):
    with open(PATH, mode) as f:
        if f.readable():
            return f.read().strip('\n')

def del_removel(data=None,reverse=True):
    if not data:
        data = read_all()
        data_list = list(set(data.strip('\n').split('\n')))
    elif isinstance(data,str):
        data_list = list(set(data.strip('\n').split('\n')))
    else:
        data_list = data
    data_dict = {}
    for i in data_list:
        num = i.split(';')[0]
        ip = i.split(';')[1]
        if ip in data_dict.keys():
            if int(num) <= int(data_dict[ip]):
                num = data_dict[ip]
        data_dict[ip] = num
    save_data = {}
    for key, value in data_dict.items():
        if value not in save_data.keys():
            save_data[value] = ['{};{}'.format(value,key)]
        else:
            save_data[value].append('{};{}'.format(value,key))
    func = lambda x:int(x)
    s = list(save_data.keys())
    s.sort(key=func,reverse=True)
    write_data('',mode='w')
    for i in s:
        write_data(save_data[i])

# def del_removel_check():
#     # str2list
#     data = read_all()
#     if isinstance(data, str):
#         data = data.strip('\n').split('\n')
#     # 根据nums排序
#     func = lambda x: int(x.split(';')[0])
#     data.sort(key=func, reverse=True)
#     # 去重
#     data = list(set(data))
#     data_ip = [i.split(';')[1] for i in data]
#     nums = [data_ip.index(i) for i in list(set(data_ip))]
#     data = [data[i] for i in nums]
#     # 根据nums排序
#     data.sort(key=func, reverse=True)
#     return data

if __name__ == '__main__':
    print(get_time())