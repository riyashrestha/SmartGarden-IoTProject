#step2.py
import time
import RPi.GPIO as GPIO
from gpiozero import Button, LED

# mode=False when changing frequency, mode=True when changing brightness

mode = False
pause = False   
bright = False

BtnPin1 = 40    #button for mode change
BtnPin2 = 12    #button for functions change

#setting for led frequency change
LedPin1 = 37
frequency = [1, 0.75, 0.5, 0.25]

#setting for led brightness change
brightMode = 15
dimMode = 16
BtnPin2 = 12

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BtnPin1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(BtnPin2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(LedPin1, GPIO.OUT)
    GPIO.setup(brightMode, GPIO.OUT)
    GPIO.setup(dimMode, GPIO.OUT)
    GPIO.output(brightMode, GPIO.HIGH)
    GPIO.output(dimMode, GPIO.HIGH)

def loop():
    global mode
    GPIO.add_event_detect(BtnPin1, GPIO.FALLING, callback=changeMode, bouncetime=200)
    while True:
        if mode == False:
            print("mode is ", mode)
            try:
                loop1()
            except KeyboardInterrupt:
                destroy()
        else:
            print("mode is ", mode)
            try:
                loop2()
            except KeyboardInterrupt:
                destroy()

def changeMode(ev=None):
    global mode
    mode = not mode
    print("Mode changed")
    destroy()

def destroy():
    GPIO.output(LedPin1, GPIO.LOW)
    GPIO.output(brightMode, GPIO.LOW)
    GPIO.output(dimMode, GPIO.LOW)
    GPIO.cleanup()


def loop1():
    global pause
    GPIO.add_event_detect(BtnPin2, GPIO.FALLING, callback=changePause, bouncetime=200)
    while True:
        for f in frequency:
            if pause:
                while True:
                    GPIO.output(LedPin1, GPIO.HIGH)
                    time.sleep(f)
                    GPIO.output(LedPin1, GPIO.LOW)
                    time.sleep(f)
                    print(f)
                    if pause == False:
                        break
            else:
                for i in range (3):
                    GPIO.output(LedPin1, GPIO.HIGH)
                    time.sleep(f)
                    GPIO.output(LedPin1, GPIO.LOW)
                    time.sleep(f)
                    print(f)
                    
                    
def changePause(ev=None):
    global pause
    pause = not pause
    print("pause changed")

def loop2():
    global bright
    GPIO.add_event_detect(BtnPin2, GPIO.FALLING, callback=changeBrightness, bouncetime=200)
    while True:
        print(bright)
        if bright == True:
            while True:
                GPIO.cleanup(dimMode)
                GPIO.setup(brightMode, GPIO.OUT)
                GPIO.output(brightMode, GPIO.HIGH)
                time.sleep(1)
                if bright == False:
                    break
        else:
            while True:
                GPIO.cleanup(brightMode)
                GPIO.setup(dimMode, GPIO.OUT)
                GPIO.output(dimMode, GPIO.HIGH)
                time.sleep(1)
                if bright == True:
                    break
            
def changeBrightness(ev=None):
    global bright
    bright = not bright
    print("brightness changed to", bright)

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()