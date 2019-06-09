from bin.req import *
from bin.func import *

class main():
    def __init__(self):
        self.getProxy = ProxyGet()
        self.checkProxy = ProxyCheck()

    def run(self):
        t_get_start = time.time()
        t_check_start = t_get_start
        self.getProxy.run()
        del_removel()
        while True:
            t_get = time.time()
            t_check = t_get

            if int(t_check-t_check_start) // CHECK_INTERVAL*3600 >= 1:
                self.checkProxy.run()
                del_removel()
                t_check_start = time.time()

            if int(t_get-t_get_start) // GET_INTERVAL*3600>=1:
                self.getProxy.run()
                t_get_start = time.time()

            time.sleep(60*30)



if __name__ == '__main__':
    main = main()
    main.run()