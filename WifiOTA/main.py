from network import LoRa, WLAN
import socket
import time
from time import sleep
import pycom
import ubinascii
from OTA import WiFiOTA

from config import WIFI_SSID, WIFI_PW, SERVER_IP

pycom.heartbeat(True)

# Setup OTA
ota = WiFiOTA(WIFI_SSID,
              WIFI_PW,
              SERVER_IP,  # Update server address
              8000)  # Update server port

# Turn off WiFi to save power
w = WLAN()
w.deinit()

# Initialise LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# app_eui = ubinascii.unhexlify('70B3D57ED0008CD6')
app_eui = ubinascii.unhexlify('58A0CBFFFE803F9C')
# Need to change the app_key
#app_key = ubinascii.unhexlify('B57F36D88691CEC5EE8659320169A61C')
app_key = ubinascii.unhexlify('E82511CC86A1FF6F8AEC6238920225DA')
dev_eui = ubinascii.unhexlify('70B3D5499A2B29C2')

# Uncomment for US915 / AU915 & Pygate
for i in range(0,8):
    lora.remove_channel(i)
for i in range(16,65):
    lora.remove_channel(i)
for i in range(66,72):
    lora.remove_channel(i)

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')
print("joined!")
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
print("Socket created!")
# set the LoRaWAN data rate - need to set to 3 for USA
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
print("Data Rate Set!")
# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(False)
print("Blocking NOT Set!")

while True:
    # send some data
    s.send(bytes([0x04, 0x05, 0x06]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)

    # Some sort of OTA trigger
    data = bytes([0x01, 0x02, 0x03])
    print("Hardcoded Trigger -> should start OTA")
    if data == bytes([0x01, 0x02, 0x03]):
        print("Performing OTA")
        # Perform OTA
        ota.connect()
        ota.update()

    sleep(5)