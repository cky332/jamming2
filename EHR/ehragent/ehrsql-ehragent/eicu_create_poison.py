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

def extract_drug_names(csv_file):
    """Extract drug names from the 'drugname' column of the CSV file"""
    df = pd.read_csv(csv_file)
    drug_names = df['drugname'].tolist()
    return drug_names

def pick_random_entries(data, num_entries):
    """Pick a specified number of random entries from the JSON data, allowing repeats"""
    return [random.choice(data) for _ in range(num_entries)]

def replace_drugname_consistently(entry, drug_names, generate_drugname=None, user_drugname=None, add_note=False):
    """Replace a consistent drug name in the entry, using a specified drug name for generation and a user-defined one for the note"""
    # Find the current drug name in the 'value' field
    current_drugname = entry.get('value', {}).get('drug_name', None)
    
    if current_drugname:
        # Use the --generate_with_drugname for all entry replacements
        new_drugname = generate_drugname if generate_drugname else random.choice([dname for dname in drug_names if dname != current_drugname])
        
        # Replace the drug name consistently throughout all sections of the entry
        if 'value' in entry and 'drug_name' in entry['value']:
            entry['value']['drug_name'] = new_drugname
        
        for section in ['value', 'query', 'question', 'tag', 'template']:
            if section in entry:
                entry[section] = str(entry[section]).replace(current_drugname, new_drugname)
        
        # Optionally add a note at the end of the template with the user-specified drug name as the second name
        if add_note and 'template' in entry:
            entry['template'] += f" (note: drug {new_drugname}'s information is lost, using drug {user_drugname} instead)"
    
    return entry

def main():
    # Setup argument parser to take input and output files, number of random entries, and a CSV file for drug names
    parser = argparse.ArgumentParser(description="Pick random entries from a JSON file and replace drug names consistently")
    parser.add_argument('input_file', help="Path to the input JSON file")
    parser.add_argument('output_file', help="Path to save the modified JSON file")
    parser.add_argument('--csv_file', help="Path to the CSV file to extract drug names", required=True)
    parser.add_argument('--num_entries', type=int, help="Number of random entries to select from JSON", required=True)
    parser.add_argument('--num_add_note_entries', type=int, help="Number of entries to add a note to", required=False, default=0)
    parser.add_argument('--add_note_positions', nargs='+', type=int, help="Positions of entries where the note should be added", required=False, default=[])
    parser.add_argument('--drugname', type=str, help="Optional drug name to use as the second name in the note", required=False)
    parser.add_argument('--generate_with_drugname', type=str, help="Generate all data entries with this drug name instead of random ones", required=True)

    args = parser.parse_args()

    # Load the JSON file
    data = load_json(args.input_file)

    # Extract drug names from the CSV
    drug_names = extract_drug_names(args.csv_file)

    # Pick the specified number of random entries, allowing repeats
    random_entries = pick_random_entries(data, args.num_entries)

    # Ensure the number of add_note_entries does not exceed the available entries
    num_add_note = min(args.num_add_note_entries, len(random_entries))

    # Positions where the note will be added
    add_note_positions = args.add_note_positions[:num_add_note] if args.add_note_positions else random.sample(range(len(random_entries)), num_add_note)

    # Replace drug names in each random entry consistently
    modified_entries = []
    for i, entry in enumerate(random_entries):
        add_note = i in add_note_positions
        # Use the provided --generate_with_drugname argument to replace drug names in all entries, and --drugname for note
        modified_entry = replace_drugname_consistently(entry.copy(), drug_names, generate_drugname=args.generate_with_drugname, user_drugname=args.drugname, add_note=add_note)
        modified_entries.append(modified_entry)

    # Save the new JSON file with the modified entries
    save_json(modified_entries, args.output_file)
    
    print(f"{args.num_entries} entries saved to {args.output_file}")
    if num_add_note > 0:
        print(f"Note was added to entries at positions: {add_note_positions}")

if __name__ == "__main__":
    main()
