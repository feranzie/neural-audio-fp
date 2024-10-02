import pandas as pd
from pydub import AudioSegment
import os
from datetime import timedelta

import argparse
import re

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Split all audio files in a folder into segments.')

# Add arguments for input directory and output directory
parser.add_argument('--input', type=str, required=True, help='Path to the input csv ')
parser.add_argument('--output_dir', type=str, required=True, help='Path to the output directory where classification output would be saved.')
parser.add_argument('--audio', type=str, required=True, help='Path to the audio file.')


# Parse the command-line arguments
args = parser.parse_args()

# Set the input and output directories from the parsed arguments
input_csv = args.input
output_dir = args.output_dir
audio_file_path = args.audio

# Load the CSV file
df = pd.read_csv(input_csv)

# Convert 'start' and 'end' columns to timedelta
df['start'] = pd.to_timedelta(df['start'])
df['end'] = pd.to_timedelta(df['end'])

# Load the audio file
audio = AudioSegment.from_file(audio_file_path)

# Create output directories if they do not exist
output_dir_music = os.path.join(output_dir, "music_segments")
output_dir_no_music = os.path.join(output_dir, "no_music_segments") 

os.makedirs(output_dir_music, exist_ok=True)
os.makedirs(output_dir_no_music, exist_ok=True)

# Function to convert timedelta to milliseconds
def timedelta_to_ms(timedelta_obj):
    return int(timedelta_obj.total_seconds() * 1000)

# Iterate over the rows in the DataFrame
for index, row in df.iterrows():
    start_time = timedelta_to_ms(row['start'])
    end_time = timedelta_to_ms(row['end'])
    segment = audio[start_time:end_time]

    # Determine the output directory based on the class
    if row['class'] == 'music':
        output_path = output_dir_music
    else:
        output_path = output_dir_no_music

    # Export the segment to the appropriate directory
    audio_file_name = os.path.basename(audio_file_path)  # Get just the file name
    segment.export(os.path.join(output_path, f'{audio_file_name}_{start_time}_{end_time}.mp3'), format='mp3')

    print(f"Saving segment to: {os.path.join(output_path, f'{audio_file_name}_{start_time}_{end_time}.mp3')}")
