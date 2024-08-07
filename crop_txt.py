from pydub import AudioSegment
import os

audio_files = [
    "rai1_20211015000000_20211015020000",
    "rai1_20211015020000_20211015040000",
    "rai1_20211015040000_20211015060000",
    "rai1_20211015060000_20211015080000",
    "rai1_20211015080000_20211015100000",
    "rai1_20211015100000_20211015120000",
    "rai1_20211015120000_20211015140000",
    "rai1_20211015140000_20211015160000",
    "rai1_20211015160000_20211015180000",
    "rai1_20211015180000_20211015200000",
    "rai1_20211015200000_20211015220000",
    "rai1_20211015220000_20211016000000",
    "rai1_20211016000000_20211016020000",
    "rai1_20211016020000_20211016040000",
    "rai1_20211016040000_20211016060000",
    "rai1_20211016060000_20211016080000",
    "rai1_20211016080000_20211016100000",
    "rai1_20211016100000_20211016120000",
    "rai1_20211016120000_20211016140000",
    "rai1_20211016140000_20211016160000",
    "rai1_20211016160000_20211016180000",
    "rai1_20211016180000_20211016200000",
    "rai1_20211016200000_20211016220000",
    "rai1_20211017000000_20211017020000",
    "rai1_20211017020000_20211017040000",
    "rai1_20211017040000_20211017060000",
    "rai1_20211017060000_20211017080000",
    "rai1_20211017080000_20211017100000",
    "rai1_20211017100000_20211017120000",
    "rai1_20211017120000_20211017140000",
    "rai1_20211017140000_20211017160000",
    "rai1_20211017160000_20211017180000",
    "rai1_20211017180000_20211017200000",
    "rai1_20211017200000_20211017220000",
    "rai1_20211017220000_20211018000000"
]
for j in audio_files:
    file_name=j
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

        print (f" audio file:{j}, start_time: {start_time}, end_time: {end_time}, audio_class: {audio_class} ")
        # Load the audio file and extract the clip
        audio = AudioSegment.from_file(input_audio_file)
        audio_clip = audio[start_time:end_time]

        # Save the clip to the appropriate folder
        if audio_class == 1:
            audio_clip.export(f"Noise/{j}_clip_{i+1}.mp3", format="mp3")
        elif audio_class == 2:
            audio_clip.export(f"Music/{j}_clip_{i+1}.mp3", format="mp3")

    print(f"Audio clips have been split and saved successfully for {j}.")

    print("Audio clips have been split and saved successfully.")


