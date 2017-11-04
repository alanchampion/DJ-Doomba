#Date: 11/2/2017
#Authors: Niall Miner, Nia Watts, Alan Champion
#Description: This is our final project for CSCI250 Python. We created a audio player
#that lights up LEDs based on the decibal level of the sounds it is playing. Attatched
#to the top is a rotating tentacle that wields a knife to intimidate your enemies.

import RPi.GPIO as GPIO, time, math

GPIO.setmode(GPIO.BCM)

try:
    while True:
        #Buttons to modify sound
        

except (KeyboardInterrupt, SystemExit):
    print("Exiting...")


GPIO.cleanup()
