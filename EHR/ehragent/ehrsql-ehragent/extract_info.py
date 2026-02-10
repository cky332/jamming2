import json
import re

def extract_patient_entries_by_question(file_path):
    # Open and load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # List to store entries where "patient" followed by a number is mentioned in the question
    patient_entries = []

    # Define a regular expression pattern to match "patient" followed by a number
    pattern = re.compile(r'patient\s*\d+', re.IGNORECASE)

    # Iterate over the entries in the JSON file
    for entry in data:
        # Check if 'question' matches the pattern
        if 'question' in entry and pattern.search(entry['question']):
            patient_entries.append(entry)

    return patient_entries

def save_patient_entries(patient_entries, output_file):
    # Save the extracted entries to a new file
    with open(output_file, 'w') as f:
        json.dump(patient_entries, f, indent=4)

# Example usage
if __name__ == "__main__":
    file_path = "mimic_iii/valid_filtered_20240104.json"  # Update with the actual path
    output_file = "mimic_iii/patient_only.json"

    # Extract entries where "patient" followed by a number is mentioned in the question
    patient_entries = extract_patient_entries_by_question(file_path)

    # Print the number of entries found
    print(f"Found {len(patient_entries)} entries where 'patient' followed by a number is mentioned in the question")

    # Save the entries to a new file
    save_patient_entries(patient_entries, output_file)
    print(f"Entries saved to {output_file}")


