import noisereduce as nr
from scipy.io import wavfile
import numpy as np
import wave

# load data
print("loading data!")

rate, data = wavfile.read("../output_audio.wav")

print(f"number of channels = {data.shape[1]}")
length = data.shape[0] / rate
print(f"length = {length}s")

data = data/1.0

print("Data loaded!")
print("Transforming into numpy array! and selecting noisy part in the signal!")

# select section of data that is noise
data = np.asfortranarray(data[:,0])
noisy_part = data[:1000]

# perform noise reduction
print("Calling noisereduce module reduce_noise with whole signal and clip with noisy part!")
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part)

print("Noise reduction successful, writing to wavfile!")
wavfile.write("final_audio.wav", rate, reduced_noise)

print("Done!! you made it!")
