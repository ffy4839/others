import os
from bin.func import *

def read_alls(mode='r'):
    with open(path, mode) as f:
        if f.readable():
            return f.read().strip('\n')

def write_datas(data, mode='a'):
    if isinstance(data,str):
        data = [data]
    for i in data:
        with open(path, mode) as f:
            f.write(i + '\n')
# os.path.dirname(os.getcwd())
path = os.getcwd() + os.path.sep + 'docs'+ os.path.sep +'proxyPool.txt'
print(path)
def del_removel(data=None,reverse=True):
    if not data:
        data = read_alls()
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
    write_datas('',mode='w')
    for i in s:
        write_datas(save_data[i])




if __name__ == '__main__':
    a = del_removel()
