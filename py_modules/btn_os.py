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

import json
import time

import uos

import vga1_16x16 as font16
import vga1_8x8 as font8
from focaltouch import FocalTouch
from m5_init import M5Init


class Bos(M5Init):
    ctx = dict(btn=True, pallet=-1, pen=0)

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
        self.write(tl=["BtnOS"], f=font16, xl=[120], yl=[88], fg=self.GREEN)
        self.write(tl=["(c) bachipeachy"], f=font8, xl=[96], yl=[112], fg=self.GREEN)
        self.write(tl=["version 3"], f=font8, xl=[124], yl=[128])
        [self.paint(k, v) for k, v in self.btns.items() if k not in ['btn_w', 'btn_a', 'btn_b', 'btn_c']]
        self.touch = self.enable_touch()

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
        """ outer loop for app selection with task state stored in class dict(ctx) """

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

    def clock(self):
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

        print("cl> clock ", dt)
        return {'dt': dt, 'tm': tm}

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
            print("bb> Not Implemented ..")

    def btn_c(self, btn):

        if btn['btn_c']['action'] == 'HOLD':
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

            if Bos.ctx['btn']:
                self.app_screen(uid, self.tbtn1)
                Bos.ctx['btn'] = False
            else:
                self.home_screen()
                Bos.ctx['btn'] = True

        else:
            print("b1> Not Implemented ..")

    def btn_2(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if Bos.ctx['btn']:
                self.app_screen(uid, self.tbtn2)
                Bos.ctx['btn'] = False
            else:
                self.home_screen()
                Bos.ctx['btn'] = True
        else:
            print("b2> Not Implemented ..")

    def btn_3(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if Bos.ctx['btn']:
                self.app_screen(uid, self.tbtn3)
                Bos.ctx['btn'] = False
            else:
                self.home_screen()
                Bos.ctx['btn'] = True
        else:
            print("b3> Not Implemented ..")

    def btn_4(self, btn):

        uid = list(btn.keys())[0]
        loc = btn[uid]['loc']
        action = btn[uid]['action']

        if action == 'Tap' or 'HOLD':

            if Bos.ctx['btn']:
                self.app_screen(uid, self.tbtn4)
                Bos.ctx['btn'] = False
            else:
                self.home_screen()
                Bos.ctx['btn'] = True
        else:
            print("b4> Not Implemented ..")

    def write(self, tl, f=font8, xl=None, yl=None, fg=None, bg=None):
        """ write txt from a list at x,y coordinates in a list"""

        if xl is None:
            xl = [0]
        if yl is None:
            yl = [40]
        if fg is None:
            fg = self.GREEN
        if bg is None:
            bg = self.BLACK

        [self.tft.text(f, str(t), xl[i], yl[i], fg, bg) for i, t in enumerate(tl)]

    def pallet(self, uid):
        """ choose current pixel color for drawing - e.g, doodle app """

        if Bos.ctx['pallet'] < len(self.color) - 1:
            Bos.ctx['pallet'] += 1
        else:
            Bos.ctx['pallet'] = 0
        txt = ('WHT', 'BLU', 'RED', 'GRN', 'CYAN', 'MGNT', 'YLW', 'BLK')
        if txt[Bos.ctx['pallet']] == 'BLK':
            fg = self.WHITE
        else:
            fg = self.BLACK
        bg = self.color[Bos.ctx['pallet']]
        self.edit(uid, lbl=txt[Bos.ctx['pallet']], fg=fg, bg=bg)
        return bg

    def pen(self, uid):
        """ choose pen thickness for drawing - e.g, doodle app """

        if Bos.ctx['pen'] < 9:
            Bos.ctx['pen'] += 1
        else:
            Bos.ctx['pen'] = 1

        pt = Bos.ctx['pen']
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
        fn = self.parms['mdir'] + self.parms['csv_file']
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
                time.sleep_ms(self.parms['imu_wait'])

        stat = uos.stat(fn)[-4:]
        self.release_spi2()
        return fn, stat, gyro_offset


if __name__ == "__main__":

    os = Bos()
    os.home_screen()

    try:
        os.run_app()
    except Exception as e:
        print("main> oops I blew up ..", e)
    finally:
        os.hard_reset()
