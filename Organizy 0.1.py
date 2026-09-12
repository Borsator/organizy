import os
import shutil
import tkinter as tk
from tkinter import messagebox

# --- GLOBAL UTILITY SETTINGS ---
TITLE = "organizy"
FOLDER_DESTINATION_NAME = "Organized Files"

# --- MAIN SORTING FUNCTION ---

def apply_sorting():
    downloads_folder = os.path.expanduser("~/Downloads")
    pictures_folder = os.path.expanduser("~/Pictures")
    main_destination = os.path.expanduser(f"~/Documents/{FOLDER_DESTINATION_NAME}")
    
    # Generate the target container structure (pure English names)
    target_folders = ["[file exe]", "[extracted folders]", "[non-extracted folders]", "[photos]", "[video mp4]", "Unresolved Files"]
    for folder in target_folders:
        os.makedirs(os.path.join(main_destination, folder), exist_ok=True)
        
    if not os.path.exists(downloads_folder) or not os.path.exists(pictures_folder):
        messagebox.showerror(TITLE, "Error: System folders not found!")
        return

    moved_count = 0
    sources = [downloads_folder, pictures_folder]

    for source_path in sources:
        all_items = os.listdir(source_path)

        for item in all_items:
            original_path = os.path.join(source_path, item)
            specific_destination = None
            
            # 1. EXTRACTED FOLDERS MANAGEMENT (Only from Downloads for safety)
            if os.path.isdir(original_path) and not item.startswith('.'):
                if source_path == downloads_folder and check_extracted.get():
                    specific_destination = os.path.join(main_destination, "[extracted folders]")
            
            # 2. SINGLE LOOSE FILES MANAGEMENT
            elif os.path.isfile(original_path):
                _, extension = os.path.splitext(item)
                extension = extension.lower()
                
                # Main Executables (.exe)
                if extension == ".exe" and check_exe.get():
                    specific_destination = os.path.join(main_destination, "[file exe]")
                # Compressed Archives (.zip, .rar, .7z)
                elif extension in [".zip", ".rar", ".7z"] and check_non_extracted.get():
                    specific_destination = os.path.join(main_destination, "[non-extracted folders]")
                # Photos and Screenshots (.png, .jpg, .jpeg)
                elif extension in [".png", ".jpg", ".jpeg"] and check_photos.get():
                    specific_destination = os.path.join(main_destination, "[photos]")
                # Video files (.mp4)
                elif extension == ".mp4" and check_videos.get():
                    specific_destination = os.path.join(main_destination, "[video mp4]")
                # Unrecognized Formats
                elif check_unknown.get() and extension not in [".exe", ".zip", ".rar", ".7z", ".png", ".jpg", ".jpeg", ".mp4"]:
                    specific_destination = os.path.join(main_destination, "Unresolved Files")

            if specific_destination:
                try:
                    # Tag photos tracking from Pictures directory to guarantee accurate restoration
                    if source_path == pictures_folder:
                        final_name = "IMG_ORIG_" + item
                    else:
                        final_name = item
                        
                    shutil.move(original_path, os.path.join(specific_destination, final_name))
                    moved_count += 1
                except Exception:
                    pass
                
    messagebox.showinfo(TITLE, f"Operation completed.\nMoved items: {moved_count}")

# --- RESTORATION BACKTRACK FUNCTION ---

def restore_files():
    downloads_folder = os.path.expanduser("~/Downloads")
    pictures_folder = os.path.expanduser("~/Pictures")
    main_destination = os.path.expanduser(f"~/Documents/{FOLDER_DESTINATION_NAME}")
    
    if not os.path.exists(main_destination):
        messagebox.showwarning(TITLE, "Warning: No organized directory found to restore!")
        return

    restored_count = 0
    subfolders = os.listdir(main_destination)
    
    for folder in subfolders:
        subfolder_path = os.path.join(main_destination, folder)
        if os.path.isdir(subfolder_path):
            items = os.listdir(subfolder_path)
            for item in items:
                try:
                    # Check if file originally belonged to Pictures
                    if item.startswith("IMG_ORIG_"):
                        original_name = item.replace("IMG_ORIG_", "", 1)
                        shutil.move(os.path.join(subfolder_path, item), os.path.join(pictures_folder, original_name))
                    else:
                        shutil.move(os.path.join(subfolder_path, item), os.path.join(downloads_folder, item))
                    restored_count += 1
                except Exception:
                    pass
                
    messagebox.showinfo(TITLE, f"Reset completed.\nItems moved back to original folders: {restored_count}")

