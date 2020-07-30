# VideoCleansing

NoiseReduce package is producing promising result. Have a look at that folder..

# Noise Reduction using NoiseReduce pip package. (https://pypi.org/project/noisereduce/)
https://github.com/timsainb/noisereduce

This package uses signal process algorithm based on Fast Fourier transforms to denoise the audio signal.

noise_reduction.py is the main file. 

1. it first reads the wav file. (wav file is an uncompressed audio data file format, mp3 and other popular fiel format are highly compressed and are not apt for audio procesing tasks.)

2. This audio data is nothing but some metadata (sample rate, as it's digital audio, usually it's 41000 Hz), actual data in numpy array with some possible data types.. this datatype is very important, if it's int16 then data values should be in range [-255, 255], if it's float32 then values should be in range [-1, 1] and if the values exceeds these limits, lets say you store -200, somewhere it will create a very very very loud volume, so beware, when experimenting the resulting volume can hurt you, if you are not cautious!

3. so we convert data to float format and normalize it to be in b/w -1, 1..
4. noise-reduce can onlu process mono audio.. so if it's stereo file, we are converting it to mono and then processing..
5. NOTE: If we want to retain stereo file, (which we should ideally), just process each channel 1 by 1..

6. take the noisy clip, as first few samples (currently 5000 samples).. this is done assuming the noise shjould be present in the beginning of the audio as well. and there are highter chances, for few milliseconds, tutor may not speak anything, so it will just be noise.

7. using the above noisy clip and preprocessed data file, we call noise-reduce package to process and remove noise, and it returns back processed audio data numpy array..

8. we again normalize it just to be safe and store it in wave file with same sampling rate!


