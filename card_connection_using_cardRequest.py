from smartcard.CardType import AnyCardType
from smartcard.CardRequest import  CardRequest
from smartcard.util import toHexString
cardtype=AnyCardType()
cardreq=CardRequest(timeout=100, cardType=cardtype)
cardservice=cardreq.waitforcard()
cardservice.connection.connect()
print(toHexString(cardservice.connection.getATR()))

