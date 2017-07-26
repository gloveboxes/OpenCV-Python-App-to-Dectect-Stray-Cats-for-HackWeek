# https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/
# https://github.com/opencv/opencv
# https://github.com/opencv/opencv/tree/master/data/haarcascades
# https://realpython.com/blog/python/face-recognition-with-python/
# https://pythonprogramming.net/raspberry-pi-camera-opencv-face-detection-tutorial/
# https://stackoverflow.com/questions/27069789/the-correct-manner-to-install-opencv-in-raspberrypi-to-use-it-with-python
# https://oscarliang.com/raspberry-pi-face-recognition-opencv/
# http://picamera.readthedocs.io/en/release-1.10/recipes1.html#capturing-to-a-file

# sudo pip install opencv-python
# sudo pip install picamera
# sudo apt install scipy
# sudo apt install python-opencv

import paho.mqtt.client as mqtt
import requests
import cv2
import numpy
import json
from time import sleep
import config
import iothub
from datetime import datetime
import base64


headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'aec19de023c343dd8ab6e137b5788063',
}

# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')

cap = cv2.VideoCapture(0)


params = ''
responseJson = ''
strongestEmotion = None
iotHubMode = True


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: %s" % rc)
    client.subscribe(iot.hubTopicSubscribe)


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: %s" % rc)
    # client.username_pw_set(iot.hubUser, iot.generate_sas_token(
    #     iot.endpoint, iot.sharedAccessKey))


def on_message(client, userdata, msg):
    # print("{0} - {1} ".format(msg.topic, str(msg.payload)))
    cfg.sampleRateInSeconds = msg.payload
    # Do this only if you want to send a reply message every time you receive one
    # client.publish("devices/mqtt/messages/events", "REPLY", qos=1)


def on_publish(client, userdata, mid):
    print("Message {0} sent from {1} at {2}".format(str(mid), cfg.deviceId, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def detectFace(img):
    # buff = numpy.fromstring(img, dtype=numpy.uint8)
    # buff = img
    # image = cv2.imdecode(buff, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    return faces


def getEmotion(img):
    try:
        response = requests.post(url='https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize',
                        data=img,
                        headers=headers)
        s = response.status_code
        return response.text
    except Exception as e:
        print(e)
        return None


def StartDetectingCats():
    count = 0

    while True:
        print("Image: " + str(count))
        b, frame = cap.read()
        facesDetected = detectFace(frame)

        img=cv2.imencode('.jpg', frame)[1].tostring()
        b64 = base64.b64encode(bytes(img))

        try:
            json = '{"CameraLocation":"%s","location":{"type":"Point","coordinates":[%s]},"Image":"%s"}' % (cfg.CameraLocation, cfg.GeoPoint, b64)
            client.publish(iot.hubTopicPublish, json)
        except KeyboardInterrupt:
            print("IoTHubClient sample stopped")
            return
        except:
            print("Unexpected error")
            sleep(4)

        if len(facesDetected) > 0:
            print "Image: " + str(count) + " Found " + str(len(facesDetected)) + " face(s)"
            img=cv2.imencode('.jpg', frame)[1].tostring()

        count=count + 1
        sleep(20)




cfg=config.Config("config_default.json")

iot=iothub.IotHub(cfg.hubAddress, cfg.deviceId, cfg.sharedAccessKey)

client=mqtt.Client(cfg.deviceId, mqtt.MQTTv311)

client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message
client.on_publish=on_publish


if iotHubMode:
    token = iot.generate_sas_token()
    client.username_pw_set(iot.hubUser, token)
    # client.tls_set("/etc/ssl/certs/ca-certificates.crt") # use builtin cert on Raspbian
    # Baltimore Cybertrust Root exported from Windows 10 using certlm.msc in base64 format
    client.tls_set("baltimorebase64.cer")
    client.connect(cfg.hubAddress, 8883)
else:
    # connect to local mosquitto service for testing purposes
    client.connect("192.168.1.122")

client.loop_start()

StartDetectingCats()
