# BtnOS-M5core2
* Button Operating System (BtnOS) is a touch enabled event/action framework runs on M5Stack Core2 hardware.
## Introduction
* Button Operating System (BtnOS) is a touch enabled event/action framework that runs on M5Stack Core2 hardware.
* The 'Bos' python class implemented in /py_modules/btn_os.py enables up to four(4) individual apps.
* The home_screen() provides access to these apps.
* The apps run one at a time inside a single event/action inner loop.
* Once an app is selected, it calls an app_screen() associated with the selected app.
* The app_sceen() allows a choice of up to four (4) individual tasks that may be associated with the app.
* The app runs in its own inner "task loop" until "exit" btn is touched for going' back to home_screen()

## Installation
* Flash the custom 'firmware.bin' on to M5Stack using, say thonny IDE or by other means.
* Create a /lib folder at the root level on M5Stack Core2 internal storage.
* copy the apps (wifi_app.py, imu_app.py, dodl_app.py) to /lib folder.
* These apps will now be visible to micropython REPL. Alternatively, they can be frozen into the firmware.
* apps.py is the startup script for invoking the BtnOS and all installed apps.
* Run  "apps.py". It installs and runs three (3) of the possile four (4) apps in /lib folder.

## Overview
* "BtnOS Event and Action Flow" is illustrated in the diagram btn_os.pdf.

![Image](https://github.com/bachipeachy/BtnOS-M5core2/blob/master/btn_os.pdf).

## Steps to add your own App
* As an example, consider app_4.py provided with the distro.
* app_4.py represents an app template that has minimum required skeletal methods used by a typical app.
* app_4.py implemenst class App4 that inherits every thing from parent class Bos (btn_os.py) and grand-parent class M5Init (M5_init.py).
* The required methods in the template are -- app_4(), tsk_45(), tsk_46(), tsk_47() and tsk_48().
* It is important to preserve the app and task naming conventions.
* The apps naming is keyed to btn 1-4 while tasks naming is keyed to btn 5-8.
* Update the startup script apps.py by adding install_app() method as shown in apps.py for other apps.
* Run apps.py. It installs the apps and starts an infinite outer loop
* You can gracefully terminate the BtnOS by holding hardware btn_c or shut it down by holding btn_a.
* If BtnOS bombs (note it is still in dev), it always (?) calls hard_reset() for restart
* If restarts behaves erratically, power down the hardware and restart BtnOS from a known state.

