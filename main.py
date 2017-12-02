#Date: 11/2/2017
#Authors: Niall Miner, Nia Watts, Alan Champion
#Description: This is our final project for CSCI250 Python. We created a audio player
#that lights up LEDs based on the decibal level of the sounds it is playing. Attatched
#to the top is a rotating tentacle that wields a knife to intimidate your enemies.

import RPi.GPIO as GPIO, time, math
import audio

songs = ['audio/lifeOnMars.wav', 'audio/Short_Skirt_Long_Jacket_by_Cake.wav', 'audio/SmashMouth-AllStar.wav']

songChoice = 0

audioTestObject = audio.Audio(songs[songChoice])

GPIO.setmode(GPIO.BCM)

try:
    while audioTestObject.data:
        audioTestObject.playFrame()
        # print(audioTestObject.calculatedLevelAverage)
        print(audioTestObject.calculatedLevel)

    audioTestObject.close()


except (KeyboardInterrupt, SystemExit):
    print("Exiting...")


GPIO.cleanup()

