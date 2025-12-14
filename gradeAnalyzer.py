import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import unicodedata
import matplotlib.cm as cm

class GradeAnalyzer:
    def __init__(self, parent, df, column="note_practicien", bins=10):
        self.df = df
        self.column = column
        self.bins = bins
        self.parent = parent

        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        self.figure = Figure(figsize=(8,5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both", pady=10)

        self.infoFrame = tk.Frame(self.frame)
        self.infoFrame.pack(pady=10)

        self.statsLabel = tk.Label(self.infoFrame, font=("Arial", 12), justify="left")
        self.statsLabel.pack()

        self.plotGradeDistribution()

    def plotGradeDistribution(self):
        # Resolve column robustly (trim/case/accent-insensitive)
        resolved_col = self._resolve_column(self.column, list(self.df.columns))
        if not resolved_col:
            self.ax.clear()
            available = ", ".join(map(str, self.df.columns))
            self.ax.text(0.5, 0.55, f"Missing column: {self.column}", ha="center", va="center", fontsize=12)
            self.ax.text(0.5, 0.45, "Available columns shown below", ha="center", va="center", fontsize=10)
            self.ax.set_title("Practitioner Grade Distribution (0-5)")
            self.canvas.draw()
            self.statsLabel.config(text=f"Column '{self.column}' not found. Available: {available}")
            return

        data = pd.to_numeric(self.df[resolved_col], errors="coerce").dropna()

        if data.empty:
            self.ax.text(0.5, 0.5, "No valid data", ha="center", va="center", fontsize=12)
            self.canvas.draw()
            return

        data = data[(data >= 0) & (data <= 5)]

        if data.empty:
            self.ax.text(0.5, 0.5, "No data in 0-5 range", ha="center", va="center", fontsize=12)
            self.canvas.draw()
            return

        meanVal = data.mean()
        medianVal = data.median()
        stdVal = data.std()
        minVal = data.min()
        maxVal = data.max()
        totalCount = len(data)

        counts, binEdges = np.histogram(data, bins=self.bins, range=(0, 5))

        cmap = cm.get_cmap("RdYlGn")
        colors = [cmap(i/(self.bins-1)) for i in range(self.bins)]

        self.ax.clear()

        for i in range(self.bins):
            left = binEdges[i]
            height = counts[i]
            width = binEdges[i+1] - binEdges[i]
            self.ax.bar(left, height, width=width, color=colors[i], edgecolor="black", align="edge")

        self.ax.axvline(meanVal, color="blue", linewidth=2, linestyle="--", label=f"Mean: {meanVal:.2f}")
        self.ax.axvline(medianVal, color="purple", linewidth=2, linestyle=":", label=f"Median: {medianVal:.2f}")

        self.ax.set_title("Practitioner Grade Distribution (0-5)", fontsize=14, fontweight="bold")
        self.ax.set_xlabel("Grade", fontsize=12)
        self.ax.set_ylabel("Count", fontsize=12)
        self.ax.set_xlim(0, 5)
        self.ax.legend(loc="upper left")
        self.ax.grid(axis="y", alpha=0.3)

        statsText = (
            f"Total Grades: {totalCount}  |  "
            f"Mean: {meanVal:.2f}  |  "
            f"Median: {medianVal:.2f}  |  "
            f"Std Dev: {stdVal:.2f}  |  "
            f"Range: [{minVal:.2f} - {maxVal:.2f}]"
        )
        self.statsLabel.config(text=statsText)

        self.canvas.draw()

    def _normalize(self, s: str) -> str:
        if not isinstance(s, str):
            s = str(s)
        s = s.strip()
        # Remove accents
        s = ''.join(
            c for c in unicodedata.normalize('NFKD', s)
            if not unicodedata.combining(c)
        )
        s = s.lower()
        # Collapse separators
        for ch in [" ", "-", ":", ";", ",", "."]:
            s = s.replace(ch, "_")
        while "__" in s:
            s = s.replace("__", "_")
        s = s.strip("_")
        return s

    def _resolve_column(self, target: str, columns: list) -> str | None:
        target_norm = self._normalize(target)
        # Exact normalized match
        for col in columns:
            if self._normalize(col) == target_norm:
                return col
        # Fuzzy contains heuristics for common variants
        heuristics = ["note", "not", "grade", "score", "praticien", "praticien", "praticien"]
        for col in columns:
            norm = self._normalize(col)
            if all(h in norm for h in ["note", "praticien"]):
                return col
        # Case-insensitive startswith/contains
        for col in columns:
            norm = self._normalize(col)
            if target_norm in norm:
                return col
        return None
