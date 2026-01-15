import os
import re
import csv
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Function to detect binary files
def is_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return True
    except:
        return True
    return False

# Function to perform multiple replacements in a file
def replace_text_in_file(file_path, replacements, log_entries):
    # List of encodings to try reading the file
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'cp1252']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            original_content = content
            
            # Perform all replacements using regex (case-insensitive)
            for pattern, replacement in replacements.items():
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            
            # If changes occurred, write back the file and log each replacement made
            if content != original_content:
                with open(file_path, 'w', encoding=encoding) as file:
                    file.write(content)
                
                # Log each replacement that occurred (if pattern was found in the original file)
                for pattern, replacement in replacements.items():
                    if re.search(pattern, original_content, flags=re.IGNORECASE):
                        log_entries.append({
                            'File Path': file_path,
                            'Original Text': pattern,
                            'Replaced With': replacement,
                            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
            break  # Exit loop if successful
        except (UnicodeDecodeError, UnicodeEncodeError):
            continue

# Main script using a Tkinter file dialog to select the website folder
root = tk.Tk()
root.withdraw()

folder_selected = filedialog.askdirectory(title="Select Your Website Folder")
log_entries = []

if folder_selected:
    # Define the replacement mappings.
    # Patterns are regular expressions.
    replacements = {
        # Poshak name replacement
        r"themewagon": "DMK&Brothers",
        
        # Color replacements (ordered by priority)
        # 1. Greens -> Browns
        r"#1bbd36": "#8B4513",      # Main accent (green to saddle brown)
        r"#2ae149": "#A0522D",      # Secondary accent (light green to sienna)
        r"#059652": "#689F38",      # Success messages (green to olive)
        
        # 2. Blacks/Grays -> Browns
        r"#000000": "#3E2723",      # Pure black to dark brown
        r"#000": "#3E2723",
        r"#111111": "#3E2723",      # Dark text/headings
        r"#444444": "#5D4037",      # Body text (gray to medium brown)
        r"#060606": "#4E342E",      # Dark backgrounds
        r"#252525": "#6D4C41",      # Dark surfaces
        
        # 3. Whites -> Creams
        r"#FFFDD0": "#FCFAEF",      # Pure white to cream
        r"#FFFDD0": "#FCFAEF",
        r"#f7f7f7": "#FDF5E6",      # Light backgrounds to off-white
        
        # 4. Special cases
        r"#df1529": "#D32F2F",      # Error messages (brighter red to deeper red)
        r"rgba\(0, 0, 0, 0.1\)": "rgba(139, 69, 19, 0.1)"  # Black shadows -> brown shadows
    }

    # Process only files with extensions .html, .css, or .js
    for dirpath, _, filenames in os.walk(folder_selected):
        for filename in filenames:
            if filename.endswith(('.html', '.css', '.js')):
                file_path = os.path.join(dirpath, filename)
                # Skip binary files
                if not is_binary(file_path):
                    replace_text_in_file(file_path, replacements, log_entries)
    
    # Save the log as a CSV file in the parent directory of the selected folder
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = os.path.join(os.path.dirname(folder_selected), f'Replace_Logs_{timestamp}.csv')

    with open(log_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Path', 'Original Text', 'Replaced With', 'Timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_entries)

    print("Done! Changes have been made and logged to:", log_filename)
else:
    print("No folder selected.")
