import json
import os
import sys

def split_json(file_path):
    try:
        # Load the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Check if the input is a list
        if not isinstance(data, list):
            print("The JSON file does not contain a list of entries.")
            return
        
        # Get the directory of the input file
        dir_name = os.path.dirname(file_path)
        
        # Iterate through the list and save each entry as a separate JSON file
        for index, entry in enumerate(data, start=1):
            output_file = os.path.join(dir_name, f"{index}.json")
            with open(output_file, 'w') as outfile:
                json.dump([entry], outfile, indent=4)  # Enclose entry in a list
        
        print(f"Split {len(data)} entries into individual JSON files in {dir_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_json.py <path_to_json_file>")
    else:
        input_file = sys.argv[1]
        split_json(input_file)
