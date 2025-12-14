import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

class InteractionComparisonAnalyzer:
    def __init__(self, parent, df, patientColumn, professionalColumn):
        self.df = df
        self.patientColumn = patientColumn
        self.professionalColumn = professionalColumn
        self.parent = parent

        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        self.statsLabel = tk.Label(self.frame, anchor="e", font=("Arial", 11))
        self.statsLabel.pack(anchor="ne", padx=10, pady=5)

        self.topFigure = Figure(figsize=(6,3), dpi=100)
        self.topAx = self.topFigure.add_subplot(111)
        self.topCanvas = FigureCanvasTkAgg(self.topFigure, master=self.frame)
        self.topCanvas.get_tk_widget().pack(fill="both", expand=True, pady=5)

        self.midFrame = tk.Frame(self.frame)
        self.midFrame.pack(fill="both", expand=True)

        self.leftFigure = Figure(figsize=(4,3), dpi=100)
        self.leftAx = self.leftFigure.add_subplot(111)
        self.leftCanvas = FigureCanvasTkAgg(self.leftFigure, master=self.midFrame)
        self.leftCanvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.rightFigure = Figure(figsize=(4,3), dpi=100)
        self.rightAx = self.rightFigure.add_subplot(111)
        self.rightCanvas = FigureCanvasTkAgg(self.rightFigure, master=self.midFrame)
        self.rightCanvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

        self.midFrame.columnconfigure(0, weight=1)
        self.midFrame.columnconfigure(1, weight=1)
        self.midFrame.rowconfigure(0, weight=1)

        self.plotAll()

    def plotAll(self):
        p = pd.to_numeric(self.df[self.patientColumn], errors="coerce").fillna(0)
        r = pd.to_numeric(self.df[self.professionalColumn], errors="coerce").fillna(0)

        totalP = p.sum()
        totalR = r.sum()
        meanP = p.mean()
        meanR = r.mean()
        medianP = p.median()
        medianR = r.median()
        corr = p.corr(r)

        self.statsLabel.config(
            text=f"Patient total: {totalP:.0f}   Professional total: {totalR:.0f}   "
                 f"Mean: {meanP:.2f}/{meanR:.2f}   Median: {medianP:.2f}/{medianR:.2f}   "
                 f"Correlation: {corr:.2f}"
        )

        self.topAx.clear()
        self.topAx.plot(p.values, label="Patient", color="blue")
        self.topAx.plot(r.values, label="Professional", color="red")
        self.topAx.set_title("Interactions by Session")
        self.topAx.set_xlabel("Session")
        self.topAx.set_ylabel("Count")
        self.topAx.legend()
        self.topCanvas.draw()

        self.leftAx.clear()
        alpha = 0.6
        self.leftAx.hist(p, bins=15, alpha=alpha, color="blue", label="Patient")
        self.leftAx.hist(r, bins=15, alpha=alpha, color="red", label="Professional")
        self.leftAx.set_title("Distribution Comparison")
        self.leftAx.set_xlabel("Count")
        self.leftAx.set_ylabel("Frequency")
        self.leftAx.legend()
        self.leftCanvas.draw()

        self.rightAx.clear()
        self.rightAx.boxplot([p, r], labels=["Patient", "Professional"])
        self.rightAx.set_title("Boxplot Comparison")
        self.rightAx.set_ylabel("Count")
        self.rightCanvas.draw()
