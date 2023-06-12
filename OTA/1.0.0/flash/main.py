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

# # Turn on GREEN LED
# pycom.heartbeat(False)
# pycom.rgbled(0xff00)


# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# Tan's Tenant
app_eui = ubinascii.unhexlify('58A0CBFFFE803F9C')
app_key = ubinascii.unhexlify('E82511CC86A1FF6F8AEC6238920225DA')
dev_eui = ubinascii.unhexlify('70B3D5499A2B29C2')

# Mark's Tenant
# app_eui = ubinascii.unhexlify('0102030405060708')
# app_key = ubinascii.unhexlify('66C384977A646B8BF820D5EF83487397')
# dev_eui = ubinascii.unhexlify('70B3D5499A2B29C2')


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

# creat a object to hold firmware files
data = []

flag = True
# s.send(bytes([0x01, 0x02, 0x03]))
s.settimeout(15.0) # configure a timeout value of 3 seconds
try:
    s.send(bytes([0x03, 0x02, 0x01]))
    print("Sending First 3, 2, 1")
    num_seg = s.recv(64)
    num_seg = int.from_bytes(num_seg, "big")
    print("Received num_seg is {}".format(num_seg))
    s.settimeout(5.0)
except socket.timeout:
    print("Socket Timed Out, manual retranmission to get num_seg")
    s.send(bytes([0x03, 0x02, 0x01]))
    print("Sending First 3, 2, 1")
    num_seg = s.recv(64)
    num_seg = int.from_bytes(num_seg, "big")
    print("Received num_seg is {}".format(num_seg))

# s.send(bytes([0x03, 0x02, 0x01]))
# print("Sending Second 3, 2, 1")
# rx_pkt = s.recv(64)
# print("Received rx_pkt is {}".format(rx_pkt))

start_time = time.time()
data = []

receiving_failed=False
for i in range (num_seg - 1):
    try:
        if(receiving_failed):
            s.send(bytes([0x01, 0x02, 0x03]))
        else:
            s.send(bytes([0x03, 0x02, 0x01]))
        print("Sending {} iter: 3, 2, 1".format(i))
        rx_pkt = s.recv(64)
        receiving_failed = False
        data.append(rx_pkt)
        print("Received rx_pkt is {}".format(rx_pkt))
    except socket.timeout:
        print("Socket Timed Out, retransmitting for iteration {}".format(i))
        i-=1
        print("New value of i is {}".format(i))
        receiving_failed = True
        # print('No packet received')
        # s.send(bytes([0x01, 0x02, 0x03]))
        # print("Sending {} iter: 3, 2, 1".format(i))
        # rx_pkt = s.recv(64)
        # print("Received rx_pkt is {}".format(rx_pkt))


    # s.send(bytes([0x03, 0x02, 0x01]))
    # print("Sending {} iter: 3, 2, 1".format(i))
    # rx_pkt = s.recv(64)
    # data.append(rx_pkt)
    # print("Received rx_pkt is {}".format(rx_pkt))

end_time_1 = time.time()
print("Time to move file over LoRa was: {} seconds".format(end_time_1-start_time))
# Write 2d binary array data to a file
with open('/flash/ota.bin', 'wb') as f:
    for i in range(len(data)):
        f.write(data[i])
end_time_2 = time.time()

print("Time to Flash Firmware was {} seconds".format(end_time_2-end_time_1))
print("Time for Entire Process was  {} seconds".format(end_time_2-start_time))


# while flag:
#     # print("Getting first 1, 2, 3")
#     # # Create a loop to take the segments of the file and store them in the data object
#     # # rx_pkt = s.recv(64)
#     # # print("Received data: {}".format(rx_pkt))
#     # # Check if the data received is the start of the OTA\
#     # print("Check to see if received Data is 1 , 2, 3")
#     # if rx_pkt == bytes([0x01, 0x02, 0x03]):
#     #     print("Performing OTA")
#     #     # Get the number of segments
#     #     s.send(bytes([0x03, 0x02, 0x01]))
#     num_seg = s.recv(64)
#     print("Received num_seg is {}".format(num_seg))

#     while flag:
#         num_seg = s.recv(64)
#         print("Total Length: {}".format(num_seg))
#         # Wait for the number of segments to be received
#         if num_seg != b'':
#             # Convert the byte received to an integer
#             num_seg = int.from_bytes(num_seg, "big")
#             print("Total Length: {}".format(num_seg))
#             s.send(bytes([0x03, 0x02, 0x01]))

#             # using the number of segments, loop through and get the data
#             while len(data) < num_seg:
#                 data_pkt = s.recv(64)
#                 # only append the data if the data_pkt is not empty
#                 if data_pkt != b'':
#                     print("Received data: {}".format(data_pkt))
#                     data.append(data_pkt)
#                     print("Data len is : {}", len(data))
#                     s.send(bytes([0x03, 0x02, 0x01]))
#                 # sleep(1)
#             flag = False
#             # sleep(1)
#     # sleep(1)

# # Write 2d binary array data to a file
# with open('/flash/ota.bin', 'wb') as f:
#     for i in range(len(data)):
#         f.write(data[i])

# data = []
# while True:
#     # get any data received (if any...)
#     rx_pkt = s.recv(64)
#     print("Received data: {}".format(rx_pkt))
#     if rx_pkt == bytes([0x01, 0x02, 0x03]):
#         print("Performing OTA")
#         # Perform OTA
#         ota.connect()
#         ota.update()
#     else:
#         data.append(rx_pkt)
#         print("Data: {}".format(data))

#     sleep(5)




# # send some data
# s.send(bytes([0x01, 0x02, 0x03]))
# while True:


#     # make the socket non-blocking
#     # (because if there's no data received it will block forever...)
#     s.setblocking(True)
#     # ms.settimeout(60.0)

#     try:
#         rx_pkt = s.recv(64)
#         print("Received data: {}".format(rx_pkt))
#     except socket.timeout:
#         print("No data received")


#     # get any data received (if any...)
#     # data = s.recv(64)

#     # Some sort of OTA trigger
#     if rx_pkt == bytes([0x01, 0x02, 0x03]):
#         print("Performing OTA")
#         s.send(bytes([0x03, 0x02, 0x01]))
#         print("Socket send 3,2,1")
#         sleep(1)

#         # Check if received packet is none-empty
#         rx_pkt = s.recv(64)
#         while (rx_pkt == b''):
#             rx_pkt = s.recv(64)
#             print("Receiving Empty packet")
#             sleep(1)

#         num_seg = int.from_bytes(rx_pkt, "big")
#         print("Total Length: {}".format(num_seg))
        
#         # Perform OTA
#         # ota.connect()
#         # ota.update()
#     sleep(5)

