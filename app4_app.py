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


class App4(Bos):
    """ sample 'template' app """

    def __init__(self):
        """ inherit all BtnOS methods and properties """

        super(App4, self).__init__()

    def app_4(self, uid, x, y):
        print("a4> {}".format(uid))

    def tsk_45(self, uid, uidt):
        print("t45> {}:{}".format(uid, uidt))

    def tsk_46(self, uid, uidt):
        print("t46> {}:{}".format(uid, uidt))

    def tsk_47(self, uid, uidt):
        print("t47> {}:{}".format(uid, uidt))

    def tsk_48(self, uid, uidt):
        print("t48> {}:{}".format(uid, uidt))
