import RPi.GPIO as GPIO
import time

servoPIN = 12   # kies een pin
lft_input = 16
rht_input = 20

GPIO.setmode(GPIO.BCM)  # zet pin mode
GPIO.setup(servoPIN, GPIO.OUT)  # zet pin mode van pin 12 op output
GPIO.setup(lft_input, GPIO.IN)
GPIO.setup(rht_input, GPIO.IN)

p = GPIO.PWM(servoPIN, 50)  # variabele pinnummer en frequentie meegeven (50Hz)
p.start(7)    # initialiseren

waarde = 7

try:
    while True:
        time.sleep(.25)
        if GPIO.input(lft_input) == 1:
            waarde = 4
        elif GPIO.input(rht_input) == 1:
            waarde = 10
        elif GPIO.input(lft_input) == 0 and GPIO.input(rht_input) == 0:
            waarde = 7
        print(waarde, GPIO.input(rht_input), GPIO.input(lft_input))
        p.ChangeDutyCycle(waarde)
except KeyboardInterrupt:
    print(' Interrupted ')
    GPIO.cleanup()
    exit(0)