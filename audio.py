import wave
import scipy.io.wavfile
import pyaudio
import numpy as np

class Audio:
    # init function
    def __init__(self, audioFile='audio/SmashMouth-AllStar.wav'):
        self.audioFile = audioFile

        # define stream chunk
        self.chunk = 1024

        # define pyaudio
        self.p = pyaudio.PyAudio()
        self.song = wave.open(self.audioFile, 'rb')
        self.samprate, self.wavdata = scipy.io.wavfile.read(self.audioFile)

        # get stream
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.song.getsampwidth()),
            channels = self.song.getnchannels(),
            rate = self.song.getframerate(),
            frames_per_buffer = 48000,
            output = True)

        # read data
        self.data = self.song.readframes(self.chunk)

        # setup initial data
        self.frameLocation = 0
        self.level = 0

        self.maxLevel = np.amax(np.abs(self.wavdata))

        # number of bins
        self.bins = 4
        self.calculatedLevel = 0

    # plays the full song
    def playFull(self):
        try:
            while self.data:
                # play frame
                self.playFrame()

        finally:
            #stop stream
            self.stream.stop_stream()
            self.stream.close()

            #close PyAudio
            self.p.terminate()

    # plays an individual frame
    def playFrame(self):
        # handle stream
        self.stream.write(self.data)
        self.data = self.song.readframes(self.chunk)

        # get levels
        self.level = np.abs(self.wavdata[self.frameLocation]) + 1
        # TODO: look into averaging all data within the chunk
        # self.level = np.average(np.abs(self.wavdata[self.frameLocation:self.frameLocation + self.chunk]), axis=0)
        self.levelAverage = np.average(np.abs(self.wavdata[self.frameLocation])) + 1

        # get bins of levels
        self.calculatedLevel = self.__bins__(self.level)
        self.calculatedLevelAverage = self.__bins__(self.levelAverage)

        # advance frames
        self.frameLocation += self.chunk

    # closes the object
    def close(self):
        # stop stream
        self.stream.stop_stream()
        self.stream.close()

        #close PyAudio
        self.p.terminate()

    def __bins__(self, level):
        return np.floor((np.log(level) / np.log(self.maxLevel)) * (self.bins + 1))
