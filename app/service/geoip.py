import controller.logit
import requests
import json
class GeoIP(controller.logit.Logit):
    def __init__(self):
        super(GeoIP, self).__init__(__name__)

    def get_geo_ip(self, ip):
        """
        {u'city': u'Cambridge', u'region_code': u'MA', u'region_name': u'Massachusetts', u'ip': u'23.32.167.135',
        u'time_zone': u'America/New_York', u'longitude': -71.0843, u'metro_code': 506, u'latitude': 42.3626,
         u'country_code': u'US', u'country_name': u'United States', u'zip_code': u'02142'}

        :param ip:
        :return:
        """
        ret = {}
        url = 'http://mygeogeo:8080/json/'+ip
        response = requests.get(url)
        if response.ok:
            ret = json.loads(response.content)
        return ret