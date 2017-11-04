#Date: 11/2/2017
#Authors: Niall Miner, Nia Watts, Alan Champion
#Description: This is our final project for CSCI250 Python. We created a audio player
#that lights up LEDs based on the decibal level of the sounds it is playing. Attatched
#to the top is a rotating tentacle that wields a knife to intimidate your enemies.

# Imports
#import RPi.GPIO as GPIO, time, math
import wave
import scipy.io.wavfile
import pyaudio
import numpy as np
# GPIO Junk
#GPIO.setmode(GPIO.BCM)

audioFile = 'audio/SmashMouth-AllStar.wav'

#define stream chunk
chunk = 1024

#instantiate PyAudio
p = pyaudio.PyAudio()

song = wave.open(audioFile, 'rb')
songSciPy = scipy.io.wavfile.read(audioFile)
#open stream
stream = p.open(format = p.get_format_from_width(song.getsampwidth()),
                channels = song.getnchannels(),
                rate = song.getframerate(),
                output = True)

#read data
data = song.readframes(chunk)

frameLocation = 0
streamMax = np.nanmax(songSciPy[1])
streamMin = np.nanmin(songSciPy[1])

print(str(streamMax))
print(str(streamMin))

try:
    #while True:
        #Buttons to modify sound
        #print('hi')
        #print(allStar)
    #play stream
    while data:
        stream.write(data)
        #print(int.from_bytes(data, 'big'))
        data = song.readframes(chunk)
        print(np.average(songSciPy[1][frameLocation][0]))
        frameLocation += 1


except (KeyboardInterrupt, SystemExit):
    print("Exiting...")

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()


#GPIO.cleanup()
