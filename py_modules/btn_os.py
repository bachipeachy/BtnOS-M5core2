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

import vga1_16x16 as font16
import vga1_8x8 as font8
from focaltouch import FocalTouch

from m5_init import M5Init


class Bos(M5Init):
    ctx = dict(btn=True, pallet=-1, pen=0)

    def __init__(self, **kwargs):
        """ run app forever until hardware btn_c is 'HELD' for hard reset or haedware btn_a 'HELD' for power down """

        super(Bos, self).__init__(**kwargs)

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

    def home_screen(self):

        self.btns = self.define_btns()
        self.btns.update(self.abtns)
        self.edit('btn_w')
        self.write(tl=["BtnOS"], f=font16, xl=[120], yl=[88], fg=self.GREEN)
        self.write(tl=["(c) bachipeachy"], f=font8, xl=[96], yl=[112], fg=self.GREEN)
        self.write(tl=["Alpha version"], f=font8, xl=[112], yl=[128])
        [self.paint(k, v) for k, v in self.btns.items() if k not in ['btn_w', 'btn_a', 'btn_b', 'btn_c']]
        self.touch = self.enable_touch()

    def app_screen(self, uid, tbtn):

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
                    getattr(self, app_x)(uid, x, y)
                elif i > 0 and self.touch.touch_detected(self.btns[uid]['loc']):
                    print("rt> exiting run {} task loop".format(uid))
                    break
                elif self.touch.touch_detected(self.loc_5):
                    tsk = 'tsk_' + uid[-1] + '5'
                    getattr(self, tsk)(uid, 'btn_5')
                elif self.touch.touch_detected(self.loc_6):
                    tsk = 'tsk_' + uid[-1] + '6'
                    getattr(self, tsk)(uid, 'btn_6')
                elif self.touch.touch_detected(self.loc_7):
                    tsk = 'tsk_' + uid[-1] + '7'
                    getattr(self, tsk)(uid, 'btn_7')
                elif self.touch.touch_detected(self.loc_8):
                    tsk = 'tsk_' + uid[-1] + '8'
                    getattr(self, tsk)(uid, 'btn_8')
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
        " refresh screen for chosen btn "

        loc = v['loc']
        if v['fill']:
            self.tft.fill_rect(loc[0], loc[1], loc[2], loc[3], v['bg'])
        self.tft.rect(loc[0], loc[1], loc[2], loc[3], v['border'])
        self.tft.text(v['font'], v['lbl'], loc[0] + 6, loc[1] + 12, v['fg'], v['bg'])

    def edit(self, uid, **kwargs):
        " configure btn properties "

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

    def app_1(self, uid, x, y):
        """ method to overide typical for all apps """

        print("a1> {}".format(uid))
        self.help_app(uid)

    def app_2(self, uid, x, y):
        print("a2> {}".format(uid))
        self.help_app(uid)

    def app_3(self, uid, x, y):
        print("a3> {}".format(uid))
        self.help_app(uid)

    def app_4(self, uid, x, y):
        print("a4> {}".format(uid))
        self.help_app(uid)

    def tsk_15(self, uid, uidt):
        """ task to overide typical for all tasks """

        print("t15> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_16(self, uid, uidt):
        print("t16> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_17(self, uid, uidt):
        print("t17> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_18(self, uid, uidt):
        print("t18> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_25(self, uid, uidt):
        print("t25> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_26(self, uid, uidt):
        print("t26> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_27(self, uid, uidt):
        print("t27> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_28(self, uid, uidt):
        print("t28> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_35(self, uid, uidt):
        print("t34> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_36(self, uid, uidt):
        print("t36> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_37(self, uid, uidt):
        print("t37> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_38(self, uid, uidt):
        print("t38> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_45(self, uid, uidt):
        print("t45> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_46(self, uid, uidt):
        print("t46> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_47(self, uid, uidt):
        print("t47> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

    def tsk_48(self, uid, uidt):
        print("t48> {}:{}".format(uid, uidt))
        self.help_tsk(uidt)

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

        [self.tft.text(f, t, xl[i], yl[i], fg, bg) for i, t in enumerate(tl)]

    def help_app(self, uid):

        app = str("Bos.app_" + str(uid[-1]))
        tx = "<In " + app + " loop>"
        self.write(tl=[tx], yl=[56], f=font16)
        self.write(tl=["* overide " + app + " method"], yl=[96], f=font16, fg=self.RED)
        self.write(["<touched window btn>"], yl=[136], f=font16, fg=self.YELLOW)

    def help_tsk(self, uidt):

        self.edit('btn_w')
        tx = "  <touched " + str(uidt) + ">"
        self.write([tx], yl=[136], f=font16)

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


if __name__ == "__main__":

    os = Bos()
    os.home_screen()

    try:
        os.run_app()
    except Exception as e:
        print("main> oops I blew up ..", e)
    finally:
        os.hard_reset()