#!/usr/bin/python

import sys
import time
import MySQLdb
import datetime
from threading import Thread,Timer

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *
from notifo import *

def getTime():
        now = datetime.datetime.now()
        dateAndTime = now.strftime("%m-%d-%Y %H:%M:%S")
        return dateAndTime

def init():
        notifo = Notifo(user="pcondosta", secret="xc53e5cdc470b9adb5165adcd4aeb597549136d7c")
        db=MySQLdb.connect(host="localhost",user="pete",passwd="",db="security")
        c=db.cursor()
        interfaceKit = InterfaceKit()
        interfaceKit.openPhidget()
        interfaceKit.waitForAttach(10000)
        sec_state = interfaceKit.getInputState(0)
        setMysql(0,0,FD)
        

def setMysql(sensor,val,name):
        if (val)
                c.execute("""UPDATE sensors set state = %s where sensor = %s""",(val,name))
        
        else: 
                c.execute("""UPDATE sensors set state='0' where sensor = 'FD'""")
        

def getSensorInfo( sensorLoc, sensorVal):
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

init()
while True:
        
#        interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
#        print "Started at " + getTime()
#        c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'ON', %s)""", (getTime()))
#        notifo.send_notification(label="Security", title="Started", msg="Security is on")


#c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'OFF', %s)""", (getTime()))

interfaceKit.closePhidget()
c.close()
db.close()
