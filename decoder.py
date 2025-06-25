
import pyaudio
import numpy as np

SAMPLE_RATE = 44100
CHUNK = int(SAMPLE_RATE * 0.2)  # match BIT_DURATION
FREQS = [1000, 2000, 3000]

def goertzel(samples, target_freq):
    n = len(samples)
    k = int(0.5 + (n * target_freq) / SAMPLE_RATE)
    omega = (2.0 * np.pi * k) / n
    coeff = 2.0 * np.cos(omega)
    s_prev, s_prev2 = 0.0, 0.0
    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    return s_prev2**2 + s_prev**2 - coeff * s_prev * s_prev2

def listen_and_decode():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("Listening...")

    in_message = False
    bits = ''
    silent_count = 0

    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            powers = {f: goertzel(data, f) for f in FREQS}
            detected = max(powers, key=powers.get)

            if not in_message:
                if detected == FREQS[2]:
                    print("Preamble detected.")
                    in_message = True
                    continue
            else:
                if detected == FREQS[0]:
                    bits += '0'
                elif detected == FREQS[1]:
                    bits += '1'
                else:
                    silent_count += 1
                    if silent_count > 5:
                        break
                    continue
                print(f"Detected bit: {bits[-1]}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        if char == '\0':  # null terminator
            break
        chars.append(char)

    message = ''.join(chars)

    print(f"\nDecoded message: {message}")

if __name__ == '__main__':
    listen_and_decode()
