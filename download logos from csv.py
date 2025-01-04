import os

# Function to rename logos by removing the 'channel_' prefix
def rename_logos(folder='logos'):
    # List all files in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        
        # Check if it's a file and if it starts with 'channel_'
        if os.path.isfile(file_path) and filename.startswith('channel_'):
            # Create new filename by removing the 'channel_' prefix
            new_filename = filename.replace('channel_', '', 1)
            new_file_path = os.path.join(folder, new_filename)
            
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f'Renamed: {filename} -> {new_filename}')

# Example usage
rename_logos()

print("Logo renaming process completed.")
