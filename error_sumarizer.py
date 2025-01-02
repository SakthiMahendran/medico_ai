import re

# Path to the log file
LOG_FILE_PATH = "url_test_results.txt"  # Replace with the actual path to your log file

# Load the log content from the file
try:
    with open(LOG_FILE_PATH, "r") as file:
        log_content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{LOG_FILE_PATH}' was not found.")
    exit()

# Regular expression to extract error messages
error_pattern = re.compile(
    r"ERROR:\s(?P<method>\w+)\s(?P<url>http[^\s]+)\s-\s(?P<status_code>\d+)\s-\s(?P<message>.+?)(?=\n\n|$)",
    re.DOTALL
)

# Extract and summarize error messages
error_summary = []
for match in error_pattern.finditer(log_content):
    method = match.group("method")
    url = match.group("url")
    status_code = match.group("status_code")
    message = match.group("message").strip()
    error_summary.append(f"{method} {url} - {status_code} - {message}")

# Print summarized error messages
print("Extracted Error Messages:")
for error in error_summary:
    print(error)

# Save the summary to a new file
SUMMARY_FILE_PATH = "error_summary.txt"
with open(SUMMARY_FILE_PATH, "w") as summary_file:
    summary_file.write("\n".join(error_summary))
print(f"Error summary saved to '{SUMMARY_FILE_PATH}'.")
