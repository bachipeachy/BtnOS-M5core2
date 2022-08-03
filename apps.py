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

from dodl_app import Dodl
from imu_app import Imu
from wifi_app import Wifi


class Apps(Wifi, Dodl, Imu):

    def __init__(self):
        super(Apps, self).__init__()


if __name__ == "__main__":

    ap = Apps()
    ap.m5parms['essid'] = 'TBD'
    ap.m5parms['pwd'] = 'xxxx'
    [print("M5Init parm {}> {} = {}".format(i + 1, k, v)) for i, (k, v) in enumerate(ap.m5parms.items())]

    ap.install_app(('btn_1', 'WiFi'), btn_5='Wifi', btn_6='Scan', btn_7='Clk', btn_8='Wipe')
    ap.install_app(('btn_2', 'IMU'), btn_5='IMU', btn_6='Wait', btn_7='Size', btn_8='CSV')
    ap.install_app(('btn_3', 'DoDl'), btn_5='CLR', btn_6='Pen', btn_7='TBD', btn_8='Wipe')

    ap.home_screen()
    try:
        ap.run_app()
    except Exception as e:
        print("main> oops BtnOS blew up ..", e)
    finally:
        # to reset M5 module -- required for clean restart
        ap.hard_reset()
