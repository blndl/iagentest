import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.cm as cm

class QualiteScoreHistogram:
    def __init__(self, parent, df, column="qualite_score", bins=10):
        self.df = df
        self.column = column
        self.bins = bins
        self.parent = parent

        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        self.figure = Figure(figsize=(6,4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both", pady=10)

        self.infoLabel = tk.Label(self.frame, anchor="e", font=("Arial", 11))
        self.infoLabel.pack(anchor="ne", padx=10, pady=5)

        self.plotHistogram()

    def plotHistogram(self):
        data = pd.to_numeric(self.df[self.column], errors="coerce").dropna()

        if data.empty:
            self.ax.text(0.5, 0.5, "No valid data", ha="center", va="center", fontsize=12)
            self.canvas.draw()
            return

        minVal = data.min()
        maxVal = data.max()
        padding = (maxVal - minVal) * 0.1
        if padding == 0:
            padding = 0.05

        counts, binEdges = np.histogram(data, bins=self.bins, range=(minVal, maxVal))

        cmap = cm.get_cmap("coolwarm")
        colors = [cmap(i/(self.bins-1)) for i in range(self.bins)]

        self.ax.clear()

        for i in range(self.bins):
            left = binEdges[i]
            height = counts[i]
            width = binEdges[i+1] - binEdges[i]
            self.ax.bar(left, height, width=width, color=colors[i], edgecolor="black", align="edge")

        meanVal = data.mean()
        medianVal = data.median()

        self.ax.axvline(meanVal, color="red", linewidth=2)
        self.ax.axvline(medianVal, color="green", linewidth=2)

        self.infoLabel.config(text=f"Mean: {meanVal:.3f}    Median: {medianVal:.3f}")

        self.ax.set_title(f"{self.column} Distribution")
        self.ax.set_xlabel("Score")
        self.ax.set_ylabel("Count")
        self.ax.set_xlim(minVal - padding, maxVal + padding)

        self.canvas.draw()
