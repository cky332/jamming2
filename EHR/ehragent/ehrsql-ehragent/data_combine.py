import json
import argparse
import random

def load_json(file_path):
    """Load the JSON file"""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, output_file):
    """Save the combined JSON data to a new file"""
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def combine_json_files(file1, file2, randomize=False):
    """Combine two JSON files and return the combined data, with an option to randomize"""
    data1 = load_json(file1)
    data2 = load_json(file2)

    # Combine the two datasets
    combined_data = data1 + data2

    # Optionally randomize the combined entries
    if randomize:
        random.shuffle(combined_data)

    return combined_data

def main():
    # Set up argument parser for combining two JSON files
    parser = argparse.ArgumentParser(description="Combine two JSON files with an option to randomize the entries.")
    parser.add_argument('file1', help="Path to the first JSON file")
    parser.add_argument('file2', help="Path to the second JSON file")
    parser.add_argument('output_file', help="Path to save the combined JSON file")
    parser.add_argument('--randomize', action='store_true', help="Randomize the entries in the combined JSON output")

    args = parser.parse_args()

    # Combine the JSON files
    combined_data = combine_json_files(args.file1, args.file2, randomize=args.randomize)

    # Save the combined JSON data to the output file
    save_json(combined_data, args.output_file)

    print(f"Combined JSON file saved to {args.output_file}")
    if args.randomize:
        print("The entries were randomized.")

if __name__ == "__main__":
    main()
