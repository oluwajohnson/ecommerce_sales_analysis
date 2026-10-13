# E-Commerce Sales Analysis

## Project Description
This Python project analyzes a free Global Superstore CSV dataset with pandas and matplotlib. It answers three questions using data cleaning, filtering, data conversion, aggregation, sorting, comparisons, and a chart.

## Dataset
- File: `data/global_superstore.csv`
- Source: [Global Superstore CSV on GitHub](https://github.com/yannie28/Global-Superstore/blob/master/Global_Superstore%28CSV%29.csv)
- The CSV supplied for this project contains 100 rows and includes order IDs, order dates, markets, product categories, and sales.
- This is a small subset, so findings describe this file only and should not be generalized to all Global Superstore sales.

## Analysis Questions
1. Which product categories generate the highest total sales?
   - Filters rows with valid category and sales values.
   - Groups rows by category and sums sales.
   - Sorts categories from highest to lowest.
   - Explains the leading category and its difference from the lowest category.
2. Which markets have the highest average sales per order?
   - Converts sales to numeric values and filters missing data during cleaning.
   - Groups product lines by market and order ID to calculate a complete order total.
   - Calculates the average order total for each market and sorts the results.
   - Explains the leading market and its difference from the lowest market.
3. Which year had the highest total sales?
   - Converts order dates to datetime and extracts the year.
   - Groups rows by year and sums sales.
   - Sorts years and compares the leading year with the next-highest year.

## Data Analysis Operations Demonstrated
- **Filtering:** excludes records missing fields needed for the analysis and sales values below zero.
- **Conversion:** converts `Order Date` into datetime, `Sales` into numeric values, and extracts the calendar year.
- **Aggregation:** uses `groupby()` and `sum()` / `mean()` to calculate category totals, order totals, market averages, and yearly totals.
- **Sorting:** uses `sort_values()` to rank categories, markets, and years.
- **Justification:** each question prints an explanation based on calculated totals or averages and compares the leader with another result.
- **Visualization:** creates a bar chart showing total sales by category.

## Requirements
- Python 3
- pandas
- matplotlib

## How to Run
Open a terminal in the project folder and run:

```bash
python -m venv .venv
```

On Windows PowerShell, activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the packages:

```bash
python -m pip install -r requirements.txt
```

Run the analysis:

```bash
python main.py
```

If PowerShell blocks activation, you can install and run with the Python executable directly:

```powershell
python -m pip install -r requirements.txt
python main.py
```

## Output Files
Running `main.py` creates the `outputs` folder and saves:
- `category_sales.csv` — total sales by product category.
- `average_sales_by_market.csv` — average order value, number of orders, and total sales by market.
- `order_totals_by_market.csv` — combined sales total for each order within each market.
- `yearly_sales.csv` — total sales by year.
- `sales_by_category.png` — bar chart of total sales by category.

## Video Walkthrough Outline (4–5 Minutes)
1. **Introduction (30 seconds):** State the project goal and the three questions.
2. **Dataset (30–45 seconds):** Show the CSV and explain the columns used. Mention that it contains 100 rows.
3. **Data preparation (45 seconds):** Explain missing-value filtering, conversion of sales to numeric values, conversion of order dates, and extraction of year.
4. **Question 1 (45 seconds):** Show `groupby("Category")`, `sum()`, and `sort_values()`. Explain why the leading category has the highest total.
5. **Question 2 (60 seconds):** Explain why multiple product rows can belong to one order. Show the first grouping by `Market` and `Order ID`, then the average calculation by market.
6. **Question 3 and chart (45 seconds):** Show date-to-year conversion, yearly aggregation, sorting, and the bar chart.
7. **Wrap-up (15 seconds):** Show the output files and mention the project limitations.

## Limitations
- The CSV is a 100-row subset, so findings are limited to these records.
- Total sales are not the same as profit.
- The market average is calculated using complete order totals, not individual product rows.
- The analysis describes historical records and does not forecast future sales.

## Course Submission Reminders
- Confirm that the project has more than 100 lines of your own code, excluding setup files, and that comments explain the main functions and operations.
- Use the official CSE 310 Data Analysis README template if your instructor requires its exact headings; copy this project's details into that template.
- Put the code and README in a public GitHub repository, but do not upload `.venv`.
- Record a 4–5 minute video showing the program running and explaining the code. Add the video link here before submission.
- Complete any separate course reflection or submission form required by the module.

## Author

Ogunleye Johnson

## Repository

GitHub repository:
https://github.com/oluwajohnson/ecommerce_sales_analysis.git