def show_about():
    messagebox.showinfo(TITLE, "organizy v1.0\nLightweight open-source utility inspired by 7-Zip.")

# --- USER INTERFACE WINDOW CREATION (7-ZIP MANAGER STYLE) ---

window = tk.Tk()
window.title(TITLE)
window.geometry("560x480")
window.resizable(False, False)

BACKGROUND_COLOR = "#F0F0F0" 
window.configure(bg=BACKGROUND_COLOR)

# Classic Toolbar Menu File Setup
top_bar_menu = tk.Menu(window)
menu_file = tk.Menu(top_bar_menu, tearoff=0)
menu_file.add_command(label="Exit", command=window.quit)
top_bar_menu.add_cascade(label="File", menu=menu_file)

menu_help = tk.Menu(top_bar_menu, tearoff=0)
menu_help.add_command(label="About organizy...", command=show_about)
top_bar_menu.add_cascade(label="Help", menu=menu_help)
window.config(menu=top_bar_menu)

# Raised Action Button Layout Bar
action_bar_frame = tk.Frame(window, bg=BACKGROUND_COLOR, bd=1, relief="groove")
action_bar_frame.pack(fill="x", padx=2, pady=2)

btn_apply = tk.Button(action_bar_frame, text="➕ Apply", command=apply_sorting, font=("Segoe UI", 9), bg=BACKGROUND_COLOR, bd=1, relief="raised", padx=12, pady=2)
btn_apply.pack(side="left", padx=4, pady=4)

btn_restore = tk.Button(action_bar_frame, text="❌ Restore", command=restore_files, font=("Segoe UI", 9), bg=BACKGROUND_COLOR, bd=1, relief="raised", padx=12, pady=2)
btn_restore.pack(side="left", padx=4, pady=4)

# Options Sunken White Frame Display Box
options_group_box = tk.LabelFrame(window, text=" SORTING OPTIONS (7-ZIP STYLE) ", font=("Segoe UI", 9, "bold"), bg="white", bd=2, relief="sunken")
options_group_box.pack(fill="both", expand=True, padx=10, pady=15)

# Boolean Switch Allocation Setup Tracker values
check_exe = tk.BooleanVar(value=True)
check_extracted = tk.BooleanVar(value=True)
check_non_extracted = tk.BooleanVar(value=True)
check_photos = tk.BooleanVar(value=True)
check_videos = tk.BooleanVar(value=True)
check_unknown = tk.BooleanVar(value=True)

def build_option_row(text_description, target_variable, row_index):
    row_label = tk.Label(options_group_box, text=text_description, font=("Segoe UI", 10), bg="white", fg="black", anchor="w", width=48)
    row_label.grid(row=row_index, column=0, pady=6, padx=15, sticky="w")
    
    row_checkbox = tk.Checkbutton(options_group_box, variable=target_variable, bg="white", activebackground="white", selectcolor="white", bd=1)
    row_checkbox.grid(row=row_index, column=1, pady=6, padx=15, sticky="e")

# Deploy text fields maps assignments straight onto window template grid rows
build_option_row("organize [file exe] (main executables)", check_exe, 0)
build_option_row("organize [extracted folders]", check_extracted, 1)
build_option_row("organize [non extracted folders] (.zip, .rar, .7z)", check_non_extracted, 2)
build_option_row("organize photos jpg and png...", check_photos, 3)
build_option_row("organize video (.mp4)", check_videos, 4)
build_option_row("organize unknown extensions (unknown extensions)", check_unknown, 5)

# Bottom Status Footer strip setup configuration bar
status_bottom_bar = tk.Label(window, text=" 1 object(s) selected                     0 KB", font=("Segoe UI", 9), bg=BACKGROUND_COLOR, bd=1, relief="sunken", anchor="w")
status_bottom_bar.pack(fill="x", side="bottom")

window.mainloop()
