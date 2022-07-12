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

import errno
import json
import time

import ili9342c
import network
import uos
from esp32 import raw_temperature, hall_sensor
from machine import SoftI2C, Pin, SPI, soft_reset, reset

import axp202c
import vga1_16x16 as font16
import vga1_8x8 as font8
from focaltouch import FocalTouch
from mpu6886 import MPU6886, SF_DEG_S
from sdcard import SDCard


class M5Init:

    def __init__(self):
        """ auto start power up and tft services """

        self._parms = {'essid': None, 'pwd': None, 'mdir': '/sd', 'imu_wait': 0, 'imu_size': 0,
                       'json_file': '/imu.json', 'csv_file': '/imu.csv'}

        self.BLACK = ili9342c.BLACK
        self.BLUE = ili9342c.BLUE
        self.RED = ili9342c.RED
        self.GREEN = ili9342c.GREEN
        self.CYAN = ili9342c.CYAN
        self.MAGENTA = ili9342c.MAGENTA
        self.YELLOW = ili9342c.YELLOW
        self.WHITE = ili9342c.WHITE

        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.axp = self.power_up()
        self.spi2 = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(38))
        self.sensor = MPU6886(self.i2c, gyro_sf=SF_DEG_S)
        self.tft = self.enable_tft()

        self.greet()
        print("* M5Stack Core2 initialization complete")

    @property
    def parms(self):
        return self._parms

    @parms.setter
    def parms(self, value):
        self._parms = value

    def power_up(self):
        """ turn on M5Stack Core2 """

        axp = axp202c.PMU(i2c=self.i2c, address=0x34)
        axp.enablePower(axp202c.AXP192_LDO2)
        axp.setDC3Voltage(3000)
        print("* M5Core2 powered up")
        return axp

    @staticmethod
    def soft_reset():
        print("* soft reset")
        soft_reset()

    @staticmethod
    def hard_reset():
        print("* hard reset")
        reset()

    def power_down(self):
        """ turn off M5Stack Core2 """

        print("* M5Core2 shutting it down ..")
        time.sleep(2)
        self.axp.shutdown()

    def enable_tft(self):
        """ initialize tft function for display """

        tft = ili9342c.ILI9342C(
            self.spi2,
            320, 240,
            reset=Pin(33, Pin.OUT),
            cs=Pin(5, Pin.OUT),
            dc=Pin(15, Pin.OUT),
            rotation=0)
        tft.init()
        print("* tft display enabled")
        return tft

    def mount_sd(self):
        """ mount the sdcard """
        try:
            sdc = SDCard()
            vfs = uos.VfsFat(sdc)
            uos.mount(vfs, self.parms['mdir'])
            print("* Flash Memory root level listing -> {}\nSDCard root files {} -> {}".format(
                uos.listdir(), self.parms['mdir'], uos.listdir(self.parms['mdir'])))
        except OSError as e:
            if e.errno == errno.EPERM:
                print("{} already mounted".format(self.parms['mdir']))
        except Exception as e:
            print("ERROR: {}".format(e))

    def release_spi2(self):
        """ release spi channel for sharing """

        self.spi2.deinit()
        self.spi2.init()
        print("* released spi2")

    def greet(self):
        """ test initialization """

        self.tft.text(font16, "M5Core2> initialized!", 0, 0, ili9342c.WHITE, ili9342c.BLACK)

    @staticmethod
    def is_wifi_connected():
        """ returns True or False of wifi connection status """

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        print("* wifi connection active -> {}".format(wlan.isconnected()))
        return wlan.isconnected()

    def connect_wifi(self):
        """ connect wifi if disconnected """

        wlan = network.WLAN(network.STA_IF)
        t1 = time.time()
        run = True
        wlan.active(True)
        i = 15
        if not wlan.isconnected():
            print("* connecting to wireless '{}' with {} sec timeout ...".format(self.parms['essid'], i))

            try:
                wlan.connect(self.parms['essid'], self.parms['pwd'])
            except Exception as e:
                print("ERROR: {} .. check or missing/wrong essid/pwd info\nStand by ..".format(e))

            while not wlan.isconnected() and run:
                if (time.time() - t1) > i:
                    run = False
        else:
            print("* wifi connection active -> {}".format(wlan.ifconfig()[0]))
            return wlan.ifconfig()[0]

        if run:
            print("* wifi connection established -> {}".format(wlan.ifconfig()[0]))
        else:
            print("* unable to connect to SSID-> '{}'".format(self.parms['essid']))
        return wlan.ifconfig()[0]

    @staticmethod
    def disconnect_wifi():
        """ disconnect wifi if connected """

        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        print("* wifi disconnected -> {}".format(wlan.ifconfig()[0]))
        return wlan.ifconfig()[0]

    @staticmethod
    def scan_wifi():
        """ scan wlan to extract ssid and RSSI """
        """
        wifi list will have 2 of 6 tuples -- 'ssid, bssid, ch, RSSI, auth and hidden'
        # RSSI - Received Signal Strength Indicator
        Excellent -33 to -67  4 bars green
        Good      -67 to -70  3 bars blue
        OK        -70 to -80  2 bars yellow
        Bad       -80 to -90   1 bar  red
        """

        bar4 = -67
        bar3 = -78
        bar2 = 80

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        print("* scanning wifi ..")
        vals = wlan.scan()

        lines = []
        for i, v in enumerate(vals):
            ssid = v[0]
            rssi = v[3]
            if rssi >= bar4:
                bars = 4
            elif rssi >= bar3:
                bars = 3
            elif rssi >= bar2:
                bars = 2
            else:
                bars = 1
            lines.append((ssid, rssi, bars))

        print("* wifi scanned {} essid's".format(len(lines)))
        return lines

    def read_imu(self):
        """  returns a list of samples as a dict of ts, accl, gyro & temp and corresponding uom """

        imu = []
        print("* gyro_offset -> {}".format(self.sensor.calibrate()))

        for i in range(self.parms['imu_size']):
            imu.append({'ts': {'val': int(str(time.time_ns())[:-6]), 'uom': 'ms'},
                        'accl': {'val': self.sensor.acceleration, 'uom': 'm/s/s'},
                        'gyro': {'val': self.sensor.gyro, 'uom': 'deg/s'},
                        'temp': {'val': round(self.sensor.temperature * 1.8 + 32, 1), 'uom': 'F'}})
            time.sleep_ms(self.parms['imu_wait'])
        return imu

    @staticmethod
    def read_hall_sensor():
        """  returns a dict  of timestamp, 3d-readings and their uom """
        hs_val = {'ts': [time.time_ns(), 'ns'],
                  'hs': [hall_sensor(), 'micTes']}
        return hs_val

    @staticmethod
    def read_raw_temp():
        """  returns raw CPU temperature in def F """
        return round(raw_temperature(), 1)

    def erase_sd(self, path):
        """" on SDCard erase files and empty directories one at time """

        try:
            print("* contents in sdcard before erase {} -> {}".format(
                self.parms['mdir'], uos.listdir(self.parms['mdir'])))

        except Exception as e:
            print("ERROR: {}".format(e))

        if path[0] != '/':
            path = '/' + path

        try:
            uos.remove(self.parms['mdir'] + path)
            print("* success removed'{}'".format(self.parms['mdir'] + path))
            print("* contents in sdcard after erase {} -> {}".format(
                self.parms['mdir'], uos.listdir(self.parms['mdir'])))

        except OSError as e:
            if e.errno == errno.ENOENT:
                print("ERRPR: {} erase failed did not find '{}'".format(e, self.parms['mdir'] + path))
            else:
                print("* checking if path '{}' is a dir".format(path))
            if e.errno == errno.EISDIR:
                try:
                    ct = len([f for f in uos.listdir(self.parms['mdir'] + path)])
                    if ct == 0:
                        uos.rmdir(self.parms['mdir'] + path)
                        print("* success removed empty dir {}".format(self.parms['mdir'] + path))
                        print("* contents in sdcard after erase {} -> {}".format(
                            self.parms['mdir'], uos.listdir(self.parms['mdir'])))
                    else:
                        print("{}: dir '{}' is not empty has {} entry -> {}".format(
                            e, self.parms['mdir'] + path, ct, uos.listdir(self.parms['mdir'] + path)))
                except Exception as e:
                    print("ERROR: {}".format(e))
            else:
                pass

        except Exception as e:
            print("ERROR: {}".format(e))


