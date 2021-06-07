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
        global lastPwrOn
        ser = serial.Serial(serPort, 9600, timeout=None)
        time.sleep(1)
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        time.sleep(1)
        #ser.flush()
        while(True):    
            stat = ser.readline().decode('utf-8').rstrip()
            ser.reset_output_buffer()
            ser.reset_input_buffer()
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
                lastPwrOn = time.time()
            elif(stat == "ONLINE"):
                online = True
                pwrOn(360)
            time.sleep(0.5)
            
            #count+=1 #For debugging 
            #print(str(count)) #For debugging
            
    except Exception as e:
        print(f"ERROR!!!\n{e}")
        print('Attempting restart in 3 seconds')
        time.sleep(3)
        upsStatus(serPort)
    except KeyboardInterrupt:
        print("User Exit")    
        ser.close()


upsStatus(serPort)
