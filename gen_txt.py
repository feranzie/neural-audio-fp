# Define the base directory and file name format
base_dir = "../TestOlafRN/Recordings/new/s-CZWGsZK4_2024-03-01_17-00-02.mp3/"
file_name_format = "segment_{}_{}-{}.mp3"

# Define the output file path
output_file = "file_paths.txt"

# Open the output file in write mode
with open(output_file, "w") as f:
    # Initialize the start and end times
    start_time = 0
    end_time = 5000
    
    # Loop over the segment numbers from 0 to 720
    for segment in range(1, 721):
        # Create the file path
        file_path = base_dir + file_name_format.format(segment, start_time, end_time)
        # Write the file path to the text file
        f.write(file_path + "\n")
        
        # Update the start and end times for the next segment
        start_time = end_time
        end_time += 5000

print(f"File paths written to {output_file}")
