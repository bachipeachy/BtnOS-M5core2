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

from btn_os_p import Bos


class Dodl(Bos):

    def __init__(self):
        """ inherit all BtnOS methods and properties """

        super(Dodl, self).__init__()

    def app_3(self, uid, x, y):
        """ Doodle app invoked by Btn_3 shows output on btn_w space """

        clr = self.color[self.ctx['pallet']]
        pt = self.ctx['pen']
        [[self.tft.pixel(x + i, y + j, clr) for j in range(pt)] for i in range(pt)]

    def tsk_35(self, uid, uidt):
        """ Btn_5 selects color pallet """

        print("t35> {}:{}".format(uid, uidt))
        clr = self.pallet('btn_5')
        print("t35> set color# {}".format(clr))
        return clr

    def tsk_36(self, uid, uidt):
        """ Btn_6 selects pen thickness """

        print("t36> {}:{}".format(uid, uidt))
        pt = self.pen('btn_6')
        print("t36> set pen# {}".format(pt))
        return pt

    def tsk_37(self, uid, uidt):
        """ Btn_7 is unused """

        print("t37> {}:{}".format(uid, uidt))

    def tsk_38(self, uid, uidt):
        """ Btn_8 is erases btn_w space """

        print("t38> {}:{}".format(uid, uidt))
        self.edit('btn_w')
