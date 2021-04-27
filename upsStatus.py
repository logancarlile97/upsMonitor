import time
import serial
import subprocess

serPort = '/dev/arduino/tty-1-1.4.1' #Related to the USB port the upsMonitor is plugged into
online = False
lastPwrOn = time.time()

def pwrOn(pwrOnInterval):
    global lastPwrOn
    global online
    if (time.time() - lastPwrOn > pwrOnInterval):
        if(online == True):
            lastPwrOn = time.time()
            print("Power ON")
            subprocess.run("cd /home/pi/HomelabShutdown && python3 ./mainPowerOn.py standalone", shell=True, text=True)
            #Put pwrOn cmd here
            
            

def upsStatus(serPort):
    global online
    ser = serial.Serial(serPort, 9600)
    while(True):    
        stat = ser.readline().decode('utf-8').rstrip()
        ser.flush()
        if(stat == "SHUTDOWN"):
            online = False
            print("SHUTDOWN!!!")
            #time.sleep(30)
            subprocess.run("cd /home/pi/HomelabShutdown && python3 ./mainShutdown.py noAuth", shell=True, text=True)
            ##input("Press ENTER to continue")
            break
        elif(stat == "OFFLINE"):
            online = False
        elif(stat == "ONLINE"):
            online = True
            pwrOn(300)
try:
    upsStatus(serPort)
except KeyboardInterrupt:
    print("User Exit")
except Exception as e:
    print(f"ERROR!!!\n{e}")
