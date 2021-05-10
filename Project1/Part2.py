#blink.py
import time
import RPi.GPIO as GPIO
from gpiozero import Button, LED

# mode=0 when changing frequency, mode=1 when changing brightness
mode = 1
Btn1 = 12
Btn2 = 3

pause = False
LedPin = 11 #led1
frequency = [1, 0.75, 0.5, 0.25]

bright = True
brightMode = 15 #led2 bright
dimMode = 16    #led2 dim


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    #buttons
    GPIO.setup(Btn1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(Btn2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    #Frequency mode setup
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.output(LedPin, GPIO.LOW)
    
    #Bright mode setup
    GPIO.setup(brightMode, GPIO.OUT)
    GPIO.setup(dimMode, GPIO.OUT)
    GPIO.output(brightMode, GPIO.LOW)
    GPIO.output(dimMode, GPIO.LOW)

def switchMode(ev=None):
    global mode
    mode = not mode
    print("button 2 pressed")
    
    if mode == 0:
        if bright == True:
            GPIO.output(brightMode, GPIO.LOW)
            GPIO.cleanup(brightMode)
        else:
            GPIO.output(dimMode, GPIO.LOW)
            GPIO.cleanup(dimMode)
        print("mode changed to Frequency")
        
    else:
        GPIO.output(LedPin, GPIO.LOW)
        print("mode changed to Brightness")
    
    
################ Frequency Mode ########################
def Frequency():
    global pause
    while True:
        if mode == 1:
            Brightness()
        for f in frequency:
            if pause:
                while True:
                    if mode == 1:
                        Brightness()
                    GPIO.output(LedPin, GPIO.HIGH)
                    time.sleep(f)
                    GPIO.output(LedPin, GPIO.LOW)
                    time.sleep(f)
                    if pause == False:
                        break
                    print(f)
            else:
                for i in range (3):
                    if mode == 1:
                        Brightness()
                    GPIO.output(LedPin, GPIO.HIGH)
                    time.sleep(f)
                    GPIO.output(LedPin, GPIO.LOW)
                    time.sleep(f)
                    if pause == True:
                        break
                    print(f)
                    
                    
################ Brightness Mode ########################
def Brightness():
    global bright
    while True:
        if mode == 0:
            Frequency()
        print(bright)
        if bright == True:
            GPIO.cleanup(dimMode)
            while True:
                if mode == 0:
                    Frequency()
                GPIO.setup(brightMode, GPIO.OUT)
                GPIO.output(brightMode, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(brightMode, GPIO.LOW)
                time.sleep(1)
                if bright == False:
                    break
        else:
            GPIO.cleanup(brightMode)
            while True:
                if mode == 0:
                    Frequency()
                GPIO.setup(dimMode, GPIO.OUT)
                GPIO.output(dimMode, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(dimMode, GPIO.LOW)
                time.sleep(1)
                if bright == True:
                    break

            
def changeStatus(ev=None):
    global bright
    global pause
    if mode == 1:
        bright = not bright
        print("brightness changed to", bright)
    else:   
        pause = not pause
        print("pause changed to", pause)
        
    
def destroy():
    if mode == 0:
        GPIO.output(LedPin, GPIO.LOW)
    else:
        if bright == True:
            GPIO.output(brightMode, GPIO.LOW)
        else:
            GPIO.output(dimMode, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    GPIO.add_event_detect(Btn1, GPIO.BOTH, callback=changeStatus, bouncetime=200)
    GPIO.add_event_detect(Btn2, GPIO.BOTH, callback=switchMode, bouncetime=200)
    try:
        Brightness()
        
    except KeyboardInterrupt:
        destroy()

