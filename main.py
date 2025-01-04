import subprocess

# List of Python files to run
python_files = [
    'csv_to_m3u8.py',
    'git_push.py',
    # Add more files as needed
]

# Run each Python file
for python_file in python_files:
    # Print the name of the file being executed
    print(f"Executing {python_file}...")
    
    try:
        # Execute the Python file using subprocess
        result = subprocess.run(['python', python_file], capture_output=True, text=True)
        
        # Print the output of the execution
        if result.stdout:
            print(f"Output of {python_file}: {result.stdout}")
        if result.stderr:
            print(f"Error in {python_file}: {result.stderr}")
    except Exception as e:
        print(f"Failed to execute {python_file}: {e}")
