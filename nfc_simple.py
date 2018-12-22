#! /usr/bin/env python
import re, argparse
from smartcard.System import readers
import datetime, sys

#ACS ACR122U NFC Reader
#Suprisingly, to get data from the tag, it is a handshake protocol
#You send it a command to get data back
#This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer
LOAD_AUTH_KEY=[0xFF,0x82,0x00,0x00,0x06,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]#Load authentication key
AUTHENTICATE_COMMAND=[0xFF,0x86,0x00,0x00,0x05,0x01,0x00,0x04,0x60,0x00]#authenticate
# get all the available readers
r = readers()
print ("Available readers:", r)
reader=r[0]

def authenticate():
    connection = reader.createConnection()
    status_connection = connection.connect()
    connection.transmit(COMMAND)
    #Read command [FF, B0, 00, page, #bytes]
    resp=connection.transmit(LOAD_AUTH_KEY)
    if resp[1]==144:
        print("Authentication key loaded")
    else:
        print("Problem loading auth key")
    resp=connection.transmit(AUTHENTICATE_COMMAND)
    if resp[1]==144:
        print("Authentication done")
    else:
        print("Problem while authenticating")
    
    

def readTag(page): 
            connection = reader.createConnection()
            status_connection = connection.connect()
            connection.transmit(COMMAND)
            #Read command [FF, B0, 00, page, #bytes]
            resp = connection.transmit([0xFF, 0xB0, 0x00, 0x04, 0x3])
            if resp[1]==144:
                print(resp)
            else:
                print("Couldnt read")
           # dataCurr = stringParser(resp)

            #only allows new tags to be worked so no duplicates
           
def writeTag(value):
                connection = reader.createConnection()
                status_connection = connection.connect()
                connection.transmit(COMMAND)
                WRITE_COMMAND = [0xFF,0xD6,0x00,6,0x04,int(value[0:2],16),int(value[2:4],16),int(value[4:6],16),int(value[6:8],16)]#[0xFF, 0xD6, 0x00, int(page), 0x04, int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16)]
                # Let's write a page Page 9 is usually 00000000
                resp = connection.transmit(WRITE_COMMAND)
                print(resp)
                if resp[1] == 144:
                    print ("Wrote " + str(value) + " to page ")
                else:
                    print("Error occured during write operation")



authenticate()
readTag(4)
#writeTag("2506101")
#readTag(5)
