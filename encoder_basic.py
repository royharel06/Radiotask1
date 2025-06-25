import wave
import struct
import math

def text_to_binary(text):
    return ''.join(f"{ord(c):08b}" for c in text)

def generate_tone(freq, duration, sample_rate=44100, amplitude=32767):
    samples = int(sample_rate * duration)
    return [
        int(amplitude * math.sin(2 * math.pi * freq * t / sample_rate))
        for t in range(samples)
    ]

def encode_text_to_wav(input_txt, output_wav, bit_duration=0.1):
    with open(input_txt, 'r', encoding='utf-8') as f:
        text = f.read()

    binary_data = text_to_binary(text)
    freq_map = {'0': 440, '1': 880}
    sample_rate = 44100
    signal = []

    for bit in binary_data:
        signal.extend(generate_tone(freq_map[bit], bit_duration))

    with wave.open(output_wav, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
        for sample in signal:
            wav_file.writeframes(struct.pack('<h', sample))

encode_text_to_wav('input.txt', 'output.wav')