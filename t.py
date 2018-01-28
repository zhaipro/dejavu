import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

y, sr = librosa.load('mp3/audio.mp3')
C = librosa.cqt(y, sr=sr)
print C.shape, C.dtype
C = librosa.amplitude_to_db(C, ref=np.max)
print C.shape, C.dtype, np.min(C), np.max(C)
librosa.display.specshow(C, sr=sr, x_axis='time', y_axis='cqt_note')
plt.colorbar(format='%+2.0f dB')
plt.title('Constant-Q power spectrum')
plt.tight_layout()
plt.show()
