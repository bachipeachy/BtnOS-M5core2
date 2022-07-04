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
        """ Btn_5  display imu 'accl' data """

        print("t25> {}:{}".format(uid, uidt))
        self.parms['imu_wait'] = 500
        self.parms['imu_calibrate'] = False
        hd = ["accl_x", "accl_y", "accl_z", "m/s/s"]
        self.imu_data(hd, calib="No")

    def tsk_26(self, uid, uidt):
        """ Btn_6 display imu 'gyro' data """

        print("t26> {}:{}".format(uid, uidt))
        self.parms['size'] = 11
        self.parms['imu_calibrate'] = True
        hd = ["gyro_x", "gyro_y", "gyro_z", "deg/s"]
        self.imu_data(hd, calib="Yes")

    def tsk_27(self, uid, uidt):
        """ Btn_7 save 'accl', 'gyro' & 'temp' data to SDCard json format """

        print("t27> {}:{}".format(uid, uidt))
        fn, stat, gyro_offset = self.imu_json()
        self.imu_fdback(fn, stat, gyro_offset)

    def tsk_28(self, uid, uidt):
        """ Btn_8 save 'accl', 'gyro' & 'temp' data to SDCard csv format """

        print("t28> {}:{}".format(uid, uidt))
        fn, stat, gyro_offset = self.imu_csv()
        self.imu_fdback(fn, stat, gyro_offset)

    def imu_data(self, hd, calib):
        """ display data """

        self.edit('btn_w')
        self.write(hd, xl=[8, 112, 208, 280], yl=[48, 48, 48, 48])

        [self.write([v['gyro']['val'][0], v['gyro']['val'][1], v['gyro']['val'][2]],
                    xl=[0, 104, 208], yl=[60 + i * 12, 60 + i * 12, 60 + i * 12])
         for i, v in enumerate(self.read_imu())]

        self.write(
            ["ts:" + str(time.time()) + " sec, wait:" + str(str(self.parms['imu_wait'])) + " ms, calib:" + calib],
            yl=[184])

    def imu_fdback(self, fn, stat, gyro_offset):
        """ display feedback from action """

        self.edit('btn_w')
        tx = [('', 'Processing Details'), ("filename:", fn), ("size:", str(stat[0]) + ' bytes'),
              ("file_ts:", stat[-1]), ("gyroCalib:", gyro_offset)]
        for i, v in enumerate(tx):
            self.write([v[0], v[1]], xl=[0, 80], yl=[46 + i * 16, 46 + i * 16])
