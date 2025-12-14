import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class IntroFrame:
    def __init__(self, root, onCsvLoaded):
        self.root = root
        self.onCsvLoaded = onCsvLoaded
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")

        tk.Label(self.frame, text="Welcome! Please select a CSV file to start.").pack(pady=20)
        tk.Button(self.frame, text="Select CSV", command=self.loadCsv).pack(pady=10)

    def loadCsv(self):
        filePath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filePath:
            return

        try:
            df = pd.read_csv(filePath)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV:\n{e}")
            return

        self.frame.destroy()
        self.onCsvLoaded(df)
