Project Title: Real-Time Active Cancellation of the Adhan (Muslim Call to Prayer)
Goal in one sentence
Automatically detect the adhan when it starts broadcasting from nearby loudspeakers and instantly play a perfectly phase-inverted version through local speakers to cancel it out in real time (active noise cancellation targeted specifically at the call to prayer).
Core components

Exact recording(s) of the local adhan (standard version + Fajr version with “prayer is better than sleep”)
Phase-inverted copies of both created in Audacity
Windows-based real-time system using:
– Python + PyAudio + Librosa for live audio fingerprinting (MFCC correlation)
– Voicemeeter (VB-Audio) for routing and mixing
– Microphone listening to the environment
When the script detects the adhan signature (correlation > threshold), it immediately plays the matching inverted WAV at the same volume and perfect sync to nullify the sound in the room/area.

Current status
Working prototype: manual trigger works perfectly; auto-detection via MFCC fingerprinting functional but needs threshold tuning and separate handling for Fajr adhan.
Basically: Shazam + noise-cancelling headphones, but for the adhan, running 24/7 on a Windows PC
