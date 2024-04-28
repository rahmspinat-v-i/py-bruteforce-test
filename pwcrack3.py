import tkinter as tk
from tkinter import filedialog, messagebox, Checkbutton, IntVar, Toplevel
import itertools
import rarfile
import zipfile
import time

def load_file(entry):
    filename = filedialog.askopenfilename()
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def brute_force(archive_file_path, charset, max_length, status_window, status_label):
    start_time = time.time()
    file_type = archive_file_path.split('.')[-1].lower()
    status_window.deiconify()  # Show the status window when starting the brute force
    try:
        if file_type == 'rar':
            archive = rarfile.RarFile(archive_file_path)
        elif file_type == 'zip':
            archive = zipfile.ZipFile(archive_file_path)
        else:
            messagebox.showerror("Unsupported file", f"No support for .{file_type} files.")
            return

        attempt_counter = 0
        for length in range(1, max_length + 1):
            for attempt in itertools.product(charset, repeat=length):
                password = ''.join(attempt)
                status_label.config(text=f"Trying: {password}\nAttempts: {attempt_counter}\nTime Elapsed: {int(time.time() - start_time)}s")
                status_window.update()
                attempt_counter += 1
                try:
                    if file_type == 'rar':
                        archive.extractall(pwd=password)
                    elif file_type == 'zip':
                        archive.extractall(pwd=password.encode('utf-8'))
                    messagebox.showinfo("Success", f"Password found: {password}")
                    return
                except (rarfile.RarWrongPassword, RuntimeError, zipfile.BadZipFile):
                    continue
        messagebox.showinfo("Failure", "No valid password found.")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found. Please check the paths.")
    except (rarfile.BadRarFile, zipfile.BadZipFile):
        messagebox.showerror("Error", "Bad file. Please provide a valid archive file.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        status_window.withdraw()  # Hide the status window when done

def get_charset(options):
    charset = ""
    if options[0].get() == 1:
        charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if options[1].get() == 1:
        charset += "abcdefghijklmnopqrstuvwxyz"
    if options[2].get() == 1:
        charset += "0123456789"
    if options[3].get() == 1:
        charset += "!@#$%^&*()-_=+[]{};:,.<>?/"
    if options[4].get() == 1:
        charset += "àáâäãåçèéêëìíîïñòóôöõøùúûüýÿ"
    return charset

def create_gui():
    root = tk.Tk()
    root.title("Brute Force Password Cracker")

    options = [IntVar() for _ in range(5)]
    charset_labels = ["All Capital Letters", "All Lowercase Letters", "All Numbers", "All Special Characters", "All Diacritics"]
    
    tk.Label(root, text="Archive File:").grid(row=0, column=0)
    archive_entry = tk.Entry(root, width=50)
    archive_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse...", command=lambda: load_file(archive_entry)).grid(row=0, column=2)

    # Status window setup
    status_window = Toplevel(root)
    status_window.title("Brute Force Status")
    status_label = tk.Label(status_window, text="Ready", font=('Helvetica', 12))
    status_label.pack(pady=20)
    status_window.withdraw()  # Initially hide the window

    for i, label in enumerate(charset_labels):
        Checkbutton(root, text=label, variable=options[i]).grid(row=2+i, column=0, sticky='w')

    tk.Button(root, text="Start Brute Force", command=lambda: brute_force(archive_entry.get(), get_charset(options), 24, status_window, status_label)).grid(row=7, column=1)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
