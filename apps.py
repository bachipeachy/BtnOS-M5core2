from dodl_app import Dodl
from wifi_app import Wifi


class Apps(Wifi, Dodl):

    def __init__(self):
        super(Apps, self).__init__(essid='TBD', pwd='????')


if __name__ == "__main__":

    ap = Apps()
    ap.install_app(('btn_1', 'WiFi'), btn_5='Wifi', btn_6='SCAN', btn_7='TBD', btn_8='Wipe')
    ap.install_app(('btn_4', 'DoDl'), btn_5='CLR', btn_6='PEN', btn_7='TBD', btn_8='Wipe')
    ap.home_screen()
    try:
        ap.run_app()
    except Exception as e:
        print("main> oops BtnOS blew up ..", e)
    finally:
        # to reset M5 module -- required for clean restart
        ap.hard_reset()
