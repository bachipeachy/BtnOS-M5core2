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
from btn_os import Bos



class BosTest(Bos):
    """ an attempt to test all methods in class M5Init """

    def __init__(self):

        super(BosTest, self).__init__()

    def hard_reset_test(self):
        """ perform hard reset """
        self.hard_reset()

    def powerdown_test(self):
        self.power_down()

    def sdcard_erase_test(self):
        self.mount_sd()
        f = 'lib'
        print("trying to erase {} if exits ..".format(f))
        self.erase_sd(f)
        self.release_spi2()

    def wifi_test(self):
        if not self.is_wifi_connected():
            self.connect_wifi()
        else:
            print("wifi is already connected ..")
        self.scan_wifi()
        self.disconnect_wifi()

    def imu_test(self):
        print("returns a list of samples as a dict of ts, accl, gyro & temp and corresponding uom")
        self.m5parms['imu_size'] = 1
        [[print("  {} -> {}".format(k, v)) for k, v in sample.items()]
         for sample in self.read_imu()]

    def hall_test(self):
        print("read_hall_sensor ..")
        [print("  {} -> {} {}".format(item[0], item[1][0], item[1][1])) for item in self.read_hall_sensor().items()]

    def cpu_temp_test(self):
        print("read_raw_temp -> {}".format(self.read_raw_temp()))


if __name__ == "__main__":
    """ execute various methods sequentially """

    bt = BosTest()

    bt.m5parms['essid'] = 'TBD'
    bt.m5parms['pwd'] = 'xxxx'
    
    print("m5parms -> {}".format(bt.m5parms))

    tests = ["wifi_test",
             "imu_test",
             "hall_test",
             "cpu_temp_test",
             "sdcard_erase_test"]
    try:
        for test in tests:
            print("\n    ********** M5Init {} **********".format(test))
            func = getattr(bt, test)
            func()
            print("'{}' in M5Init class completed successfully ..".format(test))
    except Exception as e:
        print(" oops M5Init class method blew up ..", e)
        print("PROCEEDING with Bos class methods tests ..")


    bt.home_screen()
    try:
        bt.run_app()
    except Exception as e:
        print("main> oops Bos class method blew up ..", e)
    finally:
        os.hard_reset()
