# CSV Analysis App

A Tkinter-based app to analyze a CSV dataset with multiple visualizations:

- Top values by column
- Entries over time
- Service table filter
- Qualité score histogram
- Interaction comparison
- Practitioner grade distribution (0–5)

## Requirements

- Python 3.10+
- Packages: `pandas`, `numpy`, `matplotlib`, `tkinter` (bundled with Python on macOS)

Install packages:

```bash
pip install pandas numpy matplotlib
```

## Run

```bash
python main.py
```

On launch, select your CSV file; the tabs will render analyses.

## Files

- `main.py`: App entry and tab wiring
- `introFrame.py`: CSV loader UI
- `csvAnalyzer.py`: Top values and date curve
- `serviceTableAnalyzer.py`: Service-based filtering table
- `qualiteScoreHistogram.py`: Histogram for `qualite_score`
- `interactionComparisonAnalyzer.py`: Patient vs practitioner interactions
- `gradeAnalyzer.py`: Histogram and stats for `note_practicien` (0–5)

## Notes

- `gradeAnalyzer.py` resolves the grade column robustly (trim/case/accent-insensitive).
- Ensure your CSV headers match expected columns or choose variants.
