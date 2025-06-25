import wave
import numpy as np

def freq_from_fft(signal, sample_rate):
    freqs = np.fft.rfftfreq(len(signal), d=1/sample_rate)
    fft = np.fft.rfft(signal)
    peak_idx = np.argmax(np.abs(fft))
    return freqs[peak_idx]

def binary_to_text(binary_str):
    chars = [chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)]
    return ''.join(chars)

def decode_wav_to_text(input_wav, output_txt, bit_duration=0.1):
    with wave.open(input_wav, 'r') as wav_file:
        _, _, framerate, n_frames, _, _ = wav_file.getparams()
        frames = wav_file.readframes(n_frames)
        samples = np.frombuffer(frames, dtype=np.int16)

    samples_per_bit = int(framerate * bit_duration)
    bits = []

    for i in range(0, len(samples), samples_per_bit):
        chunk = samples[i:i+samples_per_bit]
        if len(chunk) < samples_per_bit:
            break
        freq = freq_from_fft(chunk, framerate)
        bits.append('0' if abs(freq - 440) < 100 else '1')

    binary_str = ''.join(bits)
    text = binary_to_text(binary_str)

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(text)

decode_wav_to_text('output.wav', 'recovered.txt')
