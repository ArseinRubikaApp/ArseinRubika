class clien:
    def __init__(self, platform: str) -> dict:
        if platform == "android":
            self.platform = dict(
                {
                    "app_name": "Main",
                    "app_version": "3.5.7",
                    "lang_code": "fa",
                    "package": "app.rbmain.a",
                    "temp_code": "31",
                    "platform": "Android",
                }
            )
        elif platform == "web":
            self.platform = dict(
                {
                    "app_name": "Main",
                    "app_version": "4.4.6",
                    "platform": "Web",
                    "package": "web.rubika.ir",
                    "lang_code": "fa",
                }
            )
        else:
            self.platform = dict(
                {
                    "app_name": "Main",
                    "app_version": "2.1.4",
                    "platform": "PWA",
                    "package": "m.rubika.ir",
                    "lang_code": "fa",
                }
            )
