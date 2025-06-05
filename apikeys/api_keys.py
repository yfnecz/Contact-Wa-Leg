import os

class api_keys:

    def __init__(self):
        dir = os.path.dirname(__file__)
        try:
            with open(os.path.join(dir, "maps-api.key")) as file:
                self.maps_api_key = file.read().strip()
        except FileNotFoundError:
            dir = "/etc/secrets/"
            with open(os.path.join(dir, "maps-api.key")) as file:
                self.maps_api_key = file.read().strip()
                
        with open(os.path.join(dir, "geo-api.key")) as file:
            self.geo_api_key = file.read().strip()
        with open(os.path.join(dir, "ai.key")) as file:
            self.ai_key = file.read().strip()
        with open(os.path.join(dir, "captcha-site.key")) as file:
            self.site_key = file.read().strip()
        with open(os.path.join(dir, "captcha.secret")) as file:
            self.site_secret = file.read().strip()
    

    def get_keys(self):
        return (self.ai_key, self.maps_api_key, self.geo_api_key, self.site_key, self.site_secret)
