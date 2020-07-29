import noisereduce as nr
from scipy.io import wavfile
import numpy as np
import wave
import soundfile as sf
from noisereduce.generate_noise import band_limited_noise
import matplotlib.pyplot as plt
import urllib.request
import io

def stereoToMono(audiodata):
    d = audiodata.sum(axis=1) / 2
    return d

# url = "https://raw.githubusercontent.com/timsainb/noisereduce/master/assets/fish.wav"
# response = urllib.request.urlopen(url)
# data, rate = sf.read(io.BytesIO(response.read()))
data, rate = sf.read("testfile.wav")

if (data.shape[1] == 2):
    data = stereoToMono(data)
    
noise_len = 2 # seconds
noise = band_limited_noise(min_freq=2000, max_freq = 12000, samples=len(data), samplerate=rate)*10
noise_clip = noise[:rate*noise_len]
audio_clip_band_limited = data+noise

noise_reduced = nr.reduce_noise(audio_clip=audio_clip_band_limited, noise_clip=noise_clip, prop_decrease=1.0, verbose=True)
noise_reduced /= np.max(np.abs(noise_reduced),axis=0)

wavfile.write("input_audio_noise.wav", rate, audio_clip_band_limited)
wavfile.write("input_audio.wav", rate, data)
wavfile.write("final_audio.wav", rate, noise_reduced)
