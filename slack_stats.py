import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from collections import defaultdict
import re

# Function to open file dialog and select the file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select Slack Messages File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    return file_path

# Load the file content
file_path = select_file()  # Use GUI to select the file
if not file_path:
    print("No file selected, exiting...")
    exit()

with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize counters
message_count = defaultdict(int)
response_count = defaultdict(int)
tag_count = defaultdict(int)

# Regular expression to find tags (e.g., @user)
tag_pattern = re.compile(r'@(\w+)')

# Process each line
current_user = None
for line in lines:
    if not line.startswith("\t"):  # It's a message
        # Extract user
        timestamp, user_message = line.split(" - ", 1)
        user, message = user_message.split(": ", 1)
        current_user = user.strip()

        # Increment message count
        message_count[current_user] += 1

        # Check for direct mentions in the message
        tags = tag_pattern.findall(message)
        for tag in tags:
            tag_count[tag] += 1

    else:  # It's a reply
        timestamp, reply_message = line.strip().split(" - ", 1)
        reply_user, message = reply_message.split(": ", 1)

        # Increment response count
        response_count[reply_user.strip()] += 1

        # Check for direct mentions in the reply
        tags = tag_pattern.findall(message)
        for tag in tags:
            tag_count[tag] += 1

# Prepare data for graphing
users = list(message_count.keys())

# Message count by user
message_values = [message_count[user] for user in users]

# Response count by user
response_values = [response_count.get(user, 0) for user in users]

# Tag count by user
tag_values = [tag_count.get(user, 0) for user in users]

# Display the results in text format
print("Message count by user:")
for user, count in message_count.items():
    print(f"{user}: {count} messages")

print("\nResponse count by user:")
for user, count in response_count.items():
    print(f"{user}: {count} responses")

print("\nTag count by user:")
for user, count in tag_count.items():
    print(f"{user}: {count} direct mentions")

# Create bar chart for message, response, and tag counts
fig, ax = plt.subplots(3, 1, figsize=(10, 10))

# Plot message count
ax[0].bar(users, message_values)
ax[0].set_title('Message Count by User')
ax[0].set_xlabel('User')
ax[0].set_ylabel('Message Count')

# Plot response count
ax[1].bar(users, response_values)
ax[1].set_title('Response Count by User')
ax[1].set_xlabel('User')
ax[1].set_ylabel('Response Count')

# Plot tag count
ax[2].bar(users, tag_values)
ax[2].set_title('Tag Count by User')
ax[2].set_xlabel('User')
ax[2].set_ylabel('Tag Count')

# Adjust layout
plt.tight_layout()

# Show the graph
plt.show()
