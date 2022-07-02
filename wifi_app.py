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


class Wifi(Bos):
    """ sample wifi app """

    def __init__(self):
        """ inherit all BtnOS methods and properties """

        super(Wifi, self).__init__()

    def app_1(self, uid, x, y):
        print("a1> {}".format(uid))

        if self.is_wifi_connected():
            self.edit('btn_5', bg=self.GREEN)
        else:
            self.edit('btn_5', bg=self.RED)

    def tsk_15(self, uid, uidt):
        """ toggle wifi connection if available """

        print("t15> {}:{}".format(uid, uidt))

        if self.is_wifi_connected():
            self.write(["disconnecting .."], yl=[96])
            ip = self.disconnect_wifi()
            self.write(["disconnected -> " + ip], yl=[96])
            self.edit('btn_5', bg=self.RED)
        else:
            self.write(["connecting to '" + self.parms['essid'] + "' with 15 sec timeout"], yl=[96])
            ip = self.connect_wifi()
            self.edit('btn_w')
            self.write(["got ip address -> " + ip], yl=[96])
            if ip != '0.0.0.0':
                self.edit('btn_5', bg=self.GREEN)

    def tsk_16(self, uid, uidt):
        print("t16> {}:{}".format(uid, uidt))

        lines = self.scan_wifi()
        ssid = "ssid's scanned " + str(len(lines))
        if len(lines) == 0:
            return
        self.write([ssid, "sig", "bars"], xl=[12, 162, 248], yl=[44, 44, 44], fg=self.YELLOW)

        for i in range(14):
            print("t16> {}: {}".format(i + 1, lines[i]))
            y = 56 + (10 * i)
            self.write(lines[i], xl=[2, 162, 194], yl=[y, y, y])
            bars = lines[i][2]
            if bars > 0:
                self.tft.fill_rect(194, y, 30, 8, self.RED)
            if bars > 1:
                self.tft.fill_rect(194 + 32, y, 30, 8, self.YELLOW)
            if bars > 2:
                self.tft.fill_rect(194 + 64, y, 30, 8, self.BLUE)
            if bars > 3:
                self.tft.fill_rect(194 + 96, y, 30, 8, self.GREEN)

    def tsk_17(self, uid, uidt):
        print("t17> {}:{}".format(uid, uidt))

    def tsk_18(self, uid, uidt):
        print("t18> {}:{}".format(uid, uidt))
        self.edit('btn_w')
