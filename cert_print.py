import re, argparse
from smartcard.System import readers
import datetime, sys
import requests
import urllib
import json
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import  CardRequest
from smartcard.util import toHexString
url_prefix="http://certificateweb.sumato.tech/api/v1/"
url_all_certs_init=url_prefix+"studentsall"
url_all_certs_complete=url_prefix+"stugents/print/completed"
url_cert_status=url_prefix+"print/status/"
url_cert_pdf=url_prefix+"print/pdf/"#provide certificate id
url_update_cert_complete=url_prefix+"print/complete/" #provide certificate id
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer
LOAD_AUTH_KEY=[0xFF,0x82,0x00,0x00,0x06,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]#Load authentication key
AUTHENTICATE_COMMAND=[0xFF, 0x88, 0x00, 0x04, 0x60, 0x00]#authenticate
# get all the available readers
r = readers()
print ("Available readers:", r)
reader=r[0]

def getCertificateListInit():
    r=requests.get(url_all_certs_init)
    students=r.json()
    return students   
def getCertPdf(certId):
    urllib.request.urlretrieve(url_cert_pdf+certId,"cert_"+certId+".pdf")
    return 1
def updateCertComplete(certId):
    r.requests.get(url_update_cert_complete+certId)
    return 1

def authenticate():
    connection = reader.createConnection()
    status_connection = connection.connect()
    connection.transmit(COMMAND)
    #Read command [FF, B0, 00, page, #bytes]
    resp=connection.transmit(LOAD_AUTH_KEY)
    if resp[1]==144:
        print("Authentication key loaded")
    else:
        print("Problem loading auth key "+resp)
    resp=connection.transmit(AUTHENTICATE_COMMAND)
    if resp[1]==144:
        print("Authentication done")
    else:
        print("Problem while authenticating "+str(resp))
    
    

def readTag(page): 
            connection = reader.createConnection()
            status_connection = connection.connect()
            connection.transmit(COMMAND)
            #Read command [FF, B0, 00, page, #bytes]
            resp = connection.transmit([0xFF, 0xB0, 0x00, 0x04, 0x04])
            if resp[1]==144:
                print(resp)
            else:
                print("Couldnt read "+resp)
           # dataCurr = stringParser(resp)

            #only allows new tags to be worked so no duplicates
           
def writeTag(value):
                page=4
                cardtype=AnyCardType()
                cardreq=CardRequest(timeout=100, cardType=cardtype)
                cardservice=cardreq.waitforcard()
                cardservice.connection.connect()
                print(toHexString(cardservice.connection.getATR()))
                WRITE_COMMAND = [0xFF,0xD6,0x00,0x04,0x04,int(value[0:2],16),int(value[2:4],16),int(value[4:6],16),int(value[6:8],16)]
                print(WRITE_COMMAND)
                #[0xFF, 0xD6, 0x00, int(page), 0x04, int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16)]
                # Let's write a page Page 9 is usually 00000000
                resp = cardservice.connection.transmit(AUTHENTICATE_COMMAND)
                print(resp)
                resp = cardservice.connection.transmit(WRITE_COMMAND)
                print(resp)
                if resp[1] == 144:
                    print ("Wrote " + str(value))
                else:
                    print("Error occured during write operation")
def printToNfc(data):
    #authenticate()
    writeTag(data)

certs=getCertificateListInit()
print(certs[0]['printjob']['certificate_id'])
for cert in certs:
    cert_id=cert['printjob']['certificate_id']
    print(cert_id)
    printToNfc(cert_id)
    getCertPdf(cert['printjob']['certificate_id'])
readTag(4)
#getCertPdf('9315224')
