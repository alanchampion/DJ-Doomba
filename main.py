#Date: 11/2/2017
#Authors: Niall Miner, Nia Watts, Alan Champion
#Description: This is our final project for CSCI250 Python. We created a audio player
#that lights up LEDs based on the decibal level of the sounds it is playing. Attatched
#to the top is a rotating tentacle that wields a knife to intimidate your enemies.

import RPi.GPIO as GPIO, time, math
import audio

# song config
songs = ['audio/lifeOnMars.wav', 'audio/Short_Skirt_Long_Jacket_by_Cake.wav', 'audio/SmashMouth-AllStar.wav']
songChoice = 0
audioObject = audio.Audio(songs[songChoice])
playing = True

# pin config
playPauseButton = 27
skipButton = 26

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(playPauseButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(skipButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# button setup
# handles only pressing once by storing previous state
pauseButtonState = False
skipButtonState = False

def buttonInput(button):
    return GPIO.input(button) == 1

# handles pausing the song on button press
def checkPlaying():
    global pauseButtonState
    global playPauseButton
    button = buttonInput(playPauseButton)
    if button == False and button != pauseButtonState:
        global playing
        print("Pausing")
        playing = not playing

    pauseButtonState = button

# handles skipping the song
def checkSkip():
    global skipButtonState
    global skipButton
    button = buttonInput(skipButton)
    if button == False and button != skipButtonState:
        global songChoice
        global songs
        global audioObject
        global playing
        print("Skiping")
        songChoice += 1
        audioObject.changeSong(songs[songChoice % len(songs)])
        playing = True

    skipButtonState = button

try:
    while audioObject.data:
        while playing:
            audioObject.playFrame()
            # print(audioObject.calculatedLevelAverage)
            # print(audioObject.calculatedLevel)
            # print(playing)
            checkPlaying()
            checkSkip()

        checkPlaying()
        checkSkip()

    audioObject.close()


except (KeyboardInterrupt, SystemExit):
    print("Exiting...")


GPIO.cleanup()

