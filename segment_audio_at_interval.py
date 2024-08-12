from pydub import AudioSegment
import os

# Set the input and output directories
input_dir = 'path/to/input/directory'

# Set the audio file name
audio_file = 's-CZWGsZK4_2024-03-01_20-00-04.mp3'

output_dir =f"new/{audio_file}"
os.makedirs(output_dir, exist_ok=True)

# Load the audio file
audio = AudioSegment.from_file(os.path.join(audio_file), format='mp3')

# Set the segment duration in milliseconds
segment_duration = 1000  # 5 seconds                                                                                                                                    
# Calculate the number of segments
num_segments = len(audio) // segment_duration

# Split the audio into segments
for i in range(num_segments):
    start = i * segment_duration
    end = start + segment_duration
    segment = audio[start:end]
    segment.export(os.path.join(output_dir, f'segment_{i+1}.mp3'), format='mp3')

print(f'Audio file split into {num_segments} segments.')