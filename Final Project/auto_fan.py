import os
import glob
import time
from time import sleep
import RPi.GPIO as GPIO

#Settings for the environment
pin = 13    #for fan (Pin 33)
maxTemp = 71
minTemp = 70.5
sleepTime = 5


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setwarnings(False)
    return()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def fanON():
    setPin(True)
    return()

def fanOFF():
    setPin(False)
    return()

def getTemperature():
    room_temp = read_temp()
    print(room_temp)
    if room_temp>maxTemp:
        fanON()
    elif room_temp<minTemp:
        fanOFF()
    return()

def setPin(mode):
    GPIO.output(pin, mode)
    return()

def destroy():
    setup()
    fanOFF()
    GPIO.cleanup()
    
def loop():
    while True:
        getTemperature()
        sleep(sleepTime)

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt: 
        destroy()