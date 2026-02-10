import json
import argparse

def remove_duplicate_questions(input_file, output_file):
    try:
        # Read the JSON data from the input file
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Create a dictionary to track unique questions
        seen_questions = set()
        unique_entries = []

        for entry in data:
            question = entry.get("question", "").strip()
            if question not in seen_questions:
                seen_questions.add(question)
                unique_entries.append(entry)

        # Write the cleaned data to the output file
        with open(output_file, 'w') as f:
            json.dump(unique_entries, f, indent=4)

        print(f"Duplicates removed. Cleaned data written to '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove duplicate entries from a JSON file based on the question field.")
    parser.add_argument("input_file", help="Path to the input JSON file.")
    parser.add_argument("output_file", help="Path to the output JSON file.")
    
    args = parser.parse_args()

    remove_duplicate_questions(args.input_file, args.output_file)
