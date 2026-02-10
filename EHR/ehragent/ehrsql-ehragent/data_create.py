import json
import argparse
import pandas as pd
import random

def load_json(file_path):
    """Load the JSON file"""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, output_file):
    """Save the modified JSON file"""
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def extract_subject_ids(csv_file):
    """Extract data from SUBJECT_ID section of CSV file"""
    df = pd.read_csv(csv_file)
    subject_ids = df['SUBJECT_ID'].tolist()
    return subject_ids

def pick_random_entries(data, num_entries):
    """Pick a specified number of random entries from the JSON data, allowing repeats"""
    return [random.choice(data) for _ in range(num_entries)]

def replace_subject_id_consistently(entry, subject_ids):
    """Replace a consistent SUBJECT_ID in the entry with a different one from the CSV"""
    # Find the current SUBJECT_ID in the 'value' field (assuming this is where it is stored)
    if 'value' in entry and 'patient_id' in entry['value']:
        current_subject_id = entry['value']['patient_id']
        
        # Select a new SUBJECT_ID that is different from the current one
        new_subject_id = random.choice([sid for sid in subject_ids if sid != current_subject_id])
        
        # Replace the SUBJECT_ID consistently throughout all sections of the entry
        for section in ['value', 'query', 'question', 'tag', 'template']:
            if section in entry:
                entry[section] = str(entry[section]).replace(str(current_subject_id), str(new_subject_id))
    
    return entry

def main():
    # Setup argument parser to take input and output files, number of random entries, and a CSV file for subject IDs
    parser = argparse.ArgumentParser(description="Pick random entries from a JSON file and replace SUBJECT_IDs consistently")
    parser.add_argument('input_file', help="Path to the input JSON file")
    parser.add_argument('output_file', help="Path to save the modified JSON file")
    parser.add_argument('--csv_file', help="Path to the CSV file to extract SUBJECT_IDs", required=True)
    parser.add_argument('--num_entries', type=int, help="Number of random entries to select from JSON", required=True)
    
    args = parser.parse_args()

    # Load the JSON file
    data = load_json(args.input_file)

    # Extract SUBJECT_IDs from the CSV
    subject_ids = extract_subject_ids(args.csv_file)

    # Pick the specified number of random entries, allowing repeats
    random_entries = pick_random_entries(data, args.num_entries)

    # Replace SUBJECT_IDs in each random entry consistently
    modified_entries = []
    for entry in random_entries:
        modified_entry = replace_subject_id_consistently(entry.copy(), subject_ids)
        modified_entries.append(modified_entry)

    # Save the new JSON file with the modified entries
    save_json(modified_entries, args.output_file)
    
    print(f"{args.num_entries} randomly modified entries saved to {args.output_file}")

if __name__ == "__main__":
    main()
