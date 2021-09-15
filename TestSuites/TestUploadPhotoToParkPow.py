# TestUploadPhotoToParkPow.py

# Need to launch Docker and the SDK first.  (See notes at the bottom.)


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
       print("TestUploadPhotoToParkPow.py:  PlateRecognizerUtils was imported successfully, and RaspberryPi is already in the path")
    else:
       print("TestUploadPhotoToParkPow.py:  PlateRecognizerUtils was imported successfully, but RaspberryPi is not in the Python path")
       print(f"sys.path:  {sys.path}")
except:
    # Add the RaspberryPi folder to the Python path (if not already)
    # Note:  We use forward-slashes in the paths below. These don't need to be escaped (like back-slashes would).
    if os.path.isfile("../FarmgateMain.py"):
       site.addsitedir("../")
       print("TestUploadPhotoToParkPow.py:  '../' was added to the path")
    elif os.path.isfile("../RaspberryPi/FarmgateMain.py"):
       site.addsitedir("../RaspberryPi/")
       print("TestUploadPhotoToParkPow.py:  '../RaspberryPi' was added to the path")
    elif os.path.isfile("J:/Python/Farmgate/RaspberryPi/FarmgateMain.py"):
       site.addsitedir("J:/Python/Farmgate/RaspberryPi")
       print("TestUploadPhotoToParkPow.py:  'J:/Python/Farmgate/RaspberryPi' was added to the path")
    import PlateRecognizerUtils    # Adminsoft's library of SQL utilities in the RaspberryPi folder / package

#import PlateRecognizerUtils
import FarmgateUtils

glDebug = True
gcPlateRecognizerToken = "1df3d23be00daf490284c608b45456e780123a7f"


def main():
    gcImageLocation = "TestSuites/_TestPlateImages"
    print(f"\nTestUploadPhotoToParkPow.py:  gcImageLocation is {gcImageLocation}")
    while True:
        lcFileName = input("\nFileName for Test Image (eg 'c2'):") + ".jpg"
        lcFullPathName = gcImageLocation + '/' + lcFileName
        print(f"\nTestUploadPhotoToParkPow.py:  lcFullPathName is {lcFullPathName}")
        lcVehicleType = "" ; lcNumberPlate = "" ; lcTimeStamp = "" ; lcResponseJSON = ""
        loResultDict = {} ; loResponseDict = {}
        lnStartTime = FarmgateUtils.GetCurrentTimeMark()

        lcVehicleType, lcNumberPlate, lcTimeStamp, loResultDict, loResponseDict, lcResponseJSON = PlateRecognizerUtils.ObtainInfoFromPhoto(lcFullPathName)           # f"{gcImageLocation}/{lcFileName}"
        print(f"TestUploadPhotoToParkPow.py:  ObtainInfoFromPhoto() took {FarmgateUtils.TimeElapsedSinceStartMark(lnStartTime)} seconds")
        print(f"TestUploadPhotoToParkPow.py:  loResultDict is {loResultDict}")

        lnStartTime = FarmgateUtils.GetCurrentTimeMark()
        #PlateRecognizerUtils.UploadPhotoAndDetailsToParkPow(lcFullPathName, loResultDict)
        PlateRecognizerUtils.UploadPhotoAndDetailsToParkPow(lcFullPathName, loResultDict)
            # UploadPhotoAndDetailsToParkPow(pcFileOrBase64Image = "", pcSDKResultJSON = "", pcCameraID = "", pcTime = "")
        print(f"TestUploadPhotoToParkPow.py:  UploadPhotoAndDetailsToParkPow() took {FarmgateUtils.TimeElapsedSinceStartMark(lnStartTime)} seconds")


main()


# Start Docker by pasting this into terminal:
# Nathan Raspberry:
# docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=95ebhApkbH -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr-raspberry-pi

# AJ Windows:
# docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=2pJvzxuK3C -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr:latest
# AJ Raspberry:
# docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=2pJvzxuK3C -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr-raspberry-pi

# Graeme Windows 10 computer:
# J:\Python\Farmgate\DockerLaunchScripts\GraemeWin10_LaunchSnapShotSDKinDocker.bat