import pandas as pd
import re

# Load the CSV file
file_path = '2s_detail.csv'
df = pd.read_csv(file_path, header=None)

# Function to extract the segment number and timestamp from the query
def extract_segment_info(query):
    segment_match = re.search(r'segment_(\d+)', query)
    timestamp_match = re.search(r'_(\d+)-(\d+)\.mp3', query)
    if segment_match and timestamp_match:
        segment_number = int(segment_match.group(1))
        start_time = int(timestamp_match.group(1))
        end_time = int(timestamp_match.group(2))
        return segment_number, start_time, end_time
    return None, None, None

# Function to extract the base path (removing the segment and timestamp)
def extract_base_path(query):
    path_match = re.match(r'(.+/s-CZWGsZK4_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.mp3', query)
    if path_match:
        base_path = path_match.group(1) + ".mp3"
        return base_path
    return query

# Function to convert milliseconds to hh:mm:ss:ms format
def ms_to_time_format(milliseconds):
    seconds, ms = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(ms):03}"

# Initialize variables to store the processed data
combined_rows = []

# Iterate through the rows of the dataframe
prev_query, prev_answer, prev_start, prev_end, prev_score = None, None, None, None, None

for index, row in df.iterrows():
    # Skip header row
    if index == 0:
        continue
    
    query, answer, score = row[0], row[1], float(row[2])
    segment_number, start_time, end_time = extract_segment_info(query)
    
    if prev_answer == answer and prev_end == start_time:
        # Update the end time and score
        prev_end = end_time
        prev_score = max(prev_score, score)
    else:
        # Save the previous combined row with the base path and time format conversion
        if prev_query:
            base_query = extract_base_path(prev_query)
            start_time_formatted = ms_to_time_format(prev_start)
            end_time_formatted = ms_to_time_format(prev_end)
            combined_rows.append([base_query, prev_answer, prev_score, start_time_formatted, end_time_formatted])
        # Update the previous row variables
        prev_query = query
        prev_answer = answer
        prev_start = start_time
        prev_end = end_time
        prev_score = score

# Save the last combined row with the base path and time format conversion
if prev_query:
    base_query = extract_base_path(prev_query)
    start_time_formatted = ms_to_time_format(prev_start)
    end_time_formatted = ms_to_time_format(prev_end)
    combined_rows.append([base_query, prev_answer, prev_score, start_time_formatted, end_time_formatted])

# Convert the combined rows into a dataframe with formatted start and stop times
combined_df = pd.DataFrame(combined_rows, columns=['query', 'answer', 'score', 'query_start', 'query_stop'])

# Save the processed data to a new CSV file
combined_df.to_csv('2s_processed_file_with_formatted_times.csv', index=False)

# Show the combined data
combined_df.head()
