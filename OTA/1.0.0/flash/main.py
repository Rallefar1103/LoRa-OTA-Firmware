#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from network import LoRa, WLAN
import socket
import time
from OTA import WiFiOTA
from time import sleep
import pycom
import binascii
import ubinascii

# Turn on GREEN LED
pycom.heartbeat(False)
pycom.rgbled(0xff00)


# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# Tan's Tenant
# app_eui = ubinascii.unhexlify('58A0CBFFFE803F9C')
# app_key = ubinascii.unhexlify('E82511CC86A1FF6F8AEC6238920225DA')
# dev_eui = ubinascii.unhexlify('70B3D5499A2B29C2')
# Mark's Tenant
app_eui = ubinascii.unhexlify('0102030405060708')
app_key = ubinascii.unhexlify('66C384977A646B8BF820D5EF83487397')
dev_eui = ubinascii.unhexlify('70B3D5499A2B29C2')


# Uncomment for US915 / AU915 & Pygate
for i in range(0, 8):
    lora.remove_channel(i)
for i in range(16, 65):
    lora.remove_channel(i)
for i in range(66, 72):
    lora.remove_channel(i)


# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

print("Socket Created")

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
print("Set Socket Data Rate")

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)
print("Set Socket Blocking")

while True:
    # send some data
    s.send(bytes([0x04, 0x05, 0x06]))

    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)
    # ms.settimeout(60.0)

    try:
        rx_pkt = s.recv(64)
        print("Received data: {}".format(rx_pkt))
    except socket.timeout:
        print("No data received")


    # get any data received (if any...)
    data = s.recv(64)

    # Some sort of OTA trigger
    if data == bytes([0x01, 0x02, 0x03]):
        print("Performing OTA")
        # Perform OTA
        ota.connect()
        ota.update()

    sleep(5)

