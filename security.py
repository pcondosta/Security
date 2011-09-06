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
        security_state = interfaceKit.getInputState(0)
        sec_state(security_state)
        FD,BSDR,BSLR = getSensor()
        updateMysql(FD,"FD")
        updateMysql(BSDR,"BSDR")
        updateMysql(BSLR,"BSLR")

def sec_state(value):
        curState = getMysql("SYSTEM")
        if value is None:
                return getMysql("SYSTEM")
        if (value):
                if (curState eq "0"):
                        updateMysql(1,"SYSTEM")
                        sendNotifo(1,"SYSTEM")
        else:
                if (curState eq "1"):
                        updateMysql(0,"SYSTEM")
                        sendNotifo(0,"SYSTEM")
                
def getSensor():
        FD = interfaceKit.getInputState(1)
        BSDR = interfaceKit.getInputState(2)
        BSLR = interfaceKit.getInputState(3)
        return FD,BSDR,BSLR

def getMysql(value):
        c.execute("""select * from sensors where sensor = %s""", (value))
        rows = c.fetchone()
        val = rows[1]
        return val
        
def updateMysql(val,name):
        c.execute("""UPDATE sensors set state = %s where sensor = %s""",(val,name))
                
def setOutput(channel,value):
        interfaceKit.setOutputState(channel,value)

def checkSensors():
        FD,BSDR,BSLR = getSensor()
        FDmy = getMysql("FD")
        BSDRmy = getMysql("BSDR")
        BSLRmy = getMysql("BSLR")
        if (FD):
                if(FDmy):
                        updateMysql(0,"FD")
                        sendNotifo(0,"FD")
                        setOutput("0",0)
                else:
                        updateMysql(1,"FD")
                        sendNotifo(1,"FD")
                        setOutput("0",1)
        if (BSDR):
                if (BSDRmy):
                        updateMysql(0,"BSDR")
                        sendNotifo(0,"BSDR")
                        setOutput("1",0)
                else:
                        updateMysql(1,"BSDR")
                        sendNotifo(1,"BSDR")
                        setOutput("1",1)
        IF (BSLR):
                if (BSLRmy):
                        updateMysql(0,"BSLR")
                        sendNotifo(0,"BSLR")
                        setOutput("2",0)
                else:
                        updateMysql(1,"BSLR")
                        sendNotifo(1,"BSLR")
                        setOutput("2",1)
        
def sendNotifo(state, location):
        if (state):
                msgState = "Opened at " + getTime()
                notifo.send_notification(label="Security", title=location, msg=msgState)
        else:
                msgState = "Closed At " + getTime()
                notifo.send_notification(label="Security", title=location, msg=msgState)

# TODO: Delete function below
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

# TODO: Delete function below
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
        security_state = sec_state()
        if (security_state):
                checkSensors()
        time.sleep(5)
#        interfaceKit.setOnInputChangeHandler(interfaceKitInputChanged)
#        print "Started at " + getTime()
#        c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'ON', %s)""", (getTime()))
#        notifo.send_notification(label="Security", title="Started", msg="Security is on")


#c.execute("""INSERT INTO sensors_audit (sensor, state, time) VALUES ('Security System', 'OFF', %s)""", (getTime()))

interfaceKit.closePhidget()
c.close()
db.close()
