#!/usr/bin/python

import sys
import time
import MySQLdb
import datetime

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
from notifo import *

def getTime():
        now = datetime.datetime.now()
        dateAndTime = now.strftime("%m-%d-%Y %H:%M:%S")
        return dateAndTime

notifo = Notifo(user="pcondosta", secret="xc53e5cdc470b9adb5165adcd4aeb597549136d7c")
db=MySQLdb.connect(host="localhost",user="pete",passwd="secnet",db="security")
c=db.cursor()

try:
        interfaceKit = InterfaceKit()
except RuntimeError as e:
        print ("Runtime Error: %s" % e.message)

interfaceKit.openPhidget()
interfaceKit.waitForAttach(10000)
print ("%d attached!" % (interfaceKit.getSerialNum()))

print ("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

def getSensorInfo( sensorLoc, sensorVal):
        msgState = "0"
        if sensorVal:
                msgState = "Closed"
        else:
                msgState = "Opened"

        if sensorLoc == 0:
                sensor = "BSDR"
        if sensorLoc == 1:
                sensor = "BSLR"
        if sensorLoc == 2:
                sensor = "FD"
        return sensor,msgState

def interfaceKitInputChanged(e):
        sensor,state = getSensorInfo(e.index, e.value)
        print ("%s: %s, %i, %s" % (sensor, state, e.value, getTime()))
#        c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES (%s, %s, %s)""", (sensor, state, getTime()))
        msgState = state + " at " + getTime()
        print msgState
#        notifo.send_notification(label="Security", title=sensor, msg=msgState)
        time.sleep(7)
try:
        interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
        print "Started at " + getTime()
#        c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'ON', %s)""", (getTime()))
#        notifo.send_notification(label="Security", title="Started", msg="Security is on")
except PhidgetException as e:
        print ("Phidget Exception %i: %s" % (e.code, e.details))

chr = sys.stdin.read(1)

#c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'OFF', %s)""", (getTime()))

interfaceKit.closePhidget()
c.close()
db.close()
