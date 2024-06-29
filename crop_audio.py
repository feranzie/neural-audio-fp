import os
import pandas as pd
from pydub import AudioSegment

# Read the spreadsheet
df = pd.read_excel('report_2804.xlsx')

# Print the first few rows to inspect the data before conversion
print("Initial DataFrame:")
print(df.head())

# Function to convert HH:MM:SS to total seconds
def time_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except Exception as e:
        print(f"Error converting time '{time_str}': {e}")
        return None

# Apply the conversion function to Time_start and Time_end
df['Time_start'] = df['Time_start'].apply(time_to_seconds)
df['Time_end'] = df['Time_end'].apply(time_to_seconds)

# Print the first few rows after conversion to inspect NaN values
print("DataFrame after conversion to seconds:")
print(df.head())

# Print rows where conversion failed
print("Rows with NaN in Time_start or Time_end after conversion:")
print(df[df['Time_start'].isna() | df['Time_end'].isna()])

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
    try:
        audio = AudioSegment.from_file(file_name)
        start_ms = start_time * 1000  # Convert to milliseconds
        end_ms = end_time * 1000  # Convert to milliseconds
        cropped_audio = audio[start_ms:end_ms]
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        output_path = os.path.join(output_folder, f"{base_name}_{start_time}-{end_time}.mp3")
        cropped_audio.export(output_path, format="mp3")
        print(f"Exported {output_path}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Process each row in the dataframe
for index, row in df.iterrows():
    file_name = row['Program']
    time_start = row['Time_start']
    time_end = row['Time_end']
    class_number = row['Class']

    # Validate the row data
    if pd.isna(file_name) or pd.isna(time_start) or pd.isna(time_end) or pd.isna(class_number):
        print(f"Skipping row {index} due to missing data: {row}")
        continue

    output_folder = class_folders.get(class_number, "others")
    crop_audio(file_name, time_start, time_end, output_folder)

print("Audio files have been processed and saved into respective folders.")
