import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(filename="file_organizer.log", level=logging.INFO)

# File type categories
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx'],
    'Videos': ['.mp4', '.mov', '.avi'],
    'Music': ['.mp3', '.wav'],
    'Archives': ['.zip', '.rar'],
    'Scripts': ['.py', '.js', '.html'],
    'Others': []
}

def organize_files(folder_path):
    try:
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Folder not found!")
            return

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(file)[1].lower()
                moved = False
                for folder, extensions in FILE_TYPES.items():
                    if file_ext in extensions:
                        dest_folder = os.path.join(folder_path, folder)
                        os.makedirs(dest_folder, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_folder, file))
                        logging.info(f"Moved {file} to {folder}")
                        moved = True
                        break
                if not moved:
                    other_folder = os.path.join(folder_path, "Others")
                    os.makedirs(other_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(other_folder, file))
                    logging.info(f"Moved {file} to Others")

        messagebox.showinfo("Success", "Files organized successfully!")
    except Exception as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", str(e))

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def on_submit():
    folder = folder_entry.get()
    organize_files(folder)

# GUI Setup
app = tk.Tk()
app.title("Smart File Organizer")
app.geometry("400x200")
app.resizable(False, False)

tk.Label(app, text="Select Folder to Organize:").pack(pady=10)
folder_entry = tk.Entry(app, width=40)
folder_entry.pack(pady=5)

browse_btn = tk.Button(app, text="Browse", command=browse_folder)
browse_btn.pack(pady=5)

submit_btn = tk.Button(app, text="Organize", command=on_submit, bg="#28a745", fg="white", padx=20)
submit_btn.pack(pady=15)

app.mainloop()
