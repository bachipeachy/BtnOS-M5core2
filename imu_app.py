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
        self.imu_accl()

    def tsk_26(self, uid, uidt):
        """ Btn_6 display imu 'gyro' data """

        print("t26> {}:{}".format(uid, uidt))
        self.parms['size'] = 9
        self.imu_gyro()

    def tsk_27(self, uid, uidt):
        """ Btn_7 save 'accl' and 'gyro' data to SDCard """

        print("t27> {}:{}".format(uid, uidt))
        self.imu_save()

    def tsk_28(self, uid, uidt):
        """ Btn_8 'Wipe' erases btn_w space """

        print("t28> {}:{}".format(uid, uidt))
        self.edit('btn_w')

    def imu_accl(self):
        """ display imu 'accl' for parms['size] samples with parms['wait'] milli sec pause """

        hd = ["accl_x", "accl_y", "accl_z", "m/s/s"]
        self.write(hd, xl=[24, 128, 216, 280], yl=[48, 48, 48, 48], fg=self.WHITE)

        [self.write([v['accl']['val'][0], v['accl']['val'][1], v['accl']['val'][2]],
                    xl=[0, 104, 208], yl=[60 + i * 12, 60 + i * 12, 60 + i * 12])
         for i, v in enumerate(self.read_imu())]

        self.write(["ts:" + str(time.time()) + " sec, wait:" + str(str(self.parms['imu_wait'])) +
                    " ms, calib:No"],
                   xl=[0], yl=[188], fg=self.WHITE)

    def imu_gyro(self):
        """ display imu 'gyro' for parms['size] samples with parms['wait'] milli sec pause """
        self.parms['imu_calibrate'] = True
        hd = ["gyro_x", "gyro_y", "gyro_z", "deg/s"]
        self.write(hd, xl=[24, 128, 216, 280], yl=[48, 48, 48, 48], fg=self.YELLOW)

        [self.write([v['gyro']['val'][0], v['gyro']['val'][1], v['gyro']['val'][2]],
                    xl=[0, 104, 208], yl=[60 + i * 12, 60 + i * 12, 60 + i * 12])
         for i, v in enumerate(self.read_imu())]
        self.parms['imu_calibrate'] = False

        self.write(["ts:" + str(time.time()) + " sec, wait:" + str(str(self.parms['imu_wait'])) +
                    " ms, calib:Yes"],
                   xl=[0], yl=[188], fg=self.YELLOW)

    def imu_save(self):
        """ save 'ts', 'accl', 'gyro' and data to SDCard as '/sd/imu_scan.json' """

        fn, stat, gyro_offset = self.imu()
        self.edit('btn_w')
        tx = [('', 'Processing Details'), ("filename:", fn), ("size:", str(stat[0]) + ' bytes'),
              ("timestamp:", stat[-1]), ("gyroCalib:", gyro_offset)]
        for i, v in enumerate(tx):
            self.write([v[0], v[1]], xl=[0, 80], yl=[46 + i * 16, 46 + i * 16])
