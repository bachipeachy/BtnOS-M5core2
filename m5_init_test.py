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
from m5_init import M5Init


class M5InitTest(M5Init):
    """ an attempt to test all methods in m5_init.py """

    def __init__(self):

        super(M5InitTest, self).__init__()

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
        [print("{}> {}".format(i+1, sample)) for i, sample in enumerate(self.read_imu())]

    def hall_test(self):

        print("read_hall_sensor ..")
        [print("  {} -> {} {}".format(item[0], item[1][0], item[1][1])) for item in self.read_hall_sensor().items()]

    def cpu_temp_test(self):

        print("read_raw_temp -> {}".format(self.read_raw_temp()))


if __name__ == "__main__":
    """ execute various methods sequentially """

    m5t = M5InitTest()
    
    m5t.parms['essid'] = 'T20'
    m5t.parms['pwd'] = 'stacstac'
    
    print("parms -> {}".format(m5t.parms))

    tests = ["wifi_test",
             "imu_test",
             "hall_test",
             "cpu_temp_test",
             "sdcard_erase_test",
             "hard_reset_test"]
    try:
        for test in tests:
            print("\n    ********** {} **********".format(test))
            func = getattr(m5t, test)
            func()
            print("'{}' completed successfully ..".format(test))
    except Exception as e:
        print(" oops I blew up ..", e)
        m5t.hard_reset()
