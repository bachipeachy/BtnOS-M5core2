# BtnOS-M5core2
* Button Operating System (BtnOS) is a touch enabled event/action framework that runs on M5Stack Core2 hardware.
## Introduction
* Button Operating System (BtnOS) is a touch enabled event/action framework that runs on M5Stack Core2 hardware.
* The 'Bos' python class implemented in btn_os.py can execute up to four(4) individual apps.
* The home_screen() provides access to these apps.
* The apps run one at a time inside a single event/action inner loop.
* Once an app is gestured, it calls an app_screen() associated with the selected app.
* The app_sceen() allows gesturing up to four (4) individual task buttons that perform app defined functions.
* The app runs in its own inner "task loop" until "exit" btn is gestured which ends the task loop and calls the home_screen() for gesturing other apps.

## Installation
* Flash the custom 'firmware.bin' on to M5Stack using say, thonny IDE or by other means.
* The firmware contains Micropython latest stable release (1.19) and other required 'c' and 'py' source files in respective modules folder.
* The btn_os.py and app scripts are not included in the firmware to make development process less laborious
* Create a /lib folder at the root level on M5Stack Core2 flash storage.
* Copy python scripts for btn_os and apps (wifi, imu and dodl) to the M5 /lib folder. Note, the script app4_app is simply a template for user apps. It is not installed as an app.
* The module list can be inspected in REPL using help('modules'). Alternatively, they can be frozen into the firmware if the space permits.
* The scripts installed in /lib can be imported into user python scripts.
* apps.py is the startup script for invoking the BtnOS and all installed apps.
* Run  "apps.py". It installs and runs three (3) of the possile four (4) apps in /lib folder.
* Monitor the extensive logging output to console to follow the execution thread.
* For standalone M5Stack operation without console, save apps.py on to flash memory at root level as main.py
* On power-up of the hardware, main.py will startup the BtnOS.

## Overview
* "BtnOS Event and Action Flow" is illustrated in the diagram btn_os.pdf.

![Image](https://github.com/bachipeachy/BtnOS-M5core2/blob/master/btn_os.pdf).

### Screenshots
##### In folder jpg
##### 1_homescreen.jpg
##### 2_wifi_scan.jpg
##### 3_wifi_clok.jpg
##### 4-imu_accl.jpg
##### 5_imu_gyro.jpg
##### 6_imu_csv.jpg
##### 7_dodl.jpg

## Steps to add your own App
* As an example, consider app4_app.py provided with the distro.
* app4_app.py represents an app template that has minimum required skeletal methods used by a typical app.
* app4_app.py implements class App4 that inherits every thing from parent class Bos and grand-parent class M5Init.
* The required methods in app4_app.py are: app_4(), tsk_45(), tsk_46(), tsk_47() and tsk_48().
* It is important to preserve the app and task naming conventions.
* The apps naming is keyed to btn 1-4 while tasks naming is keyed to btn 5-8.
* Update the startup script apps.py by adding install_app() method as shown in apps.py for other apps.
* Run apps.py. It installs the apps and starts an infinite outer loop, wating for a btn gesture.
* You can gracefully terminate the BtnOS (hard reset) by holding hardware btn_c or shut it down by holding btn_a.
* btn_b toggles auto reboot flag when the M5Stack is disconnected from the console machine -- standalone mode.
For btn_b to function correctly, copy apps.py to M5Stack flash memory at root level as main.py
* If BtnOS bombs (note it is still in dev), it calls hard_reset() for next restart cycle.
* If restarts behaves erratically, power down the hardware and restart BtnOS from a known state.
