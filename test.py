import noisereduce as nr
from scipy.io import wavfile
import numpy as np

# load data
rate, data = wavfile.read("output_audio.wav")
data = data/1.0
data = np.asfortranarray(data[:,0])
# select section of data that is noise
noisy_part = data
# perform noise reduction
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part)

wavfile.write("final_audio.wav", rate, reduced_noise)