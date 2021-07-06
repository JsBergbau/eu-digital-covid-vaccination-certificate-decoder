#!/bin/python3
import sys
from base45 import b45decode
from zlib import decompress
from cose.messages import CoseMessage
import cbor2 
import json

if len(sys.argv) != 2:
	print("Usage: ", sys.argv[0], '"<String from QRCode"')
	print('Important write string in "quotation marks"')
	print("Example: ", sys.argv[0], '"HC1:6BF+70790T9WJWG.FKY*4GO0.O1CV2 O5 N2FBBRW1*70HS8WY04AC*WIFN0AHCD8KD97TK0F90KECTHGWJC0FDC:5AIA%G7X+AQB9746HS80:54IBQF60R6$A80X6S1BTYACG6M+9XG8KIAWNA91AY%67092L4WJCT3EHS8XJC$+DXJCCWENF6OF63W5NW6WF6%JC QE/IAYJC5LEW34U3ET7DXC9 QE-ED8%E.JCBECB1A-:8$96646AL60A60S6Q$D.UDRYA 96NF6L/5QW6307KQEPD09WEQDD+Q6TW6FA7C466KCN9E%961A6DL6FA7D46JPCT3E5JDLA7$Q6E464W5TG6..DX%DZJC6/DTZ9 QE5$CB$DA/D JC1/D3Z8WED1ECW.CCWE.Y92OAGY8MY9L+9MPCG/D5 C5IA5N9$PC5$CUZCY$5Y$527B+A4KZNQG5TKOWWD9FL%I8U$F7O2IBM85CWOC%LEZU4R/BXHDAHN 11$CA5MRI:AONFN7091K9FKIGIY%VWSSSU9%01FO2*FTPQ3C3F"')
	exit(1)


qrString = sys.argv[1]

base45string = qrString[4:]
compressedBinaryData = b45decode(base45string)

uncompressedBinaryData = decompress(compressedBinaryData)
#print(uncompressedBinaryData)
cose = CoseMessage.decode(uncompressedBinaryData)
cborRep = cose.payload
#print(cborRep)
cbor2Object = cbor2.loads(cborRep)
print(json.dumps(cbor2Object, indent=6))