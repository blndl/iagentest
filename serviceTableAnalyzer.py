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
        self.currentData = df
        self.sortColumn = None
        self.sortReverse = False
        
        # Mapping of original column names to display names
        self.columnNames = {
            "session_id": "ID",
            "date": "Date",
            "service": "Service",
            "langue": "Language",
            "duree_minutes": "Duration (min)",
            "interactions_patient": "Patient Int.",
            "interactions_praticien": "Doctor Int.",
            "interactions_totales": "Total Int.",
            "note_praticien": "Rating",
            "qualite_score": "Quality",
            "segments_non_reconnus": "Errors",
            "device": "Device"
        }

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
            displayName = self.columnNames.get(col, col)
            self.tree.heading(col, text=displayName, command=lambda c=col: self.sortBy(c))
            self.tree.column(col, width=100, anchor="center")

    def populateTable(self, data):
        self.tree.delete(*self.tree.get_children())
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def updateTable(self, event=None):
        selected = self.filterVar.get()
        if selected == "All":
            self.currentData = self.df
        else:
            self.currentData = self.df[self.df[self.filterColumn] == selected]
        self.populateTable(self.currentData)
    
    def sortBy(self, col):
        if self.sortColumn == col:
            self.sortReverse = not self.sortReverse
        else:
            self.sortColumn = col
            self.sortReverse = False
        
        sortedData = self.currentData.sort_values(by=col, ascending=not self.sortReverse)
        self.populateTable(sortedData)
