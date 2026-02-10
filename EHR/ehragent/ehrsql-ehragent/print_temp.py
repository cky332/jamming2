import json
import sys

def extract_templates(input_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Extract the templates
    templates = [entry['template'] for entry in data]

    # Write the templates to "templates.txt"
    with open('templates.txt', 'w') as file:
        for template in templates:
            file.write(template + '\n')

    print("Templates have been written to templates.txt")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_templates.py <input_file.json>")
    else:
        input_file = sys.argv[1]
        extract_templates(input_file)
