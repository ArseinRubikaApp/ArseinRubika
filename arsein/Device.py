from random import choices


class DeviceTelephone:
    def __init__(self, platform):
        if platform == "android":
            self.Device: dict = {
                "app_version": "MA_3.0.7",
                "device_hash": "".join(choices("0123456789", k=26)),
                "device_model": "Arsein-library",
                "is_multi_account": False,
                "lang_code": "fa",
                "system_version": "SDK 28",
                "token": "",
                "token_type": "Firebase",
            }

        elif platform == "web":
            self.Device: dict = {
                "app_version": "WB_4.3.3",
                "device_hash": "".join(choices("0123456789", k=26)),
                "device_model": "Arsein-library",
                "is_multi_account": False,
                "lang_code": "fa",
                "system_version": "Windows 11",
                "token": "",
                "token_type": "Web",
            }

        elif platform == "pwa":
            self.Device: dict = {
                "device_model": "Arsein-library",
                "system_version": "Linux",
                "app_version": "PW_2.5.2",
                "lang_code": "fa",
                "token_type": "Firebase",
                "device_hash": "".join(choices("0123456789", k=26)),
            }
