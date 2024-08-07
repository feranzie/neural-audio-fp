from pydub import AudioSegment
import os


file_name="rai1_20211017120000_20211017140000"
# Load the input audio file
input_audio_file = f"{file_name}.mp3"  # Replace with your audio file

# Create directories for music and noise
os.makedirs("Music", exist_ok=True)
os.makedirs("Noise", exist_ok=True)

# Read the timestamps and audio classes from the text file
with open(f"{file_name}.txt", "r") as f:  # Replace with your txt file
    lines = f.readlines()

# Iterate through each row and process the audio
for i, line in enumerate(lines):
    start_time, end_time, audio_class = line.strip().split()
    start_time = float(start_time) * 1000  # Convert to milliseconds
    end_time = float(end_time)* 1000  # Convert to milliseconds
    audio_class = int(audio_class)

    print (f"start_time: {start_time}, end_time: {end_time}, audio_class: {audio_class} ")
    # Load the audio file and extract the clip
    audio = AudioSegment.from_file(input_audio_file)
    audio_clip = audio[start_time:end_time]

    # Save the clip to the appropriate folder
    if audio_class == 1:
        audio_clip.export(f"Noise/clip_{i+1}.mp3", format="mp3")
    elif audio_class == 2:
        audio_clip.export(f"Music/clip_{i+1}.mp3", format="mp3")

print("Audio clips have been split and saved successfully.")