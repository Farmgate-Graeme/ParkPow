# FarmgateUtils.py
# All Utilty Functions required for Back End

# BackEndUtils called by Raspberry Pi for actions to be performed by server.

# Server Tasks: 
# Save Image/ update log file, check Plate with criminal database 

# Local Tasks:
# Primary: Check Local Whitelist/Blacklist, Send Text
# Implements: Motion(InfraR - 7+ meters), Speaker/Buzzer

import os
import sys
import site
import platform
import urllib       # Native to Python. Contains parse_qs() - Parse query string
import base64
import time

lcTestPath = "C:/Users/Andrew/Source/Repos/PlateRecognizer/TestSuites/_TestPlateImages"

glDebug = True
if glDebug: gnStartTime = 0 


def ConvertPhotoToBase64(pcPhotoFullPathName): 
    # See: https://www.codegrepper.com/code-examples/python/convert+jpg+to+base64+python
    global glDebug
    image_64_decode = ""
    try:
        image = open(pcPhotoFullPathName, 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        #print(image_64_encode)
        image_64_decode = base64.decodebytes(image_64_encode) 
        #image_result = open('deer_decode.jpg', 'wb') # create a writable image and write the decoding result
        #image_result.write(image_64_decode)
    except Exception as exc:
        print(f"B64 Conversion failed:  %s\n" % str(exc))

    return image_64_decode

def GetCurrentTimeMark():
    return round(time.perf_counter(), 3)


def TimeElapsedSinceStartMark(pnStartTime = 0):
    return round(time.perf_counter() - pnStartTime, 3)


def CopyValuesOnly(poSource):
    global glDebug
    loResult = None
    try:
        if glDebug:  print(f"FarmgateUtils.py CopyValuesOnly():  poSource is type {type(poSource)}")
        if poSource == None:
           loResult = None
        elif type(poSource) is dict:
           loResult = {}
           for k, v in poSource:
               loResult[k] = v
        elif type(poSource) is list:
           loResult = []
           for v in poSource:
               loResult.append(v)
        elif type(poSource) is tuple:
           loList = []
           for v in poSource:
               loList.append(v)
           loResult = tuple(loList)
        elif "requests" in type(poSource):
           print(f"FarmgateUtils.py CopyValuesOnly():  Identified poSource as being a Response type")
        if glDebug:  print(f"FarmgateUtils.py CopyValuesOnly():  loResult is {loResult}")
        return loResult
    except Exception as exc:
        print(f"FarmgateUtils.py CopyValuesOnly() failed:  %s\n" % str(exc))
        return None

# Old stuff that can be deleted
"""
def RespondToGate():
    print('BackEndUtils ran.')
    LookupPlateDatabase()
    LookupGlobalBlackList()
    SavePhotoToDatabase(poPhoto)
    return


def LookupPlateDatabase(lcPlate):
    print('(Later - Look Up Plate in Database)')
    return


def SavePhotoToDatabase(poPhoto, pcListType):

    print(f'(Later - Save Photo to {pcListType} List)')

    # Get current Time / timestamp
    return
"""

