from dodl_app import Dodl
from imu_app import Imu
from wifi_app import Wifi


class Apps(Wifi, Dodl, Imu):

    def __init__(self):
        super(Apps, self).__init__()


if __name__ == "__main__":

    ap = Apps()
    ap.parms['essid'] = 'TBD'
    ap.parms['pwd'] = '????'
    [print("M5Init parm {}> {} = {}".format(i + 1, k, v)) for i, (k, v) in enumerate(ap.parms.items())]

    ap.install_app(('btn_1', 'WiFi'), btn_5='Wifi', btn_6='Scan', btn_7='TBD', btn_8='Wipe')
    ap.install_app(('btn_2', 'IMU'), btn_5='Accl', btn_6='Gyro', btn_7='Save', btn_8='Wipe')
    ap.install_app(('btn_3', 'DoDl'), btn_5='CLR', btn_6='Pen', btn_7='TBD', btn_8='Wipe')

    ap.home_screen()
    try:
        ap.run_app()
    except Exception as e:
        print("main> oops BtnOS blew up ..", e)
    finally:
        # to reset M5 module -- required for clean restart
        ap.hard_reset()
