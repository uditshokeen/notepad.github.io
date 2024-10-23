import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font

# Create the root window
root = tk.Tk()
root.title("Notepad")
root.geometry("900x500")

# Global variables
file_path = None

# Function to create a new file
def new_file():
    global file_path
    file_path = None
    text_area.delete(1.0, tk.END)
    root.title("Untitled - Notepad")

# Function to open a file
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                           filetypes=[("Text Documents", "*.txt"),
                                                      ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, file.read())
        root.title(f"{file_path} - Notepad")

# Function to save the current file
def save_file():
    global file_path
    if file_path is None:
        save_as_file()
    else:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        root.title(f"{file_path} - Notepad")

# Function to save as a new file
def save_as_file():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Documents", "*.txt"),
                                                        ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        root.title(f"{file_path} - Notepad")

# Function to exit the notepad
def exit_notepad():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Edit functions
def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def undo():
    text_area.event_generate("<<Undo>>")

def redo():
    text_area.event_generate("<<Redo>>")

# Function to find text in the document
def find_text():
    search_text = simpledialog.askstring("Find Text", "Enter text to find:")
    if search_text:
        start_idx = '1.0'
        while True:
            start_idx = text_area.search(search_text, start_idx, stopindex=tk.END)
            if not start_idx:
                messagebox.showinfo("Result", "No more matches found.")
                break
            end_idx = f"{start_idx}+{len(search_text)}c"
            text_area.tag_add("highlight", start_idx, end_idx)
            text_area.tag_config("highlight", background="yellow")
            start_idx = end_idx

# Function to display the word count
def update_word_count(event=None):
    text_content = text_area.get(1.0, tk.END)
    word_count = len(text_content.split())
    status_bar.config(text=f"Word Count: {word_count}")

# Font customization function
def customize_font():
    font_family = simpledialog.askstring("Font", "Enter font family (e.g., Arial):", initialvalue="Arial")
    font_size = simpledialog.askinteger("Font", "Enter font size:", initialvalue=12)
    if font_family and font_size:
        new_font = font.Font(family=font_family, size=font_size)
        text_area.config(font=new_font)

# Zoom functions
def zoom_in():
    current_font = font.nametofont(text_area.cget("font"))
    current_size = current_font.actual()["size"]
    current_font.configure(size=current_size + 2)

def zoom_out():
    current_font = font.nametofont(text_area.cget("font"))
    current_size = current_font.actual()["size"]
    current_font.configure(size=current_size - 2)

# Create a menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_notepad)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo)
edit_menu.add_command(label="Redo", command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Format menu
format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Font", command=customize_font)
menu_bar.add_cascade(label="Format", menu=format_menu)

# View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Zoom In", command=zoom_in)
view_menu.add_command(label="Zoom Out", command=zoom_out)
menu_bar.add_cascade(label="View", menu=view_menu)

# Add the menu bar to the window
root.config(menu=menu_bar)

# Create a text area
text_area = tk.Text(root, wrap="word", undo=True)
text_area.pack(expand=1, fill="both")

# Add a status bar
status_bar = tk.Label(root, text="Word Count: 0", anchor="e")
status_bar.pack(fill="x")

# Bind the word count to key presses
text_area.bind("<KeyRelease>", update_word_count)

# Run the application
root.mainloop()
