import pandas as pd
import re
import argparse
import os 
# Define the command-line arguments
parser = argparse.ArgumentParser(description='Process CSV file and save the processed data.')
parser.add_argument('--input', type=str, help='Path to the input CSV file', required=True)
parser.add_argument('--output', type=str, help='Path to the output CSV file', required=True)
args = parser.parse_args()

# Load the CSV file
file_path = args.input
df = pd.read_csv(file_path)

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

# Function to extract the base path (taking the text before .mp3)
def extract_base_path(query):
    base_path = query.split('.mp3')[0] + ".mp3"
    return base_path

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

start_t=[]
end_t=[]
print(df.iloc[0])
for index, row in df.iterrows():

    query, answer, score = row[0], row[1], float(row[2])
    segment_number, start_time, end_time = extract_segment_info(query)
    start_t.append(start_time)
    end_t.append(end_time)

df['start_time']=start_t
df["end_time"]=end_t
df = df.sort_values(by='start_time', ascending=True)



for index, row in df.iterrows():
    
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

# Replace answers with "unknown audio" for scores below 0.51
combined_df.loc[combined_df['score'] < 0.51, 'answer'] = "unknown audio"

# Convert query_start and query_stop back to milliseconds for duration calculation
combined_df['query_start_ms'] = combined_df['query_start'].apply(lambda x: sum(int(t) * 1000 ** i for i, t in enumerate(reversed(x.split(':')))))
combined_df['query_stop_ms'] = combined_df['query_stop'].apply(lambda x: sum(int(t) * 1000 ** i for i, t in enumerate(reversed(x.split(':')))))

# Calculate the duration in milliseconds
combined_df['duration_ms'] = combined_df['query_stop_ms'] - combined_df['query_start_ms']

# Drop rows where the duration is less than 3000 ms (3 seconds)
combined_df = combined_df[combined_df['duration_ms'] >= 3000]

# Drop the temporary columns used for calculation
combined_df = combined_df.drop(columns=['query_start_ms', 'query_stop_ms', 'duration_ms'])


output_dir = os.path.dirname(args.output)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Save the processed data to a new CSV file
output_file_path = args.output
combined_df.to_csv(output_file_path, index=False)

# Show the combined data
combined_df.head()
