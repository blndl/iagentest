import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import numpy as np



class CSVAnalyzer:
    def __init__(self, parent, df, column):
        self.df = df
        self.column = column
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        self.topNEntry = tk.Entry(self.frame)
        self.topNEntry.pack(pady=5)
        self.topNEntry.insert(0, "10")

        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(expand=True, fill="both", pady=5)

        self.analyze()

    def analyze(self):
        if self.column not in self.df.columns:
            return

        topN = self.topNEntry.get()
        if not topN.isdigit():
            topN = 10
        else:
            topN = int(topN)

        valueCounts = self.df[self.column].value_counts().head(topN)
        topDf = valueCounts.reset_index()
        topDf.columns = [self.column, "Count"]

        self.tree["columns"] = list(topDf.columns)
        self.tree["show"] = "headings"
        for col in topDf.columns:
            self.tree.heading(col, text=col)

        for _, row in topDf.iterrows():
            self.tree.insert("", "end", values=list(row))

class DateCurveAnalyzer:
    def __init__(self, parent, df, dateColumn="date", durationColumn="duree_minutes"):
        self.df = df
        self.dateColumn = dateColumn
        self.durationColumn = durationColumn
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        self.avgLabel = tk.Label(self.frame, text="", anchor="e", font=("Arial", 10))
        self.avgLabel.pack(fill="x", padx=10, pady=5)

        self.figure = Figure(figsize=(6,4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        self.prepareData()
        self.plotCurve()

    def prepareData(self):
        dfCopy = self.df.copy()
        dfCopy[self.dateColumn] = pd.to_datetime(dfCopy[self.dateColumn], errors='coerce')
        dfCopy = dfCopy.dropna(subset=[self.dateColumn])
        dfCopy[self.durationColumn] = pd.to_numeric(dfCopy[self.durationColumn], errors='coerce')

        dfCopy['weekStart'] = dfCopy[self.dateColumn] - pd.to_timedelta(dfCopy[self.dateColumn].dt.weekday, unit='d')
        groupedCount = dfCopy.groupby('weekStart').size()
        groupedAvgDuration = dfCopy.groupby('weekStart')[self.durationColumn].mean()

        self.dates = pd.to_datetime(list(groupedCount.index))
        self.values = np.array(list(groupedCount.values))
        self.avgDurations = {d: groupedAvgDuration[d] for d in groupedAvgDuration.index}
        self.datesNum = mdates.date2num(self.dates)

        durations = dfCopy[self.durationColumn].dropna()
        if len(durations) > 0:
            avgMinutes = durations.mean()
            hours = int(avgMinutes // 60)
            minutes = int(avgMinutes % 60)
            self.avgLabel.config(text=f"Average session time: {hours}h {minutes}min")
        else:
            self.avgLabel.config(text="Average session time: N/A")

    def plotCurve(self):
        self.ax.clear()
        self.ax.plot(self.datesNum, self.values, marker='o', linestyle='-')
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.ax.set_title("Number of entries per week")
        self.ax.set_xlabel("Week start date")
        self.ax.set_ylabel("Count")
        self.ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()
