import time
import serial
import subprocess

def findUPSMonitor():
    testCount = 0

    while (True):
        try:
            testCount += 1

            if(testCount == 200):
                print("Could not find ups monitor")
                return "failed"

            
            serTestPort = "COM" + str(testCount) 
            serTest = serial.Serial(serTestPort, 9600, timeout=3)
            commandGathered = serTest.readline().decode('utf-8').rstrip()

            print("Testing " + serTestPort)
            
            if (commandGathered == "UPS-Monitor"):
                print("Found UPS monitor on serial port " + serTestPort)
                return serTestPort

            else:
                print(serTestPort + " did not work")

        except Exception as e:
            print("fail")
            print(e)

def upsStatus(serPort):
        if (serPort == "failed"):
            print("Could not find UPS monitor")
        else:
            ser = serial.Serial(serPort, 9600)
            while(True):    
                stat = ser.readline().decode('utf-8').rstrip()
                ser.flush()
                if(stat == "SHUTDOWN"):
                    print("SHUTDOWN!!!")
                    #time.sleep(30)
                    subprocess.run("shutdown /s /t 0", shell=True, text=True)
                    ##input("Press ENTER to continue")
                    return "shutdown"
                elif(stat == "OFFLINE"):  
                    if(crntOffline == False):
                        print("power outage detected")
                        subprocess.run("msg * Warning!!! Power Outage Detected!!!", shell=True, text=True)
                        crntOffline = True
                else:
                    crntOffline = False

def upsMonitorRun():
    try:
        while(True):
            upsReturn = upsStatus(findUPSMonitor())
            time.sleep(3)
            if(upsReturn == "shutdown"):
                break
    except KeyboardInterrupt:
        print("User Exit")
    except Exception as e:
        print(f"ERROR!!!\n{e}")
        time.sleep(5)
        upsMonitorRun()
        

upsMonitorRun()