import subprocess

# Execute the 'echo' command and capture its output
result = subprocess.run(["git", "diff"], capture_output=True, text=True)
print(f"Output: {result.stdout}")
print(f"Error: {result.stderr}")
