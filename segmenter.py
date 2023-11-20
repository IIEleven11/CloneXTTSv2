import auditok

# Load audio file
audio_regions = auditok.split(
    "/home/pathtowavfile.wav",
    min_dur=2,  # minimum duration of a valid audio event in seconds
    max_dur=12,  # maximum duration of an event
    max_silence=0.3,  # maximum duration of tolerated continuous silence within an event
    energy_threshold=35  # threshold of detection
)

# Save regions to separate audio files
for i, region in enumerate(audio_regions):
    region.save(f"/home/pathtosavewavfilesegments/audio{i}.wav")
