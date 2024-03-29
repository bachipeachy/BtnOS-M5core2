"""
The MIT License (MIT)

Copyright (c) 2022 bachipeachy@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import time

from btn_os import Bos


class Imu(Bos):

    def __init__(self, **kwargs):
        """ inherit all BtnOS methods and properties """
        super(Imu, self).__init__(**kwargs)

    def app_2(self, uid, x, y):
        """ 'IMU' app invoked by Btn_2 shows output on btn_w space """
        print("a2> {} x:{} y:{}".format(uid, x, y))
        

    def tsk_25(self, uid, uidt):
        """ Btn_5  display imu 'accl' and 'gyro' data alternately """
        print("t25> {}:{} -> {}:{}".format(uid, self.btns[uid]['lbl'], uidt, self.tbtn2[uidt]['lbl']))
        if self.ctx['tbtn']:
            self.edit(uidt, lbl='Accl')
            data = 'accl'
            hd = ["accl_x", "accl_y", "accl_z", "mG"]
            self.imu_data(data, hd)
            self.ctx['tbtn'] = False
        else:
            self.edit(uidt, lbl='Gyro')
            data = 'gyro'
            hd = ["gyro_x", "gyro_y", "gyro_z", "deg/s"]
            self.imu_data(data, hd)
            self.ctx['tbtn'] = True

    def tsk_26(self, uid, uidt):
        """ Btn_6 sets imu sampling imu_wait time """
        print("t26> {}:{}".format(uid, uidt))
        imu_wait = self.set_imu_parm('btn_6', 'imu_wait')
        print("t26> set imu sampling imu_size {}".format(imu_wait))
        return imu_wait

    def tsk_27(self, uid, uidt):
        """ Btn_7 sets imu sampling imu_size """
        print("t27> {}:{}".format(uid, uidt))
        imu_size = self.set_imu_parm('btn_7', 'imu_size')
        print("t27> set imu sampling imu_size {}".format(imu_size))
        return imu_size

    def tsk_28(self, uid, uidt):
        """ Btn_8 save 'accl', 'gyro' & 'temp' data to SDCard csv format """
        print("t28> {}:{}".format(uid, uidt))
        self.edit('btn_w')
        self.write(["saving", self.m5parms['imu_size'], "samples every", self.m5parms['imu_wait'], "ms"],
                   xl=[0, 56, 96, 208, 248], yl=[184, 184, 184, 184, 184])
        fn, stat = self.imu_csv()
        self.imu_fdback(fn, stat)

    def imu_data(self, data, hd):
        """ display data """
        self.edit('btn_w')
        self.write(hd, xl=[8, 112, 208, 280], yl=[48, 48, 48, 48])
        [self.write([v[data]['val'][0], v[data]['val'][1], v[data]['val'][2]],
                    xl=[0, 104, 208], yl=[60 + i * 12, 60 + i * 12, 60 + i * 12])
         for i, v in enumerate(self.read_imu()) if i < 10]

        self.write(["ts:" + str(time.time()) + " sec, wait:" + str(str(self.m5parms['imu_wait'])) +
                    "ms, size:" + str(self.m5parms['imu_size'])], yl=[184])

    def imu_fdback(self, fn, stat):
        """ display feedback from action """
        self.edit('btn_w')
        tx = [('', 'Processing Details'), ("filename:", fn), ("imu_size:", str(stat[0]) + ' bytes'),
              ("file_ts:", stat[-1]), ("imu_wait:", self.m5parms['imu_wait']), ("imu_size:", self.m5parms['imu_size'])]
        for i, v in enumerate(tx):
            self.write([v[0], v[1]], xl=[0, 80], yl=[46 + i * 16, 46 + i * 16])
