import noisereduce as nr
from scipy.io import wavfile

# load data
rate, data = wavfile.read("output_audio.wav")
# select section of data that is noise
noisy_part = data
# perform noise reduction
reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)

wavfile.write("final_audio.wav", rate, reduced_noise)