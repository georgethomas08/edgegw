#!/usr/bin/python

import sys, getopt
from datetime import datetime
from datetime import timedelta
from random import seed
from random import randint
import json
import time
import requests

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

#def main(argv):
def main():
    # Arguments passed
    #print("\nName of Python script:", sys.argv[0])
    #print("\nValue for iteration  :", sys.argv[1])
    #print("\nTime Interval        :", sys.argv[2])

    tEnable = 1
    hEnable = 1
    pEnable = 1
    while(1):
    #for i in range(int(sys.argv[1])):
        #for j in range(1,6):
            tstamp = datetime.now()
            randTemp = randint(1,20)
            temp = randint(5+randTemp, 50+randTemp)
            randHum = randint(1,30)
            humidity = randint(20+randHum, 80+randHum)
            randPress = randint(1,40)
            pressure = randint(50+randPress, 120+randPress)
            dev=1
            rec = {}
            if(tEnable):
                rec['temp'] = temp
            if(hEnable):
                rec['humidity'] = humidity
            if(pEnable):
                rec['pressure'] = pressure

            rec['ts'] = tstamp
            rec['deviceId'] = 1
            #print(rec)
            jtsdata = json.dumps(rec, default = myconverter)
            print(jtsdata)
            #url='http://ec2-34-221-110-17.us-west-2.compute.amazonaws.com:30971/tsdataput'
            #url='http://192.168.49.2:30971/tsdataput'
            url='http://localhost/tsdataput'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            resp = requests.post(url, data=jtsdata, headers=headers)
            resp = json.loads(str(resp.text))

            if(str(resp['Temperature'])  == "False"):
                tEnable = 0
            else:
                tEnable = 1

            if(str(resp['Humidity'])     == "False"):
                hEnable = 0
            else:
                hEnable = 1

            if(str(resp['Pressure'])     == "False"):
                pEnable = 0
            else:
                pEnable = 1

            unit = str(resp['Unit'])
            if(unit == "False"):
                print("Data Frequency: " + str(resp['DataFreq']) + "seconds")
                time.sleep(int(resp['DataFreq']))
            else:
                print("Data Frequency: " + str(resp['DataFreq']) + "minutes")
                time.sleep(int(resp['DataFreq'])*60)


        #time.sleep(int(sys.argv[2]))

if __name__ == "__main__":
   #main(sys.argv[1:])
   main()
