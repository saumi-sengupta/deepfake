import numpy as np
from scipy.io import wavfile
from scipy.fftpack import dct
from scipy import signal
import os

def hz_to_mel(hz):
    return 2595 * np.log10(1 + hz / 700.0)

def mel_to_hz(mel):
    return 700 * (10**(mel / 2595.0) - 1)

def mel_filterbank(n_filters, n_fft, sr):
    low_mel = hz_to_mel(0)
    high_mel = hz_to_mel(sr/2)
    mel_points = np.linspace(low_mel, high_mel, n_filters+2)
    hz_points = mel_to_hz(mel_points)
    bin_points = np.floor((n_fft+1) * hz_points / sr).astype(int)

    fbanks = np.zeros((n_filters, n_fft//2+1))
    for i in range(1, n_filters+1):
        left, center, right = bin_points[i-1], bin_points[i], bin_points[i+1]
        for j in range(left, center):
            fbanks[i-1, j] = (j-left)/(center-left)
        for j in range(center, right):
            fbanks[i-1, j] = (right-j)/(right-center)
    return fbanks

def extract_features(file_path, sr=16000, n_mfcc=40, n_mels=64, max_pad_len=200, n_fft=512, hop_length=256):
    try:
        if not os.path.exists(file_path):
            return None
            
        if os.path.getsize(file_path) < 1024:
            return None

        rate, audio = wavfile.read(file_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        audio = audio.astype(np.float32)

        if rate != sr:
            num_samples = int(len(audio) * sr / rate)
            audio = signal.resample(audio, num_samples)

        window = np.hamming(n_fft)
        frames = []
        for i in range(0, len(audio)-n_fft, hop_length):
            frame = audio[i:i+n_fft] * window
            spectrum = np.fft.rfft(frame, n_fft)
            power = (1.0 / n_fft) * (np.abs(spectrum) ** 2)
            frames.append(power)
        frames = np.array(frames).T

        fbanks = mel_filterbank(n_mels, n_fft, sr)
        mel_spec = np.dot(fbanks, frames)

        mel_spec = np.where(mel_spec == 0, np.finfo(float).eps, mel_spec)
        log_mel = np.log(mel_spec)

        mfcc = dct(log_mel, type=2, axis=0, norm='ortho')[0:n_mfcc, :]

        if mfcc.shape[1] < max_pad_len:
            pad_width = max_pad_len - mfcc.shape[1]
            mfcc = np.pad(mfcc, pad_width=((0,0),(0,pad_width)), mode='constant')
        else:
            mfcc = mfcc[:, :max_pad_len]

        return mfcc.astype(np.float32)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

