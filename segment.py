from pydub import AudioSegment
import os
import argparse
import re

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Split an audio file into segments.')

# Add arguments for input directory, output directory, and audio file
parser.add_argument('--input_dir', type=str, required=True, help='Path to the input directory containing the audio file.')
parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory for the segments.')
parser.add_argument('--audio_file', type=str, required=True, help='Name of the audio file to be split.')

# Parse the command-line arguments
args = parser.parse_args()

# Set the input and output directories from the parsed arguments
input_dir = args.input_dir
output_dir = args.output_dir

# Set the audio file name from the parsed arguments
audio_file = args.audio_file

# Create the full path to the audio file
audio_path = os.path.join(input_dir, audio_file)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Extract start and stop timestamps from the input file name
# This assumes the file name ends with "_start_stop.mp3"
match = re.search(r'_(\d+)_(\d+)\.mp3$', audio_file)
if not match:
    raise ValueError("Audio file name must end with '_start_stop.mp3' where start and stop are timestamps in milliseconds.")

start_time = int(match.group(1))  # Extract the start time from the file name
stop_time = int(match.group(2))   # Extract the stop time from the file name

# Load the audio file
audio = AudioSegment.from_file(audio_path, format='mp3')

# Set the segment duration in milliseconds
segment_duration = 3000  # 3 seconds

# Calculate the number of segments
num_segments = len(audio) // segment_duration

# Split the audio into segments and update their names with correct timestamps
for i in range(num_segments):
    start = i * segment_duration
    end = start + segment_duration
    segment = audio[start:end]
    
    # Calculate actual timestamps relative to the start_time
    segment_start_time = start_time + start
    segment_end_time = start_time + end
    
    # Export the segment with updated timestamps in the name
    segment.export(os.path.join(output_dir, f'{audio_file}_segment_{i+1}_{segment_start_time}-{segment_end_time}.mp3'), format='mp3')

# Handle any remaining audio that doesn't fill a complete segment
if len(audio) % segment_duration != 0:
    start = num_segments * segment_duration
    segment = audio[start:]
    
    # Calculate actual timestamps for the remaining audio
    segment_start_time = start_time + start
    segment_end_time = start_time + len(audio)
    
    segment.export(os.path.join(output_dir, f'{audio_file}_segment_{num_segments + 1}_{segment_start_time}-{segment_end_time}.mp3'), format='mp3')

print(f'Audio file split into {num_segments + (1 if len(audio) % segment_duration != 0 else 0)} segments.')
