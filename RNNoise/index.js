const ffmpeg = require('ffmpeg');
const extractAudio = require('ffmpeg-extract-audio');
const rnnoise = require("rnnoise");


const noisyVideoInput = 'data/input/noisy_video_2.mp4';
const noisyMonoAudioOutput = 'data/output/noisy_mono_audio.wav';
const noisyMonoAudio16Output = 'data/output/noisy_mono_audio_16.wav';
const cleanMonoAudioOutput = 'data/output/clean_mono_audio.wav';
const cleanStereoAudioOutput = 'data/output/clean_stereo_audio.wav';


function ffmpegSaveResult(error, file, successMsg, successCallBack) {
    if (!error) {
        console.log(successMsg, file);
        successCallBack && typeof successCallBack === 'function' && successCallBack();
    }
    else {
        console.error(error);
    }
}

function toStereo() {
    try {
        console.log('FFMPEG reading clean mono channel audio.');
        var process = new ffmpeg(cleanMonoAudioOutput);
        process.then(function (audio) {
            console.log('File read. Setting stereo channel.');
            audio
                .setAudioChannels(2)
                .save(cleanStereoAudioOutput, function (error, file) {
                    ffmpegSaveResult(error, file, 'Clean audio saved in stereo channel')
                });

        }, function (err) {
            console.log('Error converting to stereo: ' + err);
        });
    } catch (e) {
        console.log(e.code);
        console.log(e.msg);
    }
}

function suppressUsingRNNoise() {
    console.log('Suppressing noise using RNNoise.');
    try {
        const cleanBufLength = rnnoise.suppress(
            noisyMonoAudio16Output,
            cleanMonoAudioOutput
        );
        console.log('Noise suppressed.');
        console.log(`De-noised buffer length: ${cleanBufLength} bytes`);
        toStereo();
    }
    catch (e) {
        console.error(e)
    }
}

function setBitRate16(file) {
    try {
        console.log('Setting noisy audio bitrate to 16 kb/s.')
        var process = new ffmpeg(file);
        process.then(function (audio) {
            audio
                .setAudioBitRate(16)
                .save(noisyMonoAudio16Output, (error, file) => {
                    ffmpegSaveResult(error, file, 'Noisy audio saved at bitrate=16:', suppressUsingRNNoise);
                })
        }, (reason) => console.log('ffmpeg cannot read file:', reason))
    }
    catch (e) {
        console.error('Cannot set audio bit rate to 16', e);
    }
}

async function asyncVideoExtract() {
    console.log('Extracting audio');
    await extractAudio({
        input: noisyVideoInput,
        output: noisyMonoAudioOutput,
        channel: 1
    }).then(() => {
        console.log('Audio extracted');
        setBitRate16(noisyMonoAudioOutput);
    }, (rejectReason) => {
        console.error('Rejected', rejectReason)
    })
}
asyncVideoExtract();