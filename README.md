# BtnOS-M5core2
* Button Operating System (BtnOS) is python app that runs on M5Stack Core2 hardware
## Introduction
* BtnOS (Button Operating System) alpha version is a skeletal python application that runs on M5Stack Core2 hardware.
* Upto four(4) individual apps can be configured to run on it.

## Installation
* Flash the custom firmware.bin on to M5Stack
* Run  "apps.py" that installs and runs two (2) of possile four (4) apps -- wifi_app and dodl_app

## Overview
* "BtnOS Event and Action Flow" is illustrated in the diagram btn_os.pdf

![Image](https://github.com/bachipeachy/BtnOS-M5core2/blob/master/btn_os.pdf)

## Steps to add an App - e.g, my_app.py
* create a class say Myapp(Bos) in script file 'my_app.py' that inherits every thing from class Bos (btn_os.py)
* Add methods -- app_x(), tsk_x5(), tsk_x6(), tsk_x7() and tsk_x8()
where 'x' can take value 1 through 4, depending which btn_1 through btn_4 will invoke it.
* Update the startup script apps.py using install_app() method as shown in apps.py
* Run apps.py

