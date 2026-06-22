# Attendance Agent - Documentation

## 1. What does the project do?
This project automates employee attendance analysis. It processes check-in records to check whether employees arrive on time. For late arrivals, it calculates the latency minutes and applies rules to calculate fines. Finally, it exports reports classifying employees into safe (on-time) and danger (late) zones.

## 2. What is the request flow?
1. **Execution Start**: The user runs `main.py`.
2. **Dataset Loading**: The script reads the input file `data/attendance_2023_2024.csv` using Pandas.
3. **Employee Identification**: Columns starting with the prefix `"Person_"` are dynamically identified as employee name records.
4. **Attendance Parsing**: The script loops over each date and employee cell value to parse their check-in time (`analyzer.py`).
5. **Time Evaluation**:
   - Check-in times are parsed and compared to the baseline office time (`09:00` AM).
   - If the check-in is on-time or early: The status is set to `SAFE` with 0 fine.
   - If the check-in is late: The status is set to `DANGER`, and a rule-based fine is computed based on late minutes (`fine_calculator.py`).
6. **Report Generation**: The compiled records are saved into Pandas DataFrames.
7. **File Saving**: The results are exported to local files `outputs/safe_employees.csv` and `outputs/danger_employees.csv`.
8. **Summary Output**: A summary of safe/danger count and total fine amount is printed to the terminal console.

## 3. Which packages are used and why?
- **`pandas`**: Used for loading the CSV attendance dataset, filtering and sorting columns, and writing output report CSV files.
- **`datetime` (standard library)**: Used for parsing check-in strings and computing time differences.
- **`os` (standard library)**: Used for verifying and creating output directory structures.

## 4. Where does the data come from?
The data is read from a local CSV file: `data/attendance_2023_2024.csv`.

## 5. Where is the data stored?
The resulting CSV reports are stored locally under the `outputs/` directory:
- `outputs/safe_employees.csv`
- `outputs/danger_employees.csv`

## 6. What is the role of the LLM?
There is **no LLM model used** in this project. It is entirely based on deterministic rule-based algorithms.

## 7. What breaks if the LLM is removed?
**Nothing breaks**, since the project has no dependency on any LLM or AI models.
