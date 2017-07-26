# Python 2.7 Sas generator https://azure.microsoft.com/en-us/documentation/articles/iot-hub-sas-tokens/#comments/

from base64 import b64encode, b64decode
from hmac import HMAC
from time import time
from urllib import quote_plus, urlencode
from hashlib import sha256



class IotHub():

    def __init__(self, hubAddress, deviceId, sharedAccessKey):
        self.sharedAccessKey = sharedAccessKey
        self.endpoint = hubAddress + '/devices/' + deviceId
        self.hubUser = hubAddress + '/' + deviceId
        self.hubTopicPublish = 'devices/' + deviceId + '/messages/events/'
        self.hubTopicSubscribe = 'devices/' + deviceId + '/messages/devicebound/#'


    def generate_sas_token(self, expiry=3600):
        ttl = time() + expiry
        sign_key = "%s\n%d" % ((quote_plus(self.endpoint)), int(ttl))
        # print sign_key
        signature = b64encode(HMAC(b64decode(self.sharedAccessKey), sign_key, sha256).digest())

        rawtoken = {
            'sr' :  self.endpoint,
            'sig': signature,
            'se' : str(int(ttl))
        }

        return 'SharedAccessSignature ' + urlencode(rawtoken)