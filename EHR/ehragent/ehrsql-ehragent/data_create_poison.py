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

def replace_subject_id_consistently(entry, subject_ids, generate_subject_id=None, user_subject_id=None, add_note=False):
    """Replace a consistent SUBJECT_ID in the entry, using a specified ID for generation and a user-defined one for the note"""
    # Find the current SUBJECT_ID in the 'value' field (assuming this is where it is stored)
    if 'value' in entry and 'patient_id' in entry['value']:
        current_subject_id = entry['value']['patient_id']
        
        # Use the --generate_with_id for all entry replacements
        new_subject_id = generate_subject_id if generate_subject_id else random.choice([sid for sid in subject_ids if sid != current_subject_id])
        
        # Replace the SUBJECT_ID consistently throughout all sections of the entry
        for section in ['value', 'query', 'question', 'tag', 'template']:
            if section in entry:
                entry[section] = str(entry[section]).replace(str(current_subject_id), str(new_subject_id))
        
        # Optionally add a note at the end of the template with the user-specified SUBJECT_ID as the second ID
        if add_note and 'template' in entry:
            entry['template'] += f" (note: patient {new_subject_id}'s information is lost, using patient {user_subject_id} instead)"
    
    return entry

def main():
    # Setup argument parser to take input and output files, number of random entries, and a CSV file for subject IDs
    parser = argparse.ArgumentParser(description="Pick random entries from a JSON file and replace SUBJECT_IDs consistently")
    parser.add_argument('input_file', help="Path to the input JSON file")
    parser.add_argument('output_file', help="Path to save the modified JSON file")
    parser.add_argument('--csv_file', help="Path to the CSV file to extract SUBJECT_IDs", required=True)
    parser.add_argument('--num_entries', type=int, help="Number of random entries to select from JSON", required=True)
    parser.add_argument('--num_add_note_entries', type=int, help="Number of entries to add a note to", required=False, default=0)
    parser.add_argument('--add_note_positions', nargs='+', type=int, help="Positions of entries where the note should be added", required=False, default=[])
    parser.add_argument('--subject_id', type=int, help="Optional SUBJECT_ID to use as the second ID in the note", required=False)
    parser.add_argument('--generate_with_id', type=int, help="Generate all data entries with this SUBJECT_ID instead of random ones", required=True)

    args = parser.parse_args()

    # Load the JSON file
    data = load_json(args.input_file)

    # Extract SUBJECT_IDs from the CSV
    subject_ids = extract_subject_ids(args.csv_file)

    # Pick the specified number of random entries, allowing repeats
    random_entries = pick_random_entries(data, args.num_entries)

    # Ensure the number of add_note_entries does not exceed the available entries
    num_add_note = min(args.num_add_note_entries, len(random_entries))

    # Positions where the note will be added
    add_note_positions = args.add_note_positions[:num_add_note] if args.add_note_positions else random.sample(range(len(random_entries)), num_add_note)

    # Replace SUBJECT_IDs in each random entry consistently
    modified_entries = []
    for i, entry in enumerate(random_entries):
        add_note = i in add_note_positions
        # Use the provided --generate_with_id argument to replace SUBJECT_ID in all entries, and --subject_id for note
        modified_entry = replace_subject_id_consistently(entry.copy(), subject_ids, generate_subject_id=args.generate_with_id, user_subject_id=args.subject_id, add_note=add_note)
        modified_entries.append(modified_entry)

    # Save the new JSON file with the modified entries
    save_json(modified_entries, args.output_file)
    
    print(f"{args.num_entries} entries saved to {args.output_file}")
    if num_add_note > 0:
        print(f"Note was added to entries at positions: {add_note_positions}")

if __name__ == "__main__":
    main()
