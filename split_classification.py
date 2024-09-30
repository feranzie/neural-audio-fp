import pandas as pd
from pydub import AudioSegment
import os
from datetime import timedelta

# Load the CSV file
df = pd.read_csv('s-CZWGsZK4_2024-09-24_17-00-03_results_mark.csv')

# Convert 'start' and 'end' columns to timedelta
df['start'] = pd.to_timedelta(df['start'])
df['end'] = pd.to_timedelta(df['end'])

# df['start_seconds'] = pd.to_timedelta(df['start']).dt.total_seconds()
# df['end_seconds'] = pd.to_timedelta(df['end']).dt.total_seconds()

# # cc=[]
# # for i in range(len(df)):
# #     bb=df.iloc[i]["path"] +"_"+ str(df.iloc[i]["start_seconds"])+ "_" +str(df.iloc[i]["end_seconds"])
# #     cc.append(bb)
# # df["combined"]=cc

# Path to the original audio file
audio_file_path = 's-CZWGsZK4_2024-09-24_17-00-03.mp3'  # Replace with your actual audio file path

# Load the audio file
audio = AudioSegment.from_file(audio_file_path)

# Create output directories if they do not exist
output_dir_music = 'bmusic_segments'
output_dir_no_music = 'bno_music_segments'

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
        output_dir = output_dir_music
    else:
        output_dir = output_dir_no_music
    print(index)

    # Export the segment to the appropriate directory
    segment.export(os.path.join(output_dir, f'{audio_file_path}_{start_time}_{end_time}.mp3'), format='mp3')