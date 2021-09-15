# PlateRecognizerUtils.py

# Called by Main program for all Plate Recognizer related functions

import requests # Used to get Numberplate
from pprint import pprint
import json
import copy

import FarmgateUtils

glDebug = True
gcPlateRecognizerToken = "1df3d23be00daf490284c608b45456e780123a7f"
gcCameraID = "Test-Camera"

gnStartTime = 0


def ObtainInfoFromPhoto(pcImageFullFileName = ""):
    global glDebug
    loResponseDict = {}
    lcVehicleType = "" ; lcNumberPlate = "" ; lcTimeStamp = "" ; lcResponseJSON = ""
    loResultDict = {} ; loResponseDict = {}
    try:
        if pcImageFullFileName == "":
           print("ObtainInfoFromPhoto():  pcImageFullFileName is empty")
           return "", "", "", {}, {}, ""
        if glDebug:  print(f"ObtainInfoFromPhoto():  pcImageFullFileName is {pcImageFullFileName}")
        loResponseDict, lcResponseJSON = GetDictFromSDK(pcImageFullFileName)
        lcVehicleType, lcNumberPlate, lcTimeStamp, loResultDict = ProcessDictFromSDK(loResponseDict)
        return lcVehicleType, lcNumberPlate, lcTimeStamp, loResultDict, loResponseDict, lcResponseJSON

    except Exception as exc:
        print(f"ObtainInfoFromPhoto() failed:  %s\n" % str(exc))
        return "", "", "", {}, {}, ""


def GetDictFromSDK(pcImageFullFileName):
    # See:  https://docs.platerecognizer.com/?python#license-plate-recognition
    global glDebug, gcPlateRecognizerToken, gcCameraID
    regions = ['nz'] # Change to your country
    try:
        with open(pcImageFullFileName, 'rb') as fp:
            response = requests.post(
                'http://localhost:8080/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                #camera_id = gcCameraID,
                headers={"Authorization": f"Token {gcPlateRecognizerToken}"} )
        if glDebug:  print(f"\nResponse from PlateRecognizer SDK (Local):")
        if glDebug:  print(f"Response:  {response}")
        if glDebug:  print(f"JSON:  {response.json()}")
        # pprint({response.json()})
        return response.json(), response

    except Exception as exc:
        print(f"GetDictFromSDK() failed:  %s\n" % str(exc))
        return {}, ""


def ProcessDictFromSDK(poResponseDict): 
    """	    The vehicle recognition program (continuous mode):   
    o	Loops every ¼ second until turned off, or times out (after 30 seconds)
    	    Take a photo (of vehicle or worker’s farm tag)
    	    Send photo to local SDK
    	    Decode the result
    o	If any numberplate has been recognised or vehicle type is a “Big truck”:
    	    Starts the vehicle handler program (passing details as parameters)
    	    Turns itself off """

    # Model, Make and Colour are available for additional fee. Free for <2500 Lookups p/m, <50,000 is $50 p/m. 
    #https://platerecognizer.com/pricing?utm_source=docs&utm_medium=website
    try:
          # Unpack response into Type, Plate and Timestamp
        lcFileName = "" ; lcType = "" ; lcPlate = "" ; lcTimeStamp = ""
        print()
        lcFileName = f"{poResponseDict['filename']}"
        lcTimeStamp = f"{poResponseDict['timestamp']}"
        if glDebug:  print(f"ProcessDictFromSDK():  File Name is {lcFileName}")

        laResultsList = poResponseDict['results']  # check len of results: len will still remain 1 if empty
        #print(laResultsList)
        if laResultsList == []:
            print('Results blank, plate not found in photo')
            return "", "", "", "", {}
        for loResultDict in laResultsList: # Can be multiple plates present, Should be only 1.
            lcPlate = f"{loResultDict['plate']}" # 'candidates' contains other number plate matches, the best guess should be sufficient
            loVehicleDict = loResultDict['vehicle'] # 'vehicle'/ may not always have a value
            lcType = f"{loVehicleDict['type']}"
            break                                   # The most likely result is always first

        if glDebug:  print(f"ProcessDictFromSDK():  Vehicle Type is {lcType}, Number Plate is {lcPlate}, Time Stamp is {lcTimeStamp}")
        return lcType, lcPlate, lcTimeStamp, loResultDict

    except Exception as exc:
        print(f"ProcessDictFromSDK() failed:  %s\n" % str(exc))
        return "", "", "", "", {}


