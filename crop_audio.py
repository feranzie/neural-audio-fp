import os
import pandas as pd
from pydub import AudioSegment

# Read the spreadsheet
df = pd.read_excel('audio_files.xlsx')

# Define a dictionary to map class numbers to folder names
class_folders = {
    1: "foreground_music",
    2: "background_music",
    3: "only_music",
    4: "isolated_non_music",
    5: "similar_speech_music",
    6: "igb_music"
}

# Create directories for each class if they do not exist
for folder in class_folders.values():
    os.makedirs(folder, exist_ok=True)

# Function to crop audio file
def crop_audio(file_name, start_time, end_time, output_folder):
    audio = AudioSegment.from_file(file_name)
    start_ms = start_time * 1000  # Convert to milliseconds
    end_ms = end_time * 1000  # Convert to milliseconds
    cropped_audio = audio[start_ms:end_ms]
    output_path = os.path.join(output_folder, os.path.basename(file_name))
    cropped_audio.export(output_path, format="mp3")

# Process each row in the dataframe
for index, row in df.iterrows():
    file_name = row['file_name']
    time_start = row['time_start']
    time_end = row['time_end']
    class_number = row['class']

    output_folder = class_folders.get(class_number, "others")
    crop_audio(file_name, time_start, time_end, output_folder)

print("Audio files have been processed and saved into respective folders.")
