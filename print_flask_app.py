import re, argparse
from smartcard.System import readers
import datetime, sys
import requests
import urllib
import json
from flask import Flask, render_template, request
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import  CardRequest
from smartcard.util import toHexString
url_prefix="http://certificateweb.sumato.tech/api/v1/"
url_all_certs_init=url_prefix+"studentsall"
url_all_certs_complete=url_prefix+"students/print/completed"
url_cert_status=url_prefix+"print/status/"
url_cert_pdf=url_prefix+"print/pdf/"#provide certificate id
url_update_cert_complete=url_prefix+"print/complete/" #provide certificate id
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer
LOAD_AUTH_KEY=[0xFF,0x82,0x00,0x00,0x06,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]#Load authentication key
AUTHENTICATE_COMMAND=[0xFF, 0x88, 0x00, 0x04, 0x60, 0x00]#authenticate
def getCertPdf(certId):
    urllib.request.urlretrieve(url_cert_pdf+certId,"cert_"+certId+".pdf")
    return 1
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
                #Let's write a page Page 9 is usually 00000000
                #resp = cardservice.connection.transmit(AUTHENTICATE_COMMAND)
                #print(resp)
                resp = cardservice.connection.transmit(WRITE_COMMAND)
                print(resp)
                if resp[1] == 144:
                    print ("Wrote " + str(value))
                else:
                    print("Error occured during write operation")
def getCertificateListInit():
    r=requests.get(url_all_certs_init)
    students=r.json()
    #print(students)
    return students
app=Flask(__name__)
@app.route('/')
def printerNfc():
    return render_template('home.html',students=getCertificateListInit())
@app.route('/printCert')
def printCert():
    certid = request.args.get('certid')
    print("Certificate ID is "+certid)
    getCertPdf(certid)
    writeTag(certid)
    return certid
if __name__ == "__main__":
    app.run(debug=True)
