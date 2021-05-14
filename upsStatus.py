import time
import serial
import subprocess

serPort = '/dev/arduino/tty-1-1.4.2' #Related to the USB port the upsMonitor is plugged into
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
    try:
        #count = 0 #For debugging
        
        global online
        ser = serial.Serial(serPort, 9600)
        #ser.flush()
        while(True):    
            stat = ser.readline().decode('utf-8').rstrip()
            #ser.flush()
            print(stat)
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
            #time.sleep(0.5)
            
            #count+=1 #For debugging 
            #print(str(count)) #For debugging
            
    except Exception as e:
        print(f"ERROR!!!\n{e}")
        print('Attempting restart in 3 seconds')
        time.sleep(3)
        upsStatus(serPort)

try:
    upsStatus(serPort)
except KeyboardInterrupt:
    print("User Exit")