import tkinter as tk
from tkinter import ttk
from introFrame import IntroFrame
from csvAnalyzer import CSVAnalyzer, DateCurveAnalyzer
from serviceTableAnalyzer import ServiceTableAnalyzer
from qualiteScoreHistogram import QualiteScoreHistogram
from interactionComparisonAnalyzer import InteractionComparisonAnalyzer
from gradeAnalyzer import GradeAnalyzer


class CSVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Analysis App")
        self.root.geometry("800x600")
        IntroFrame(root, self.createTabs)

    def createTabs(self, df):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both")

        topValuesTab = ttk.Frame(notebook)
        dateCurveTab = ttk.Frame(notebook)
        serviceTab = ttk.Frame(notebook)
        qualiteTab = ttk.Frame(notebook)
        interactionTab = ttk.Frame(notebook)
        gradesTab = ttk.Frame(notebook)


        notebook.add(topValuesTab, text="Top Values")
        notebook.add(dateCurveTab, text="Entries Over Time")
        notebook.add(serviceTab, text="Service Table")
        notebook.add(qualiteTab, text="Qualite Score Histogram")
        notebook.add(interactionTab, text="Interactions Compare")
        notebook.add(gradesTab, text="Practitioner Grades")

        



        CSVAnalyzer(topValuesTab, df=df, column="langue")
        DateCurveAnalyzer(dateCurveTab, df=df, dateColumn="date", durationColumn="duree_minutes")
        ServiceTableAnalyzer(serviceTab, df=df, filterColumn="service")
        QualiteScoreHistogram(qualiteTab, df=df, column="qualite_score", bins=10)
        InteractionComparisonAnalyzer(interactionTab, df=df, patientColumn="interactions_patient", professionalColumn="interactions_praticien")
        GradeAnalyzer(gradesTab, df=df, column="note_practicien", bins=10)




root = tk.Tk()
app = CSVApp(root)
root.mainloop()
