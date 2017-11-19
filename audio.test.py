import audio
import time

audioTestObject = audio.Audio('audio/lifeOnMars.wav')

# this works, but it opens a while loop, so you can't interact much.
# audioTestObject.playFull()

# this way allows you to interact with the object and do other stuff, such as printing levels.
while audioTestObject.data:
    audioTestObject.playFrame()
    print(audioTestObject.levels)

audioTestObject.close()
