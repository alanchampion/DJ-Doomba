import audio
import time

audioTestObject = audio.Audio('audio/lifeOnMars.wav')
# audioTestObject.playFull()

while audioTestObject.data:
    audioTestObject.playFrame()
