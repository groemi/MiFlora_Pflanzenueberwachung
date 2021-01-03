# Es muss hier eine Liste mit den MacAdressen der verschiedenen Sensoren übergeben werden
#!/usr/bin/env python3

# Import for Sensor Reading
from miflora.miflora_poller import MiFloraPoller
from btlewrap.gatttool import GatttoolBackend

import time

# Import for InfluxDB
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


#set these Values before runtime

# You can generate a Token from the "Tokens Tab" in the UI
url = "www.yourInfluxDB2.com"
token = "itsMyToken"
org = "organization"
bucket = "plants"

# plants stores the plants name and its Sensors MAC
# plants[i][0] = plantname
# plants[i][1] = bluetooth MAC
plants = [["plant1","plant1MAC"],["plant2","plant2MAC"]]




client = InfluxDBClient(url=url, token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


for i in plants:

    poller = MiFloraPoller(i[1], GatttoolBackend)    
    plantData = {
        "battery": poller.battery_level(),
        "temperature": poller.parameter_value("temperature"),
        "brightness": poller.parameter_value("light"),
        "moisture": poller.parameter_value("moisture"),
        "conductivity": poller.parameter_value("conductivity")
    }
    print(plantData)

    pointBat = Point("bat").tag("host", plants[i][0]).field("battery", plantData["battery"]).time(datetime.utcnow(), WritePrecision.NS)
    pointTemp = Point("temp").tag("host", plants[i][0]).field("temperature", plantData["temperature"]).time(datetime.utcnow(), WritePrecision.NS)
    pointLight = Point("light").tag("host", plants[i][0]).field("brightness", plantData["brightness"]).time(datetime.utcnow(), WritePrecision.NS)
    pointMoist = Point("moist").tag("host", plants[i][0]).field("moisture", plantData["moisture"]).time(datetime.utcnow(), WritePrecision.NS)
    pointFert = Point("cond").tag("host", plants[i][0]).field("cond", plantData["conductivity"]).time(datetime.utcnow(), WritePrecision.NS)

    write_api.write(bucket, org, pointBat)
    write_api.write(bucket, org, pointTemp)
    write_api.write(bucket, org, pointLight)
    write_api.write(bucket, org, pointMoist)
    write_api.write(bucket, org, pointFert)

    print("data is send to InfluxDB")
   

