import json
import re

def extract_specific_patient_questions(file_path, patient_number):
    # Open and load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)

    # List to store entries where the specific patient number is mentioned
    patient_entries = []

    # Define a regular expression pattern to match "patient" followed by the specific number
    pattern = re.compile(rf'patient\s*{patient_number}', re.IGNORECASE)

    # Iterate over the entries in the JSON file
    for entry in data:
        # Check if 'question' matches the pattern with the specific patient number
        if 'question' in entry and pattern.search(entry['question']):
            patient_entries.append(entry)

    return patient_entries

def save_patient_entries(patient_entries, output_file):
    # Save the extracted entries to a new file
    with open(output_file, 'w') as f:
        json.dump(patient_entries, f, indent=4)

# Example usage
if __name__ == "__main__":
    file_path = "mimic_iii/patient_only.json"  # Update with the actual path
    patient_number = 62298  # Replace with the specific patient number
    output_file = f"mimic_iii/patients/patient_{patient_number}.json"

    # Extract entries where the specific patient number is mentioned in the question
    patient_entries = extract_specific_patient_questions(file_path, patient_number)

    # Print the number of entries found
    print(f"Found {len(patient_entries)} entries mentioning patient {patient_number}")

    # Save the entries to a new file
    save_patient_entries(patient_entries, output_file)
    print(f"Entries saved to {output_file}")
