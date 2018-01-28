import librosa
import numpy as np
import pyaudio


def from_file(fn, duration=None):
    return librosa.load(fn, sr=None, mono=False, duration=duration)


def from_microphone(seconds, channels=2, fs=44100):
    chunksize = 8192
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=fs,
        input=True,
        frames_per_buffer=chunksize)

    data = [[] for i in range(channels)]

    for i in xrange(0, int(fs / chunksize * seconds)):
        data = stream.read(chunksize)
        nums = np.fromstring(data, np.int16)
        for c in xrange(channels):
            data[c].extend(nums[c::channels])

    stream.stop_stream()
    stream.close()

    return data, fs
