# Learning Log — Student Data Explorer (Python)

## 2026-02-15
- Goal: Improve code clarity and reliability by adding simple explanations, tracking data cleaning changes, and producing a clearer summary output.
- What I changed:
  - Added docstrings/comments explaining each step of the workflow
  - Added a “data quality report” to count missing values before/after cleaning
  - Kept the pipeline structure: load → clean → feature → summarise → export
  - Made outputs easier to understand in `summary.txt`
- Problem I hit: Some cells were blank, which caused calculations to return NaN until I cleaned the data properly.
- How I fixed it: Used `pd.to_numeric(..., errors="coerce")` to safely convert types and then filled missing physics values with the column mean.
- What I learned:
  - What a pandas DataFrame is and why it’s useful for CSV data
  - Why data cleaning matters before analysis (types + missing values)
  - How correlation can show a relationship between study habits and results (without proving causation)
- Next step: Add one extra insight (median scores or subject ranking) and update README to explain what the outputs mean.

## Reflection
- What I understand confidently now:
  - How to load CSV data using pandas
  - How and why I converted columns to numeric values
  - How I created a new feature (`average_score`) to compare students
- What I still need to practise:
  - Explaining correlation clearly (what it means and what it does NOT prove)
  - Trying different missing-value strategies (mean vs median vs dropping rows)
- 3 interview questions I can answer now:
  1) What is a DataFrame and why did you use it?
  2) How did you handle missing values and why?
  3) What does correlation tell you in your analysis?

## Tools/resources I used
- Python documentation (functions, file structure)
- pandas documentation (`read_csv`, `to_numeric`, `fillna`, `mean`, `corr`)
- W3Schools / Real Python (quick syntax reminders)
- VS Code + terminal errors/tracebacks (debugging)
