import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np



class CSVAnalyzer:
    def __init__(self, parent, df, column):
        self.df = df
        self.column = column
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.pack(expand=True, fill="both")

        # Top 3 display at the top
        self.top3Frame = tk.Frame(self.frame)
        self.top3Frame.pack(pady=10, fill="x")
        
        self.top3Label = tk.Label(self.top3Frame, text="Top 3 Values", font=("Arial", 14, "bold"))
        self.top3Label.pack()
        
        self.top3Display = tk.Label(self.top3Frame, text="", font=("Arial", 11), justify="left")
        self.top3Display.pack(pady=5)

        # Table in the middle with scrollbar
        tableFrame = tk.Frame(self.frame)
        tableFrame.pack(expand=False, fill="both", pady=5)
        
        self.tree = ttk.Treeview(tableFrame, height=10)
        self.tree.pack(side="left", expand=True, fill="both")
        
        scrollY = ttk.Scrollbar(tableFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side="right", fill="y")

        # Pie chart at the bottom
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        self.analyze()

    def analyze(self):
        if self.column not in self.df.columns:
            return

        # Get all values instead of just top 10
        valueCounts = self.df[self.column].value_counts()
        topDf = valueCounts.reset_index()
        topDf.columns = [self.column, "Count"]

        # Update Top 3 display (percentage based on total to match pie chart)
        top3Text = ""
        totalAll = valueCounts.sum()
        for i, (value, count) in enumerate(valueCounts.head(3).items(), 1):
            percentage = (count / totalAll) * 100
            top3Text += f"{i}. {value}: {count} ({percentage:.1f}%)\n"
        self.top3Display.config(text=top3Text)

        # Update table
        self.tree["columns"] = list(topDf.columns)
        self.tree["show"] = "headings"
        for col in topDf.columns:
            self.tree.heading(col, text=col)

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in topDf.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Create pie chart
        self.ax.clear()
        colors = plt.cm.Set3(range(len(valueCounts)))
        
        # Only show percentage for slices above 5% to avoid overlap
        def autopct_format(pct):
            return f'{pct:.1f}%' if pct > 5 else ''
        
        wedges, texts, autotexts = self.ax.pie(valueCounts.values, autopct=autopct_format, 
                    startangle=90, colors=colors)
        self.ax.legend(wedges, valueCounts.index, title=self.column, 
                      loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        self.ax.set_title(f"Distribution of {self.column}")
        self.figure.tight_layout()
        self.canvas.draw()

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
