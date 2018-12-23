from smartcard.CardType import AnyCardType
from smartcard.CardRequest import  CardRequest
from smartcard.util import toHexString
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer
LOAD_AUTH_KEY=[0xFF,0x82,0x00,0x00,0x06,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]#Load authentication key
AUTHENTICATE_COMMAND=[0xFF, 0x88, 0x00, 0x04, 0x60, 0x00]#authenticate

cardtype=AnyCardType()
cardreq=CardRequest(timeout=100, cardType=cardtype)
cardservice=cardreq.waitforcard()
cardservice.connection.connect()
print(toHexString(cardservice.connection.getATR()))
print(cardservice.connection.transmit(LOAD_AUTH_KEY))
print(cardservice.connection.transmit(AUTHENTICATE_COMMAND))
print(cardservice.connection.transmit([0xFF, 0xB0, 0x00, 0x04, 0x3]))