class Bos(M5Init):

    def __init__(self):
        """ run app forever until hardware btn_c is 'HELD' for hard reset or haedware btn_a 'HELD' for power down """

        super(Bos, self).__init__()

        self.color = (self.WHITE, self.BLUE, self.RED, self.GREEN,
                      self.CYAN, self.MAGENTA, self.YELLOW, self.BLACK)

        self.loc_a = (0, 240, 107, 40)
        self.loc_b = (107, 240, 107, 40)
        self.loc_c = (214, 240, 106, 40)

        self.loc_t = (0, 0, 320, 40)
        self.loc_w = (0, 40, 320, 160, 40)

        self.loc_1 = (0, 200, 80, 40)
        self.loc_2 = (80, 200, 80, 40)
        self.loc_3 = (160, 200, 80, 40)
        self.loc_4 = (240, 200, 80, 40)

        self.loc_5 = (0, 0, 80, 40)
        self.loc_6 = (80, 0, 80, 40)
        self.loc_7 = (160, 0, 80, 40)
        self.loc_8 = (240, 0, 80, 40)

        self.btns = None
        self._abtns = {'btn_1': {'loc': self.loc_1, 'lbl': 'App1', 'border': self.MAGENTA, 'fg': self.YELLOW,
                                 'bg': self.BLACK, 'fill': True, 'font': font16},
                       'btn_2': {'loc': self.loc_2, 'lbl': 'App2', 'border': self.MAGENTA, 'fg': self.YELLOW,
                                 'bg': self.BLACK, 'fill': True, 'font': font16},
                       'btn_3': {'loc': self.loc_3, 'lbl': 'App3', 'border': self.MAGENTA, 'fg': self.YELLOW,
                                 'bg': self.BLACK, 'fill': True, 'font': font16},
                       'btn_4': {'loc': self.loc_4, 'lbl': 'App4', 'border': self.MAGENTA, 'fg': self.YELLOW,
                                 'bg': self.BLACK, 'fill': True, 'font': font16}}
        self._tbtn1 = {
            'btn_5': {'loc': self.loc_5, 'lbl': 'Btn5', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_6': {'loc': self.loc_6, 'lbl': 'Btn6', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_7': {'loc': self.loc_7, 'lbl': 'Btn7', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_8': {'loc': self.loc_8, 'lbl': 'Btn8', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16}}
        self._tbtn2 = {
            'btn_5': {'loc': self.loc_5, 'lbl': 'Btn5', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_6': {'loc': self.loc_6, 'lbl': 'Btn6', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_7': {'loc': self.loc_7, 'lbl': 'Btn7', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_8': {'loc': self.loc_8, 'lbl': 'Btn8', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16}}
        self._tbtn3 = {
            'btn_5': {'loc': self.loc_5, 'lbl': 'Btn5', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_6': {'loc': self.loc_6, 'lbl': 'Btn6', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_7': {'loc': self.loc_7, 'lbl': 'Btn7', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_8': {'loc': self.loc_8, 'lbl': 'Btn8', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16}}
        self._tbtn4 = {
            'btn_5': {'loc': self.loc_5, 'lbl': 'Btn5', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_6': {'loc': self.loc_6, 'lbl': 'Btn6', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_7': {'loc': self.loc_7, 'lbl': 'Btn7', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16},
            'btn_8': {'loc': self.loc_8, 'lbl': 'Btn8', 'border': self.MAGENTA, 'fg': self.YELLOW, 'bg': self.BLACK,
                      'fill': True, 'font': font16}}
        self.touch = None

        self.ctx = dict(btn=True, tbtn=True, pallet=-1, pen=0)

    @property
    def abtns(self):
        return self._abtns

    @abtns.setter
    def abtns(self, value):
        self._abtns = value

    @property
    def tbtn1(self):
        return self._tbtn1

    @tbtn1.setter
    def tbtn1(self, value):
        self._tbtn1 = value

    @property
    def tbtn2(self):
        return self._tbtn2

    @tbtn2.setter
    def tbtn2(self, value):
        self._tbtn2 = value

    @property
    def tbtn3(self):
        return self._tbtn3

    @tbtn3.setter
    def tbtn3(self, value):
        self._tbtn3 = value

    @property
    def tbtn4(self):
        return self._tbtn4

    @tbtn4.setter
    def tbtn4(self, value):
        self._tbtn4 = value

    def define_btns(self):
        btns = {'btn_a': {'loc': self.loc_a}, 'btn_b': {'loc': self.loc_b}, 'btn_c': {'loc': self.loc_c},
                'btn_w': {'loc': self.loc_w, 'lbl': '', 'border': self.BLACK, 'fg': self.WHITE, 'bg': self.BLACK,
                          'fill': True, 'font': font16},
                'btn_t': {'loc': self.loc_t, 'lbl': self.clock()['dt'], 'border': self.BLACK, 'fg': self.YELLOW,
                          'bg': self.BLACK, 'fill': True, 'font': font16}}
        return btns

    def enable_touch(self):
        """ enable touch with current btns passed as parm """

        touch = FocalTouch(self.i2c, self.btns)
        return touch

    def install_app(self, app, **kwargs):

        if app[0] in self.abtns.keys():
            self.abtns[app[0]]['lbl'] = app[1]
            tbtn = getattr(self, 'tbtn' + app[0][-1])
            for k, v in kwargs.items():
                if k in tbtn.keys():
                    tbtn[k]['lbl'] = v
                else:
                    print("Error parm '{}' not in btn_5 thro' btn_8 ".format(k))
                    self.hard_reset()
        else:
            print("Error parm '{}' not in btn_1 thro' btn_4 ".format(app[0]))
            self.hard_reset()

    def home_screen(self):

        self.btns = self.define_btns()
        self.btns.update(self.abtns)
        self.edit('btn_w')
        self.home_splash()
        [self.paint(k, v) for k, v in self.btns.items() if k not in ['btn_w', 'btn_a', 'btn_b', 'btn_c']]
        self.touch = self.enable_touch()

    def home_splash(self):

        self.tft.rect(8, 48, 304, 144, self.WHITE)
        self.write(tl=["BtnOS"], font=font16, xl=[120], yl=[80])
        self.write(tl=["(c) bachipeachy"], xl=[96], yl=[104])
        self.write(tl=["version 5"], xl=[124], yl=[120])
        self.write(tl=["btn_a", "btn_b", "btn_c"], xl=[30, 140, 260], yl=[152, 152, 152], fg=self.YELLOW)
        self.write(tl=["shutdown", "homescreen", "rerun"], xl=[18, 120, 260], yl=[164, 164, 164])
        self.write(['O', 'O', 'O'], xl=[40, 152, 272], yl=[172, 172, 172], font=font16, fg=self.RED)

    def app_screen(self, uid, tbtn):

        saved_lbl = None
        [self.btns.pop(k) for k in self.btns.keys() if k not in (uid, 'btn_w', 'btn_a', 'btn_b', 'btn_c')]
        if uid in ('btn_1', 'btn_2', 'btn_3', 'btn_4'):
            saved_lbl = self.btns[uid]['lbl']
        self.btns.update(tbtn)
        self.edit(uid, lbl='QUIT', bg=self.RED)
        self.edit('btn_w')
        [self.paint(k, v) for k, v in self.btns.items() if k not in ['btn_a', 'btn_b', 'btn_c']]
        if uid in ('btn_1', 'btn_2', 'btn_3', 'btn_4'):
            self.btns[uid]['lbl'] = saved_lbl
            self.btns[uid]['bg'] = self.BLACK
        print("as> going in to run {} task loop".format(uid))
        self.run_tsk(uid)

    def run_app(self):
        """ outer loop for app selection with task state stored in dict(ctx) """

        while True:
            touched_btn = self.touch.btn_gesture()
            if touched_btn is not None:
                getattr(self, list(touched_btn.keys())[0])(touched_btn)

    def run_tsk(self, uid):
        """ inner loop for selected app """

        tp_prev = None
        i = 0
        x = None
        y = None
        while True:
            tp = self.touch.touch_points
            if tp_prev != tp:
                try:
                    x = tp[0]['x']
                    y = tp[0]['y']
                except IndexError as e:
                    pass
                if x == 0 and y == 0:
                    continue
                elif y in range(self.loc_w[1], self.loc_w[1] + self.loc_w[3]):
                    app_x = 'app_' + uid[-1]
                    try:
                        getattr(self, app_x)(uid, x, y)
                    except Exception as e:
                        print("rt> {} -- missing implementation?".format(e))
                elif i > 0 and self.touch.touch_detected(self.btns[uid]['loc']):
                    print("rt> exiting run {} task loop".format(uid))
                    break
                elif self.touch.touch_detected(self.loc_5):
                    tsk = 'tsk_' + uid[-1] + '5'
                    try:
                        getattr(self, tsk)(uid, 'btn_5')
                    except Exception as e:
                        print("rt> {} -- missing implementation?".format(e))
                elif self.touch.touch_detected(self.loc_6):
                    tsk = 'tsk_' + uid[-1] + '6'
                    try:
                        getattr(self, tsk)(uid, 'btn_6')
                    except Exception as e:
                        print("rt> {} -- missing implementation?".format(e))
                elif self.touch.touch_detected(self.loc_7):
                    tsk = 'tsk_' + uid[-1] + '7'
                    try:
                        getattr(self, tsk)(uid, 'btn_7')
                    except Exception as e:
                        print("rt> {} -- missing implementation?".format(e))
                elif self.touch.touch_detected(self.loc_8):
                    tsk = 'tsk_' + uid[-1] + '8'
                    try:
                        getattr(self, tsk)(uid, 'btn_8')
                    except Exception as e:
                        print("rt> {} -- missing implementation?".format(e))
            tp_prev = tp
            i = i + 1

    @staticmethod
    def clock():
        """ update btn_t wk_dt_time display"""
        # display format: Tue Apr 02, 10:05:02
        # time.localtime() returns (yr, mo, day, hr, mi, se, wd, yd)

        wk = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
        mo = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

        t = time.localtime()
        h = str(t[3]) if t[3] > 9 else '0' + str(t[3])
        m = str(t[4]) if t[4] > 9 else '0' + str(t[4])
        s = str(t[5]) if t[5] > 9 else '0' + str(t[5])
        tm = h + ':' + m + ':' + s
        dt = tm + ' ' + wk[t[6]] + ' ' + mo[t[1] - 1] + ' ' + str(t[2])
        clk = {'dt': dt, 'tm': tm}
        print("cl> clock ", clk)
        return clk

    def paint(self, k, v):
        """ refresh screen for chosen btn """

        loc = v['loc']
        if v['fill']:
            self.tft.fill_rect(loc[0], loc[1], loc[2], loc[3], v['bg'])
        self.tft.rect(loc[0], loc[1], loc[2], loc[3], v['border'])
        self.tft.text(v['font'], v['lbl'], loc[0] + 6, loc[1] + 12, v['fg'], v['bg'])

    def edit(self, uid, **kwargs):
        """ configure btn properties """

        for k, v in kwargs.items():
            if self.btns[uid][k] != v:
                self.btns[uid][k] = v
        self.paint(uid, self.btns[uid])
        print("ed> {} {}".format(uid, kwargs))

    def btn_a(self, btn):

        if btn['btn_a']['action'] == 'HOLD':
            self.power_down()
        else:
            print("ba> Not Implemented ..")

    def btn_b(self, btn):

        if btn['btn_b']['action'] is not None:
            self.home_screen()

    def btn_c(self, btn):

        if btn['btn_c']['action'] == 'HOLD':
            self.tft.fill(self.BLACK)
            self.hard_reset()
        else:
            print("bc> Not Implemented ..")

    def btn_t(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'TAP':
            self.tft.fill_rect(0, 0, 144, 40, self.BLACK)
            self.tft.text(font16, self.clock()['tm'], 0, 12, self.YELLOW, self.BLACK)
        else:
            self.tft.fill_rect(0, 0, 320, 40, self.BLACK)
            self.tft.text(font16, self.clock()['dt'], 0, 12, self.YELLOW, self.BLACK)

    def btn_w(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action is not None:
            print("bw> Not Implemented ..")

    def btn_1(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if self.ctx['btn']:
                self.app_screen(uid, self.tbtn1)
                self.ctx['btn'] = False
            else:
                self.home_screen()
                self.ctx['btn'] = True

        else:
            print("b1> Not Implemented ..")

    def btn_2(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if self.ctx['btn']:
                self.app_screen(uid, self.tbtn2)
                self.ctx['btn'] = False
            else:
                self.home_screen()
                self.ctx['btn'] = True
        else:
            print("b2> Not Implemented ..")

    def btn_3(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if self.ctx['btn']:
                self.app_screen(uid, self.tbtn3)
                self.ctx['btn'] = False
            else:
                self.home_screen()
                self.ctx['btn'] = True
        else:
            print("b3> Not Implemented ..")

    def btn_4(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if self.ctx['btn']:
                self.app_screen(uid, self.tbtn4)
                self.ctx['btn'] = False
            else:
                self.home_screen()
                self.ctx['btn'] = True
        else:
            print("b4> Not Implemented ..")

    def write(self, tl, font=None, xl=None, yl=None, fg=None, bg=None):
        """ write txt from a list at x,y coordinates in a list"""

        if font is None:
            font = font8
        if xl is None:
            xl = [0]
        if yl is None:
            yl = [40]
        if fg is None:
            fg = self.GREEN
        if bg is None:
            bg = self.BLACK

        [self.tft.text(font, str(t), xl[i], yl[i], fg, bg) for i, t in enumerate(tl)]

    def pallet(self, uid):
        """ choose current pixel color for drawing - e.g, doodle app """

        if self.ctx['pallet'] < len(self.color) - 1:
            self.ctx['pallet'] += 1
        else:
            self.ctx['pallet'] = 0
        txt = ('WHT', 'BLU', 'RED', 'GRN', 'CYAN', 'MGNT', 'YLW', 'BLK')
        if txt[self.ctx['pallet']] == 'BLK':
            fg = self.WHITE
        else:
            fg = self.BLACK
        bg = self.color[self.ctx['pallet']]
        self.edit(uid, lbl=txt[self.ctx['pallet']], fg=fg, bg=bg)
        return bg

    def pen(self, uid):
        """ choose pen thickness for drawing - e.g, doodle app """

        if self.ctx['pen'] < 9:
            self.ctx['pen'] += 1
        else:
            self.ctx['pen'] = 1

        pt = self.ctx['pen']
        txt = 'Pen # ' + str(pt)
        loc = self.btns[uid]['loc']
        x1 = loc[0] + int(loc[2] / 4)
        w = int(loc[2] / 2)
        self.edit(uid)
        self.edit(uid, lbl=txt, font=font8)
        for i in range(pt):
            y = loc[1] + 24 + i
            self.tft.hline(x1, y, w, self.YELLOW)
        return pt

    def imu_json(self):
        """ save 'ts', 'accl', 'gyro', and 'temp' sensor vals to SDCard as '/sd/imu.json'.
        writes all records at a time for self.parms['imu_size'] count -- memory intensive  """

        self.mount_sd()
        fn = self.parms['mdir'] + self.parms['json_file']
        with open(fn, "w") as f:
            gyro_offset = self.sensor.calibrate()
            json.dump(self.read_imu(), f)

        stat = uos.stat(fn)[-4:]
        self.release_spi2()
        return fn, stat, gyro_offset

    def imu_csv(self):
        """ save 'ts', 'accl', 'gyro', and 'temp' sensor vals to SDCard as '/sd/imu.csv'.
        writes one record at a time for self.parms['imu_size'] count -- memory friendly """

        self.mount_sd()
        fn = self.parms['mdir'] + "/imu" + str(time.time())[-4:] + ".csv"
        with open(fn, "w") as f:
            gyro_offset = self.sensor.calibrate()
            header = "timestamp,accl_x,accl_y,accl_z,gyro_x,gyro_y,gyro_z,temp\n"
            f.write(header)
            print(header, end='')
            for n in range(self.parms['imu_size']):
                ts = int(str(time.time_ns())[:-6])
                accl = self.sensor.acceleration
                gyro = self.sensor.gyro
                temp = round(self.sensor.temperature * 1.8 + 32, 1)

                line = str(ts) + ',' + str(accl[0]) + ',' + str(accl[1]) + ',' + str(accl[2]) \
                       + ',' + str(gyro[0]) + ',' + str(gyro[1]) + ',' + str(gyro[2]) + ',' + str(temp) + '\n'
                f.write(line)
                print(n + 1, '>', line, end='')
                time.sleep_ms(self.parms['imu_size'])

        stat = uos.stat(fn)[-4:]
        self.release_spi2()
        return fn, stat, gyro_offset

    def set_imu_parm(self, uid, parm):
        """ set imu parm value """
        start = None
        stop = None
        inc = None
        if parm == 'imu_size':
            start = 0
            stop = 1000
            inc = 20
        elif parm == 'imu_wait':
            start = 0
            stop = 1000
            inc = 100

        if self.parms[parm] < stop:
            self.parms[parm] += inc
        else:
            self.parms[parm] = start

        loc = self.btns[uid]['loc']
        self.edit(uid, lbl=parm, font=font8)
        self.write([self.parms[parm]], xl=[loc[0] + 28], yl=[loc[1] + 24])
        return self.parms[parm]

    def draw_digit(self, digit=8, x=10, y=50, w=24, h=4, color=None):

        digit = str(digit)
        if color is None:
            color = self.GREEN
        else:
            color = color

        xa = x + h
        ya = y
        wa = w
        ha = h

        xb = x + w + h
        yb = y + h
        wb = h
        hb = w

        xc = x + w + h
        yc = y + 2 * h + w
        wc = h
        hc = w

        xd = x + h
        yd = y + 2 * w + 2 * h
        wd = w
        hd = h

        xe = x
        ye = y + 2 * h + w
        we = h
        he = w

        xf = x
        yf = y + h
        wf = h
        hf = w

        xg = x + h
        yg = y + h + w
        wg = w
        hg = h

        """
        '0' = [1, 1, 1, 1, 1, 1, 0]
        '1' = [0, 1, 1, 0, 0, 0, 0]
        '2' = [1, 1, 0, 1, 1, 0, 1]
        '3' = [1, 1, 1, 1, 0, 0, 1]
        '4' = [0, 1, 1, 0, 0, 1, 1]
        '5' = [1, 0, 1, 1, 0, 1, 1]
        '6' = [1, 0, 1, 1, 1, 1, 1]
        '7' = [1, 1, 1, 0, 0, 0, 0]
        '8' = [1, 1, 1, 1, 1, 1, 1]
        '9' = [1, 1, 1, 1, 0, 1, 1]
        """

        if digit not in ('1', '4'):
            self.tft.fill_rect(xa, ya, wa, ha, color)
        else:
            self.tft.fill_rect(xa, ya, wa, ha, self.BLACK)
        if digit not in ('5', '6'):
            self.tft.fill_rect(xb, yb, wb, hb, color)
        else:
            self.tft.fill_rect(xb, yb, wb, hb, self.BLACK)
        if digit != '2':
            self.tft.fill_rect(xc, yc, wc, hc, color)
        else:
            self.tft.fill_rect(xc, yc, wc, hc, self.BLACK)
        if digit not in ('1', '4', '7'):
            self.tft.fill_rect(xd, yd, wd, hd, color)
        else:
            self.tft.fill_rect(xd, yd, wd, hd, self.BLACK)
        if digit in ('0', '2', '6', '8'):
            self.tft.fill_rect(xe, ye, we, he, color)
        else:
            self.tft.fill_rect(xe, ye, we, he, self.BLACK)
        if digit not in ('1', '2', '3', '7'):
            self.tft.fill_rect(xf, yf, wf, hf, color)
        else:
            self.tft.fill_rect(xf, yf, wf, hf, self.BLACK)
        if digit not in ('0', '1', '7'):
            self.tft.fill_rect(xg, yg, wg, hg, color)
        else:
            self.tft.fill_rect(xg, yg, wg, hg, self.BLACK)


if __name__ == "__main__":
    os = Bos()
    os.home_screen()

    try:
        os.run_app()
    except Exception as e:
        print("main> oops I blew up ..", e)
    finally:
        os.hard_reset()
