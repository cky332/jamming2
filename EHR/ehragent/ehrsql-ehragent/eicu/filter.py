import csv
import json

# Load drug names from the CSV file
csv_file_path = 'medication.csv'
json_file_path = 'valid.json'
output_file_path = 'filtered_valid.json'

# Read drug names from CSV
drug_names = set()
with open(csv_file_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        drug_name = row['drugname'].strip().lower()  # Lowercase for case-insensitive matching
        drug_names.add(drug_name)

# Load JSON data
with open(json_file_path, 'r') as json_file:
    questions_data = json.load(json_file)

# Filter JSON entries based on drug names
filtered_questions = [
    entry for entry in questions_data
    if entry.get('value', {}).get('drug_name', '').strip().lower() in drug_names
]

# Write filtered data to a new JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(filtered_questions, output_file, indent=4)

print(f"Filtered data saved to {output_file_path}")
