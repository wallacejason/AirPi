#!/usr/bin/env python

import output
import requests
import json

class Xively(output.Output):
    requiredData = ["APIKey", "FeedID"]
    optionalData = []
    def __init__(self, data):
        self.APIKey = data["APIKey"]
        self.FeedID = data["FeedID"]
    def outputData(self, dataPoints):
        arr = []
        for i in dataPoints:
            # handle GPS data
            if i["name"] == "Location":
                arr.append({"location": {"disposition": i["Disposition"], "ele": i["Altitude"], "exposure": i["Exposure"],  "domain": "physical", "lat": i["Latitude"], "lon": i["Longitude"]}})
            else:
                arr.append({"id": i["name"], "current_value": i["value"]})
        a = json.dumps({"version": "1.0.0", "datastreams": arr})
        try:
            z = requests.put("https://api.xively.com/v2/feeds/" + self.FeedID + ".json", headers = {"X-ApiKey":self.APIKey}, data = a)
            if z.text != "":
                print "Xively Error: " + z.text
                return False
        except Exception as e:
            raise e
        return True
