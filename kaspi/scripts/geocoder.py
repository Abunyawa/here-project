import requests
import json
import time
import zipfile
import io
from bs4 import BeautifulSoup

class Batch:

    SERVICE_URL = "https://batch.geocoder.ls.hereapi.com/6.2/jobs"
    jobId = None

    def __init__(self, apikey="Ваш ключ для REST API "):
        self.apikey = apikey
        
            
    def start(self, filename, indelim=";", outdelim=";"):
        
        file = open(filename, 'rb')

        params = {
            "action": "run",
            "apiKey": self.apikey,
            "politicalview":"KAZ",
            "gen": 9,
            "maxresults": "1",
            "header": "true",
            "indelim": indelim,
            "outdelim": outdelim,
            "outcols": "displayLatitude,displayLongitude,locationLabel,houseNumber,street,district,city,postalCode,county,state,country",
            "outputcombined": "true",
        }

        response = requests.post(self.SERVICE_URL, params=params, data=file)
        self.__stats (response)
        file.close()
    

    def status (self, jobId = None):

        if jobId is not None:
            self.jobId = jobId
        
        statusUrl = self.SERVICE_URL + "/" + self.jobId
        
        params = {
            "action": "status",
            "apiKey": self.apikey,
        }
        
        response = requests.get(statusUrl, params=params)
        self.__stats (response)
        

    def result (self, jobId = None):

        if jobId is not None:
            self.jobId = jobId
        
        print("Requesting result data ...")
        
        resultUrl = self.SERVICE_URL + "/" + self.jobId + "/result"
        
        params = {
            "apiKey": self.apikey
        }
        
        response = requests.get(resultUrl, params=params, stream=True)
        
        if (response.ok):    
            zipResult = zipfile.ZipFile(io.BytesIO(response.content))
            zipResult.extractall()
            print("File saved successfully")
        
        else:
            print("Error")
            print(response.text)
    

    
    def __stats (self, response):
        if (response.ok):
            parsedXMLResponse = BeautifulSoup(response.text, "lxml")

            self.jobId = parsedXMLResponse.find('requestid').get_text()
            
            for stat in parsedXMLResponse.find('response').findChildren():
                if(len(stat.findChildren()) == 0):
                    print("{name}: {data}".format(name=stat.name, data=stat.get_text()))

        else:
            print(response.text)