def GetDictFromCloudAPI(pcImageLocation):
    # This doesn't require Docker to be running, should always work.
    # https://docs.platerecognizer.com/?python#license-plate-recognition
    global glDebug, gcPlateRecognizerToken, gcCameraID
    regions = ['nz']

    if glDebug:  print(f"\nGetDictFromCloudAPI():  Calling the cloud API.  Camera ID is {gcCameraID}")
    try:
        with open(pcImageLocation, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data = dict(regions=regions, camera_id=gcCameraID),  # Optional
                files = dict(upload=fp),
                #camera_id = gcCameraID,
                headers = {"Authorization": f"Token {gcPlateRecognizerToken}"} )
                #data=dict(regions=['us-ca'], config=json.dumps(dict(region="strict"))),  # Optional, # Calling with a custom engine configuration
        if glDebug:  print("Response from PlateRecognizer API (Online):")
        if glDebug:  print(f"{response.json()}")
        #pprint({response.json()})
        return response.json()

    except Exception as exc:
        print(f"GetDictFromCloudAPI() failed:  %s\n" % str(exc))
        return {}


def UploadPhotoAndDetailsToParkPow(pcFileOrBase64Image = "", poSDKResultDict = "", pcCameraID = "", pcTime = ""):
    # See https://app.parkpow.com/documentation/#operation/Send%20Camera%20Images%20and%20License%20Plate%20Data
    global glDebug, gcPlateRecognizerToken, gcCameraID
    try:
        if pcCameraID == "":  pcCameraID = gcCameraID
        if len(pcFileOrBase64Image) < 250:
           lcBase64Image = FarmgateUtils.ConvertPhotoToBase64(pcFileOrBase64Image)
        else:
           lcBase64Image = pcFileOrBase64Image
        loSDKResultDict = poSDKResultDict
        #loSDKResultDict = copy.deepcopy(poSDKResultDict)
        #loSDKResultDict = FarmgateUtils.CopyValuesOnly(poSDKResultDict)
        if not "model_make" in loSDKResultDict:
           if glDebug:  print("\nUploadPhotoAndDetailsToParkPow():  Needed to add MMC keys to poSDKResultDict")
           if False:
              loSDKResultDict["model_make"] = []
              loSDKResultDict["color"] = []
              loSDKResultDict["orientation"] = []
           elif True:
              loSDKResultDict["model_make"] = None
              loSDKResultDict["color"] = None
              loSDKResultDict["orientation"] = None
           else:
              loSDKResultDict["model_make"] = [{"make": "BMW", "score": 0.254, "model": "5 Series"},]
              loSDKResultDict["color"] = [{"color": "silver","score": 0.864},]
              loSDKResultDict["orientation"] = [{"score": 0.921, "orientation": "Front"},]
        #loBodyDict = {"camera": pcCameraID, "image": lcBase64Image, "results": loSDKResultDict }
        if glDebug:  print(f"\nUploadPhotoAndDetailsToParkPow():  loSDKResultDict is type {type(loSDKResultDict)}:  {loSDKResultDict}")
        response = requests.post(
            "https://app.parkpow.com/api/v1/log-vehicle/",
            json = dict(camera=pcCameraID, image=lcBase64Image, results=loSDKResultDict),
            headers = {"Authorization": f"Token {gcPlateRecognizerToken}"} )
        if glDebug:  print("\nResponse from ParkPow API:")
        if glDebug:  print(f"{response.json()}")
        #if glDebug:  print(f"UploadPhotoAndDetailsToParkPow():  loBodyDict is {loBodyDict}")
        # pprint({response.json()})
        return response.json()

    except Exception as exc:
        print(f"UploadPhotoAndDetailsToParkPow() failed:  %s\n" % str(exc))
        return {}


def UploadNewApprovedVehicleDetailsToParkPow(pcBase64Image = "", pcVehicleType = "", pcNumberPlate = "", pcTimeStamp = ""):
    # See https://app.parkpow.com/documentation/#operation/Create%20or%20Update%20Vehicle%20Details
    return


def DownloadWhitelistFromParkPow():
    # See https://app.parkpow.com/documentation/#operation/List%20Vehicles
    return


# Run this program for quick test
def testPlateRecognizer():
    gcImageLocation = '/home/pi/Desktop/_TestPlateImages'    #  the path to an image file
    gcImageLocation = 'C:/Users/Andrew/Source/Repos/FarmgateBackEnd/TestSuites/_TestPlateImages'
    while True:
        lcResponse = input("\nFileName for Test Image (eg 'c2'):")
        loResponseDict = getNumberPlateCloudAPI(f"{gcImageLocation}/{lcResponse}.jpg")
        processDockerOutput(loResponseDict)
        loResponseDict = getNumberPlateSDK(f"{gcImageLocation}/{lcResponse}.jpg")
        processDockerOutput(loResponseDict)


    #       Start Docker by pasting this into terminal:
    # Nathan Raspberry:
    # docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=95ebhApkbH -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr-raspberry-pi

    # AJ Windows:
    # docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=2pJvzxuK3C -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr:latest
    # AJ Raspberry:
    # docker run --rm -t -p 8080:8080 -v license:/license -e LICENSE_KEY=2pJvzxuK3C -e TOKEN=1df3d23be00daf490284c608b45456e780123a7f platerecognizer/alpr-raspberry-pi


# testPlateRecognizer()