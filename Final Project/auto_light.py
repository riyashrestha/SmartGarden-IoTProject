import RPi.GPIO as GPIO
import time

SENSOR_PIN = 23                         #Sensor input pin (Pin 16)
LED_PIN = 24                            #LED output pin (Pin 18)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)

def loop():
    OldValue = not GPIO.input(SENSOR_PIN)
    print('Starting up the LIGHT Module (Press CTRL+C to exit)')
    time.sleep(0.5)
    while True:
        if GPIO.input(SENSOR_PIN) != OldValue:
            if GPIO.input(SENSOR_PIN):
                print ('NIGHT')
                GPIO.output(LED_PIN, 1)       #Turn ON LED
            else:
                print ('DAY')
                GPIO.output(LED_PIN, 0)      #Turn OFF LED
        OldValue = GPIO.input(SENSOR_PIN)
        time.sleep(0.2)

def destroy():
    setup()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup() 
    
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()