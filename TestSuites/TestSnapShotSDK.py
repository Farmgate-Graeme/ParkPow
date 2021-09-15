# TestSnapShotSDK.py


import requests # Used to get Numberplate
from pprint import pprint
import json


import os
import sys
import site
import platform


# Ensure that our "RaspberryPi" folder is in this Python session's path, and import PlateRecognizerUtils module
try:
    import PlateRecognizerUtils    # Adminsoft's library of SQL utilities in the RaspberryPi folder / package
    if any("RaspberryPi" in lcDir for lcDir in sys.path):
       print("TestSnapShotSDK.py:  PlateRecognizerUtils was imported successfully, and RaspberryPi is already in the path")
    else:
       print("TestSnapShotSDK.py:  PlateRecognizerUtils was imported successfully, but RaspberryPi is not in the Python path")
       print(f"sys.path:  {sys.path}")
except:
    # Add the RaspberryPi folder to the Python path (if not already)
    # Note:  We use forward-slashes in the paths below. These don't need to be escaped (like back-slashes would).
    if os.path.isfile("../FarmgateMain.py"):
       site.addsitedir("../")
       print("TestSnapShotSDK.py:  '../' was added to the path")
    elif os.path.isfile("../RaspberryPi/FarmgateMain.py"):
       site.addsitedir("../RaspberryPi/")
       print("TestSnapShotSDK.py:  '../RaspberryPi' was added to the path")
    elif os.path.isfile("J:/Python/Farmgate/RaspberryPi/FarmgateMain.py"):
       site.addsitedir("J:/Python/Farmgate/RaspberryPi")
       print("TestSnapShotSDK.py:  'J:/Python/Farmgate/RaspberryPi' was added to the path")
    import PlateRecognizerUtils    # Adminsoft's library of SQL utilities in the RaspberryPi folder / package

#import PlateRecognizerUtils
import FarmgateUtils

glDebug = True
gcPlateRecognizerToken = "1df3d23be00daf490284c608b45456e780123a7f"

gnStartTime = 0


def TestPlateRecognizer():
    # gcImageLocation = '/home/pi/Desktop/_TestPlateImages'    #  the path to an image file
    #gcImageLocation = 'C:/Users/Andrew/Source/Repos/FarmgateBackEnd/TestSuites/_TestPlateImages'
    gcImageLocation = "TestSuites/_TestPlateImages"
    print(f"TestSnapShotSDK.py TestPlateRecognizer():  gcImageLocation is {gcImageLocation}")
    while True:
        lcResponse = input("\nFileName for Test Image (eg 'c2'):")
        lnStartTime = FarmgateUtils.GetCurrentTimeMark()
        loResponseDict = PlateRecognizerUtils.GetDictFromCloudAPI(f"{gcImageLocation}/{lcResponse}.jpg")
        print(f"TestSnapShotSDK.py:  GetDictFromCloudAPI() took {FarmgateUtils.TimeElapsedSinceStartMark(lnStartTime)} seconds")
        PlateRecognizerUtils.ProcessDictFromSDK(loResponseDict)
        lnStartTime = FarmgateUtils.GetCurrentTimeMark()
        loResponseDict = PlateRecognizerUtils.GetDictFromSDK(f"{gcImageLocation}/{lcResponse}.jpg")
        print(f"TestSnapShotSDK.py:  GetDictFromSDK() took {FarmgateUtils.TimeElapsedSinceStartMark(lnStartTime)} seconds")
        lnStartTime = FarmgateUtils.GetCurrentTimeMark()
        PlateRecognizerUtils.ProcessDictFromSDK(loResponseDict)
        print(f"TestSnapShotSDK.py:  ProcessDictFromSDK() took {FarmgateUtils.TimeElapsedSinceStartMark(lnStartTime)} seconds")

    #       Start Docker by pasting this into terminal:
    # Nathan Raspberry:
    # docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=95ebhApkbH -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr-raspberry-pi

    # AJ Windows:
    # docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=2pJvzxuK3C -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr:latest
    # AJ Raspberry:
    # docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=2pJvzxuK3C -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr-raspberry-pi


TestPlateRecognizer()