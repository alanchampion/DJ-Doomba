#Date: 11/2/2017
#Authors: Niall Miner, Nia Watts, Alan Champion
#Description: This is our final project for CSCI250 Python. We created a audio player
#that lights up LEDs based on the decibal level of the sounds it is playing. Attatched
#to the top is a rotating tentacle that wields a knife to intimidate your enemies.

import RPi.GPIO as GPIO, time, math
import audio
# import gpiozero as gz

# song config
songs = ['audio/lifeOnMars.wav', 'audio/Short_Skirt_Long_Jacket_by_Cake.wav', 'audio/SmashMouth-AllStar.wav']
songChoice = 0
audioTestObject = audio.Audio(songs[songChoice])
playing = True

# pin config
playPauseButton = 27

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(playPauseButton, GPIO.IN)
# playPauseButton = gz.Button(playPauseButtonPin)

# button setup
# handles only pressing once by storing previous state
buttonState = False

def buttonInput(button):
    return GPIO.input(button) == 1

# handles pausing the song on button press
def checkPlaying():
    global buttonState
    button = buttonInput(playPauseButton)
    if button == False and button != buttonState:
        global playing
        playing = not playing

    buttonState = button


try:
    while audioTestObject.data:
        while playing:
            audioTestObject.playFrame()
            # print(audioTestObject.calculatedLevelAverage)
            # print(audioTestObject.calculatedLevel)
            # print(playing)
            checkPlaying()

        checkPlaying()

    audioTestObject.close()


except (KeyboardInterrupt, SystemExit):
    print("Exiting...")


GPIO.cleanup()

