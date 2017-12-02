#Date: 11/2/2017
#Authors: Niall Miner, Nia Watts, Alan Champion
#Description: This is our final project for CSCI250 Python. We created a audio player
#that lights up LEDs based on the decibal level of the sounds it is playing. Attatched
#to the top is a rotating tentacle that wields a knife to intimidate your enemies.

import RPi.GPIO as GPIO, time, math
import audio
from datetime import datetime
from datetime import timedelta

# song config
songs = ['audio/lifeOnMars.wav', 'audio/Short_Skirt_Long_Jacket_by_Cake.wav', 'audio/SmashMouth-AllStar.wav']
songChoice = 0
audioObject = audio.Audio(songs[songChoice])
playing = True

# pin config
playPauseButton = 27
skipButton = 26
motorPin = 12

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(playPauseButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(skipButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motorPin, GPIO.OUT)

# button setup
# handles only pressing once by storing previous state
pauseButtonState = False
skipButtonState = False

# motor setu
motor = GPIO.PWM(motorPin, 50)
sleepTime = timedelta(days=0, seconds=0, microseconds=450000)
prevTime = datetime.today()
angle = 2.5

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
        audioObject.close
        songChoice += 1
        audioObject = audio.Audio(songs[songChoice % len(songs)])
        playing = True

    skipButtonState = button

def checkRotation():
    global angle
    global prevTime
    global motor

    curTime = datetime.today()
    if(curTime-prevTime >= sleepTime):
        if(angle == 2.5):
            angle = 12.5
            motor.ChangeDutyCycle(angle)
            prevTime = curTime
        elif(angle == 12.5):
            angle = 2.5
            motor.ChangeDutyCycle(angle)
            prevTime = curTime            

try:
    while audioObject.data:
        while playing:
            audioObject.playFrame()
            # print(audioObject.calculatedLevelAverage)
            # print(audioObject.calculatedLevel)
            # print(playing)
            checkPlaying()
            checkSkip()
            checkRotation()

        checkPlaying()
        checkSkip()
        checkRotation()

    audioObject.close()


except (KeyboardInterrupt, SystemExit):
    print("Exiting...")


GPIO.cleanup()

