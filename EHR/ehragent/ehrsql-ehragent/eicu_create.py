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

def replace_drug_names_in_entry(entry, drug_names):
    """Replace drug names in the entry with different ones from the CSV, consistently."""
    # Extract the current drug name from `value['drug_name']`
    current_drug_name = entry.get('value', {}).get('drug_name', None)
    
    if current_drug_name:
        # Select a new drug name that is different from the current one
        possible_replacements = [dname for dname in drug_names if dname != current_drug_name]
        if possible_replacements:
            new_drug_name = random.choice(possible_replacements)
            
            # Replace drug name consistently in relevant sections
            if 'value' in entry and 'drug_name' in entry['value']:
                entry['value']['drug_name'] = new_drug_name
            
            for field in ['question', 'template', 'query', 'tag']:
                if field in entry:
                    entry[field] = str(entry[field]).replace(current_drug_name, new_drug_name)
            
            # Replace in list-based fields (e.g., `q_tag`, `t_tag`, `o_tag`) if applicable
            for field in ['q_tag', 't_tag', 'o_tag']:
                if field in entry and isinstance(entry[field], list):
                    entry[field] = [str(item).replace(current_drug_name, new_drug_name) for item in entry[field]]

    # Ensure 'value' updates consistently for nested fields
    if 'value' in entry:
        for key, value in entry['value'].items():
            if isinstance(value, str) and current_drug_name in value:
                entry['value'][key] = value.replace(current_drug_name, new_drug_name)

    return entry

def main():
    # Setup argument parser to take input and output files, number of random entries, and a CSV file for drug names
    parser = argparse.ArgumentParser(description="Pick random entries from a JSON file and replace drug names consistently")
    parser.add_argument('input_file', help="Path to the input JSON file")
    parser.add_argument('output_file', help="Path to save the modified JSON file")
    parser.add_argument('--csv_file', help="Path to the CSV file to extract drug names", required=True)
    parser.add_argument('--num_entries', type=int, help="Number of random entries to select from JSON", required=True)
    
    args = parser.parse_args()

    # Load the JSON file
    data = load_json(args.input_file)

    # Extract drug names from the CSV
    drug_names = extract_drug_names(args.csv_file)

    # Pick the specified number of random entries, allowing repeats
    random_entries = pick_random_entries(data, args.num_entries)

    # Replace drug names in each random entry consistently
    modified_entries = []
    for entry in random_entries:
        modified_entry = replace_drug_names_in_entry(entry.copy(), drug_names)
        modified_entries.append(modified_entry)

    # Save the new JSON file with the modified entries
    save_json(modified_entries, args.output_file)
    
    print(f"{args.num_entries} randomly modified entries saved to {args.output_file}")

if __name__ == "__main__":
    main()