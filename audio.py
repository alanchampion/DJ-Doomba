import wave
import scipy.io.wavfile
import pyaudio
import numpy as np

class Audio:
    def __init__(self):
        self.audioFile = 'audio/SmashMouth-AllStar.wav'

        #define stream chunk
        self.chunk = 1024

        #define pyaudio
        self.p = pyaudio.PyAudio()
        self.song = wave.open(self.audioFile, 'rb')
        self.samprate, self.wavdata = scipy.io.wavfile.read(self.audioFile)

        #get stream
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.song.getsampwidth()),
            channels = self.song.getnchannels(),
            rate = self.song.getframerate(),
            output = True)

        #read data
        self.data = self.song.readframes(self.chunk)
        self.frameLocation = 0

    def play(self):
        try:
            while self.data:
                self.stream.write(self.data)
                self.data = self.song.readframes(self.chunk)
                print(np.average(self.wavdata[self.frameLocation]))
                self.frameLocation += self.chunk

        finally:
            #stop stream
            self.stream.stop_stream()
            self.stream.close()

            #close PyAudio
            self.p.terminate()

test = Audio()
test.play()
