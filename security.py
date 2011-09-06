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
        FD,BSDR,BSLR = getSensor()
        updateMysql(FD,"FD")
        updateMysql(BSDR,"BSDR")
        updateMysql(BSLR,"BSLR")
        
def getSensor():
        FD = interfaceKit.getInputState(1)
        BSDR = interfaceKit.getInputState(2)
        BSLR = interfaceKit.getInputState(3)
        return FD,BSDR,BSLR

def getMysql():
        c.execute("""select * from sensors""")
        rows = c.fetchone()
        BSDR = rows[1]
        rows = c.fetchone()
        BSLR = rows[1]
        rows = c.fetchone()
        FD = rows[1]
        return BSDR,BSLR,FD
        
def updateMysql(val,name):
                c.execute("""UPDATE sensors set state = %s where sensor = %s""",(val,name))

def checkSensors():
        FD,BSDR,BSLR = getSensor()
        BSDRmy,BSLRmy,FDmy = getMysql()
        if (FD):
                if(FDmy):
                        updateMysql(0,"FD")
                        sendNotifo(0,"FD")
                else:
                        updateMysql(1,"FD")
                        sendNotifo(1,"FD")
        if (BSDR):
                if (BSDRmy):
                        updateMysql(0,"BSDR")
                        sendNotifo(0,"BSDR")
                else:
                        updateMysql(1,"BSDR")
                        sendNotifo(1,"BSDR")
        IF (BSLR):
                if (BSLRmy):
                        updateMysql(0,"BSLR")
                        sendNotifo(0,"BSLR")
                else:
                        updateMysql(1,"BSLR")
                        sendNotifo(1,"BSLR")
        
def sendNotifo(state, location):
        
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
        if (sec_state):
                c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'ON', %s)""", (getTime()))
                checkSensors()
#        interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
#        print "Started at " + getTime()
#        c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'ON', %s)""", (getTime()))
#        notifo.send_notification(label="Security", title="Started", msg="Security is on")


#c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'OFF', %s)""", (getTime()))

interfaceKit.closePhidget()
c.close()
db.close()
