# Here's a simple Python setup using PyAudio and Librosa to detect the adhan prayer and play the inverted WAV file. This assumes you’ve got the inverted adhan file ready from Audacity.
# Install Dependencies: Run pip install pyaudio librosa numpy in your terminal.
# Install Voicemeeter Banana from VB-Audio. Route your mic to input 1, set the inverted WAV playback to output through your speakers. In Voicemeeter, select “VB-Audio Virtual Cable” as the output device for the script.
# Place your mic near the adhan source, run python adhan_cancel.py. It listens for the adhan’s unique MFCC (audio fingerprint), and when it detects a match, it plays the inverted file.
# Tweak the 0.8 correlation threshold if it’s too sensitive or misses the adhan.
# You’ll need the original adhan file (original_adhan.wav) for reference—grab it from Pixabay or record it.
# Test in a quiet environment first to avoid false triggers.
import pyaudio
import librosa
import numpy as np
import wave
import time

# Load your inverted adhan file
inverted_file = "inverted_adhan.wav"
# Reference adhan for detection
reference_file = "original_adhan.wav"

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100

# Load reference adhan for fingerprinting
y_ref, sr = librosa.load(reference_file, sr=RATE)
mfcc_ref = librosa.feature.mfcc(y=y_ref, sr=sr, n_mfcc=13)

def detect_adhan(stream, p):
    print("Listening for adhan...")
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.float32)
        mfcc = librosa.feature.mfcc(y=audio, sr=RATE, n_mfcc=13)
        # Simple correlation check (tweak threshold as needed)
        correlation = np.corrcoef(mfcc_ref.flatten(), mfcc.flatten())[0, 1]
        if correlation > 0.8:  # Adjust threshold
            print("Adhan detected! Playing inverted...")
            play_inverted(p)
            break

def play_inverted(p):
    wf = wave.open(inverted_file, 'rb')
    stream_out = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream_out.write(data)
        data = wf.readframes(CHUNK)
    stream_out.stop_stream()
    stream_out.close()

# Initialize PyAudio
p = pyaudio.PyAudio()
stream_in = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Start detection
detect_adhan(stream_in, p)

# Cleanup
stream_in.stop_stream()
stream_in.close()
p.terminate()
