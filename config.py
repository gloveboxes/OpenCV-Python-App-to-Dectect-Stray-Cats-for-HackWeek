import json

class Config():

    @property
    def sampleRateInSeconds(self):
        return self._sampleRate

    @sampleRateInSeconds.setter
    def sampleRateInSeconds(self, value):
        try:
            self._sampleRate = float(value)

            if self._sampleRate < 0.1:
                self._sampleRate = 0.1
            if self._sampleRate > 100000:
                self._sampleRate = 100000

        except:
            self._sampleRate = self._sampleRate

    def config_defaults(self):
        print('Failed loading config settings')


    def config_load(self, configFile):
        #global sensor, hubAddress, deviceId, sharedAccessKey, owmApiKey, owmLocation
        try:
            print('Loading {0} settings'.format(configFile))

            config_data = open(configFile)
            config = json.load(config_data)

            self.hubAddress = config['IotHubAddress']
            self.deviceId = config['DeviceId']
            self.sharedAccessKey = config['SharedAccessKey']
            self.CameraLocation = config['CameraLocation']
            self.GeoPoint = config['GeoPoint']
            GeoPoint
        except:
            self.config_defaults()

    def __init__(self, configFile):
        self.sampleRateInSeconds = 12 #set publishing rate in seconds. every 12 seconds (5 times a minute) good for an 8000 msg/day free Azure IoT Hub
        self.config_load(configFile)