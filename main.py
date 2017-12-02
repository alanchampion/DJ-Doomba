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
songs = ['audio/lifeOnMars.wav', 'audio/SmashMouth-AllStar.wav']
songChoice = 0
audioObject = audio.Audio(songs[songChoice])
playing = True

# pin config
playPauseButton = 27
skipButton = 26
motorPin = 12

lightPin1 = 18
lightPin2 = 19
lightPin3 = 20
lightPin4 = 21

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(playPauseButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(skipButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(motorPin, GPIO.OUT)
GPIO.setup(lightPin1, GPIO.OUT)
GPIO.setup(lightPin2, GPIO.OUT)
GPIO.setup(lightPin3, GPIO.OUT)
GPIO.setup(lightPin4, GPIO.OUT)

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
        setLights(0)

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

def setLights(level):
    try:
        GPIO.output(lightPin1, int(level) >= 1)
        GPIO.output(lightPin2, int(level) >= 2)
        GPIO.output(lightPin3, int(level) >= 3)
        GPIO.output(lightPin4, int(level) >= 4)

    except:
        GPIO.output(lightPin1, False)
        GPIO.output(lightPin2, False)
        GPIO.output(lightPin3, False)
        GPIO.output(lightPin4, False)

try:
    motor.start(angle)
    while True:
        while audioObject.data:
            while playing:
                audioObject.playFrame()
                # print(audioObject.calculatedLevelAverage)
                # print(audioObject.calculatedLevel)
                # print(playing)
                setLights(audioObject.calculatedLevel[0])
                checkPlaying()
                checkSkip()
                checkRotation()

            checkPlaying()
            checkSkip()
            checkRotation()

        audioObject.changeSong(songs[songChoice % len(songs)])


except (KeyboardInterrupt, SystemExit):
    print("Exiting...")
    motor.stop()


GPIO.cleanup()

