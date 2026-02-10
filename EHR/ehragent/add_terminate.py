import os

def append_terminate_to_files(source_dir, destination_dir):
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # List all files in the source directory
    files = os.listdir(source_dir)

    # Process each file
    for file_name in files:
        # Construct the full file path
        source_file_path = os.path.join(source_dir, file_name)
        destination_file_path = os.path.join(destination_dir, file_name)

        # Open the source file and read its contents
        with open(source_file_path, 'r') as f:
            file_contents = f.read()

        # Append 'TERMINATE' to the contents
        file_contents += "\nTERMINATE"

        # Write the modified contents to the destination file
        with open(destination_file_path, 'w') as f:
            f.write(file_contents)

    print(f"All files have been processed and saved to {destination_dir}.")

# Example usage:
source_directory = "logs-poison/"
destination_directory = "logs-poisoned/"
append_terminate_to_files(source_directory, destination_directory)
