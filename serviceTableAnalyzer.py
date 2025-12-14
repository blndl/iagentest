import tkinter as tk
from tkinter import ttk
import pandas as pd

class ServiceTableAnalyzer:
    def __init__(self, parent, df, filterColumn="service"):
        self.df = df
        self.filterColumn = filterColumn
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        self.filterVar = tk.StringVar()
        services = ["All"] + sorted(df[self.filterColumn].dropna().unique())
        self.dropdown = ttk.Combobox(self.frame, textvariable=self.filterVar, values=services, state="readonly")
        self.dropdown.current(0)
        self.dropdown.pack(padx=10, pady=5, anchor="w")
        self.dropdown.bind("<<ComboboxSelected>>", self.updateTable)

        self.tree = ttk.Treeview(self.frame, show="headings")
        self.tree.pack(expand=True, fill="both")

        self.scrollY = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollY.set)
        self.scrollY.pack(side="right", fill="y")

        self.setupTable()
        self.populateTable(df)

    def setupTable(self):
        self.tree["columns"] = list(self.df.columns)
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

    def populateTable(self, data):
        self.tree.delete(*self.tree.get_children())
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def updateTable(self, event=None):
        selected = self.filterVar.get()
        if selected == "All":
            filtered = self.df
        else:
            filtered = self.df[self.df[self.filterColumn] == selected]
        self.populateTable(filtered)
