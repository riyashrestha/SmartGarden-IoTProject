#blink.py
import time
import RPi.GPIO as GPIO
from gpiozero import Button, LED

# mode=0 when changing frequency, mode=1 when changing brightness
#mode = 0

bright = False

brightMode = 15
dimMode = 16
BtnPin = 12

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(brightMode, GPIO.OUT)
    GPIO.setup(dimMode, GPIO.OUT)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.output(brightMode, GPIO.HIGH)
    GPIO.output(dimMode, GPIO.HIGH)
    
def loop():
    global bright
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=changeBrightness, bouncetime=200)
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
        
def destroy():
    if bright == True:
        GPIO.output(brightMode, GPIO.LOW)
    else:
        GPIO.output(dimMode, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

