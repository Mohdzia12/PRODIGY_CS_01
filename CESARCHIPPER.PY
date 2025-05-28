import tkinter as tk
from tkinter import ttk, filedialog
import os

def caesar_cipher(text, shift, mode='encrypt', letters_only=True):
    result = ""
    if mode == 'decrypt':
        shift = -shift
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        elif not letters_only:
            result += chr((ord(char) + shift) % 1114112)  # full Unicode wrap
        else:
            result += char
    return result

def process_text():
    message = message_entry.get("1.0", tk.END).strip()
    try:
        shift = int(shift_entry.get())
        mode = mode_var.get()
        letters_only = letter_only_var.get()
        result = caesar_cipher(message, shift, mode, letters_only)
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state='disabled')
    except ValueError:
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Shift must be an integer.")
        output_text.config(state='disabled')

def load_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            message_entry.delete("1.0", tk.END)
            message_entry.insert(tk.END, content)

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            content = output_text.get("1.0", tk.END).strip()
            file.write(content)

def toggle_dark_mode():
    is_dark = dark_mode_var.get()
    bg = "#2e2e2e" if is_dark else "white"
    fg = "white" if is_dark else "black"
    style = ttk.Style()
    style.theme_use('clam')
    root.config(bg=bg)
    for widget in root.winfo_children():
        widget_type = widget.winfo_class()
        if widget_type in ['TLabel', 'TButton', 'TRadiobutton', 'TCheckbutton']:
            widget.configure(background=bg, foreground=fg)
        if isinstance(widget, tk.Text):
            widget.configure(bg=bg, fg=fg, insertbackground=fg)
        if isinstance(widget, ttk.Entry):
            widget.configure(background=bg)

# Main window
root = tk.Tk()
root.title("Advanced Caesar Cipher Tool")
root.geometry("600x600")
root.resizable(False, False)

# Input
ttk.Label(root, text="Enter your message:").pack(pady=(10, 0))
message_entry = tk.Text(root, height=6, width=70)
message_entry.pack()

ttk.Button(root, text="Load from File", command=load_from_file).pack(pady=5)

# Shift input
ttk.Label(root, text="Shift value:").pack(pady=(10, 0))
shift_entry = ttk.Entry(root)
shift_entry.pack()

# Mode
mode_var = tk.StringVar(value='encrypt')
ttk.Label(root, text="Mode:").pack(pady=(10, 0))
ttk.Radiobutton(root, text='Encrypt', variable=mode_var, value='encrypt').pack()
ttk.Radiobutton(root, text='Decrypt', variable=mode_var, value='decrypt').pack()

# Options
letter_only_var = tk.BooleanVar(value=True)
ttk.Checkbutton(root, text="Encrypt only letters (A-Z, a-z)", variable=letter_only_var).pack()

# Dark mode
dark_mode_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Dark Mode 🌙", variable=dark_mode_var, command=toggle_dark_mode).pack()

# Process button
ttk.Button(root, text="Process", command=process_text).pack(pady=10)

# Output
ttk.Label(root, text="Result:").pack()
output_text = tk.Text(root, height=6, width=70, state='disabled')
output_text.pack()

# Save result
ttk.Button(root, text="Save Result to File", command=save_to_file).pack(pady=10)

root.mainloop()
