import webrtcvad
import soundfile as sf
import numpy as np
import os

def audio_segmentation(audio_path, output_dir, segment_length_min, segment_length_max, silence_length):
    # Load audio file
    audio, sample_rate = sf.read(audio_path)
    
    # Initialize VAD
    vad = webrtcvad.Vad(3)  # 3 is the highest aggressiveness setting
    
    # Calculate frame length (10 ms)
    frame_length = int(sample_rate * 0.01)
    
    # Perform VAD
    audio_vad = []
    for i in range(0, len(audio), frame_length):
        frame = audio[i:i+frame_length]
        # Convert frame to 16-bit PCM
        frame = np.short(frame * 32768).tobytes()
        if vad.is_speech(frame, sample_rate):
            audio_vad.append(frame)
    
    # Check if output directory exists and create it if not
    os.makedirs(output_dir, exist_ok=True)
    # Segment audio
    segment = []
    segment_length = 0
    silence_count = 0
    segment_index = 0
    for frame in audio_vad:
        segment.append(np.frombuffer(frame, np.int16))
        segment_length += len(frame) / sample_rate
        if np.mean(np.abs(np.frombuffer(frame, np.int16))) < 200:  # adjust threshold as needed
            silence_count += 1
        else:
            silence_count = 0
        if segment_length > segment_length_max or (segment_length > segment_length_min and silence_count * frame_length / sample_rate > silence_length):
            if segment_length > segment_length_max:
                segment = segment[:int(segment_length_max * sample_rate / 2)]
                segment_length = len(segment) * 2 / sample_rate
            else:
                segment = segment[:-silence_count]
                segment_length -= silence_count * frame_length / sample_rate
            # Write segment to file
            segment_path = os.path.join(output_dir, 'audio{:04d}.wav'.format(segment_index))
            sf.write(segment_path, np.concatenate(segment), sample_rate)
            segment_index += 1
            # Reset segment
            segment = []
            segment_length = 0
            silence_count = 0

# Usage
audio_segmentation('/home/eleven/coquii/MyTTSDataset/largemodel/monoemma16bitmono.wav', '/home/eleven/coquii/WORKFROMHERE/wavs', 3, 20, 0.3)
