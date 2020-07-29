import noisereduce as nr
from scipy.io import wavfile
import numpy as np
import wave
import soundfile as sf
from noisereduce.generate_noise import band_limited_noise
import matplotlib.pyplot as plt
import urllib.request
import io
from sklearn.preprocessing import normalize
import ffmpeg


# assuming data is in stereo format (2 data channels) convert to mono audio by averaging the both audio channel data.
def stereoToMono(audiodata):
    d = audiodata.sum(axis=1) / 2
    return d

# load data
print("loading data!")

rate, data = wavfile.read("testfile.wav")
print(f"number of channels = {data.shape[1]}, length = {data.shape[0] / rate}s")

# wave file can have data in int16 or float32 format.. if in float, values should b e in range [-1, 1]. So normalize.
data = data.astype(float)
data /= np.max(np.abs(data))
# data /= np.linalg.norm(data) # another way of normalizing

# noise-reduce package needs mono audio as input, so if it's stereo audio (i.e. 2 audio channels, one for left speaker, 1 for right, then convert it to 1 audio channel)
if (data.shape[1] == 2):
    data = stereoToMono(data)

print("Data loaded!")
print("Transforming into numpy array! and selecting noisy part in the signal!")

noisy_part = data[:5000]

print('shape of noisy part is: {}'.format(noisy_part.shape))

# perform noise reduction
print("Calling noisereduce module reduce_noise with whole signal and clip with noisy part!")
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, prop_decrease=1.0)
reduced_noise_norm = reduced_noise/np.max(np.abs(reduced_noise),axis=0)

print("Noise reduction successful, writing to wavfile!")

wavfile.write("input_audio.wav", rate, data)
wavfile.write("final_audio.wav", rate, reduced_noise)
wavfile.write("final_audio_norm.wav", rate, reduced_noise_norm)

print("Done!! you made it!")