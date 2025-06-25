
import wave
import struct
import math

SAMPLE_RATE = 44100
AMPLITUDE = 16000
BIT_DURATION = 0.2  # seconds per bit
FREQ_0 = 1000
FREQ_1 = 2000
PREAMBLE_FREQ = 3000
PREAMBLE_DURATION = 1.0  # seconds

def generate_tone(freq, duration):
    samples = int(SAMPLE_RATE * duration)
    return [
        int(AMPLITUDE * math.sin(2 * math.pi * freq * t / SAMPLE_RATE))
        for t in range(samples)
    ]

def text_to_bits(text):
    return ''.join(f'{ord(c):08b}' for c in text + '\0')

def encode_to_wav(text, filename='encoded.wav'):
    audio = []

    # Preamble tone
    audio += generate_tone(PREAMBLE_FREQ, PREAMBLE_DURATION)

    # Encode each bit
    for bit in text_to_bits(text):
        freq = FREQ_0 if bit == '0' else FREQ_1
        audio += generate_tone(freq, BIT_DURATION)

    # Save to WAV
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
        for s in audio:
            wav_file.writeframes(struct.pack('<h', s))

if __name__ == '__main__':
    message = input("Enter message to encode: ")
    encode_to_wav(message)
    print("Saved to encoded.wav")
