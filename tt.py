import dejavu
from dejavu import recognize, audio


for fn in dejavu.utils.find_files('mp3'):
    dejavu.fingerprint_file(fn)

channels, fs = audio.from_file('mp3/audio_with_water.mp3')
channels = [c[15 * fs: 17 * fs] for c in channels]
print recognize.recognize(channels, fs)
