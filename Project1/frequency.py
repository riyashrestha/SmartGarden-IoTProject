#blink.py
import time
import RPi.GPIO as GPIO
from gpiozero import Button, LED

# mode=0 when changing frequency, mode=1 when changing brightness
#mode = 0

pause = False


LedPin = 11
BtnPin = 12
frequency = [1, 0.75, 0.5, 0.25]

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def loop():
    global pause
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=changePause, bouncetime=200)
    while True:
        for f in frequency:
            if pause:
                while True:
                    GPIO.output(LedPin, GPIO.HIGH)
                    time.sleep(f)
                    GPIO.output(LedPin, GPIO.LOW)
                    time.sleep(f)
                    print(f)
                    if pause == False:
                        break
            else:
                for i in range (3):
                    GPIO.output(LedPin, GPIO.HIGH)
                    time.sleep(f)
                    GPIO.output(LedPin, GPIO.LOW)
                    time.sleep(f)
                    print(f)
                    
                    
def changePause(ev=None):
    global pause
    pause = not pause
    print("pause changed")
        
def destroy():
    GPIO.output(LedPin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

