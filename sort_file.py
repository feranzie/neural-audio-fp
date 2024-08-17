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
        # Combine segments and update the end_time and score
        combined_query = f"{prev_query.split('_')[0]}_{prev_start}-{end_time}.mp3"
        prev_query = combined_query
        prev_end = end_time
        prev_score = max(prev_score, score)
    else:
        # Save the previous combined row with start and stop times
        if prev_query:
            combined_rows.append([prev_query, prev_answer, prev_score, prev_start, prev_end])
        # Update the previous row variables
        prev_query = query
        prev_answer = answer
        prev_start = start_time
        prev_end = end_time
        prev_score = score

# Save the last combined row with start and stop times
if prev_query:
    combined_rows.append([prev_query, prev_answer, prev_score, prev_start, prev_end])

# Convert the combined rows into a dataframe with start and stop columns
combined_df = pd.DataFrame(combined_rows, columns=['query', 'answer', 'score', 'query_start', 'query_stop'])

# Save the processed data to a new CSV file
combined_df.to_csv('2s_processed_file_with_times.csv', index=False)

# Show the combined data
combined_df.head()
