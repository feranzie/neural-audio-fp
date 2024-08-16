import csv
import re

def process_segments(input_csv, output_csv):
    # Dictionary to hold concatenated segments
    segments_dict = {}

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header if there is one

        for row in reader:
            query, answer, score = row
            score = float(score)

            # Extract segment number from the query
            match = re.search(r'segment_(\d+)', query)
            if match:
                segment_number = int(match.group(1))
                # Create a key based on the answer
                key = (answer, segment_number)

                if key not in segments_dict:
                    segments_dict[key] = {
                        'query_segments': [segment_number],
                        'max_score': score,
                        'start_time': int(query.split('_')[-1].split('-')[0]),
                        'end_time': int(query.split('_')[-1].split('-')[1].split('.')[0])
                    }
                else:
                    # Update the max score if current score is higher
                    segments_dict[key]['max_score'] = max(segments_dict[key]['max_score'], score)
                    segments_dict[key]['query_segments'].append(segment_number)

                    # Update the end time based on the new segment
                    segments_dict[key]['end_time'] = int(query.split('_')[-1].split('-')[1].split('.')[0])

    # Write the results to the output CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['query', 'answer', 'score'])  # Write header

        for (answer, _), data in segments_dict.items():
            # Create concatenated query
            concatenated_segments = '+'.join(map(str, data['query_segments']))
            new_query = f"../TestOlafRN/Recordings/new/s-CZWGsZK4_2024-03-01_17-00-02.mp3/segment_{concatenated_segments}_{data['start_time']}-{data['end_time']}.mp3"
            writer.writerow([new_query, answer, data['max_score']])

if __name__ == "__main__":
    input_csv_file = 'input.csv'  # Replace with your input CSV file path
    output_csv_file = 'output.csv'  # Replace with your desired output CSV file path
    process_segments(input_csv_file, output_csv_file)