import os
import tkinter as tk
from tkinter import ttk, filedialog

class FileSystemNavigator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File System Navigator (Recursive Explorer)")
        self.geometry("800x600")

        # Path input and browse button
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.path_entry = tk.Entry(top_frame, width=60)
        self.path_entry.pack(side=tk.LEFT, padx=5)
        self.path_entry.insert(0, os.getcwd())

        browse_btn = tk.Button(top_frame, text="Browse", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT)

        load_btn = tk.Button(top_frame, text="Load", command=self.load_tree)
        load_btn.pack(side=tk.LEFT, padx=5)

        # Tree view for displaying folder structure
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def load_tree(self):
        path = self.path_entry.get()
        if os.path.isdir(path):
            self.tree.delete(*self.tree.get_children())  # Clear tree
            self.insert_items('', path)
        else:
            tk.messagebox.showerror("Error", "Invalid directory path!")

    def insert_items(self, parent, path):
        try:
            for item in os.listdir(path):
                abs_path = os.path.join(path, item)
                node = self.tree.insert(parent, 'end', text=item, open=False)
                if os.path.isdir(abs_path):
                    self.insert_items(node, abs_path)
        except PermissionError:
            pass  # Skip folders that can't be accessed

if __name__ == "__main__":
    app = FileSystemNavigator()
    app.mainloop()