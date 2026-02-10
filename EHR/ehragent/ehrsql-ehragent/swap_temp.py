import json
import sys

def update_templates(input_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Update the template of each entry to match the question
    for entry in data:
        entry['template'] = entry['question']

    # Write the updated data back to the same input file
    with open(input_file, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python swap_temp.py <input_file.json>")
    else:
        input_file = sys.argv[1]
        update_templates(input_file)
        print(f"Templates in {input_file} have been updated to match the questions.")
