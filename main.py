"""
E-Commerce Sales Analysis
CSE 310 Data Analysis Project

This program uses pandas to answer three questions about a Global Superstore
sales dataset. It demonstrates data cleaning, filtering, conversion, grouping,
aggregation, sorting, comparison, and visualization.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


# Build file paths relative to this script so the project works from any folder.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "global_superstore.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"


def load_and_clean_data(file_path):
    """Read the CSV, convert important columns, and remove unusable records."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}\n"
            "Place global_superstore.csv inside the project's data folder."
        )

    # Read the source data. The CSV contains one row per product line, not
    # necessarily one row per complete order.
    data = pd.read_csv(file_path)

    required_columns = [
        "Order ID", "Order Date", "Market", "Category", "Sales"
    ]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(
            "The CSV is missing required columns: " + ", ".join(missing_columns)
        )

    # Conversion: parse text dates into pandas datetime values.
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")

    # Conversion: make sure sales are numeric so math and aggregation work.
    data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")

    original_count = len(data)

    # Filter: keep rows with the key information needed for our questions.
    data = data.dropna(
        subset=["Order ID", "Order Date", "Market", "Category", "Sales"]
    ).copy()

    # Filter: sales values below zero are excluded from this sales analysis.
    # (This is a project decision; negative values may have a different meaning
    # in other business datasets, such as returns or credit notes.)
    data = data[data["Sales"] >= 0].copy()

    # Conversion: extract a whole-number year from each valid order date.
    data["Year"] = data["Order Date"].dt.year

    removed_count = original_count - len(data)
    print(f"Rows in original CSV: {original_count}")
    print(f"Rows analyzed after cleaning: {len(data)}")
    print(f"Rows excluded during cleaning: {removed_count}")
    print(
        "Date range: "
        f"{data['Order Date'].min().date()} to "
        f"{data['Order Date'].max().date()}"
    )
    print()

    if data.empty:
        raise ValueError("No valid rows remain after cleaning the dataset.")

    return data


def analyze_categories(data):
    """Answer Question 1 using filtering, aggregation, sorting, and comparison."""
    print("QUESTION 1: Which product categories generate the highest total sales?")
    print("Operations: filter valid rows -> group and sum -> sort descending")

    # Filtering: remove rows with missing category or sales values.
    category_rows = data.dropna(subset=["Category", "Sales"]).copy()

    # Aggregation: calculate total sales for each product category.
    category_totals = (
        category_rows.groupby("Category", as_index=False)
        .agg(Total_Sales=("Sales", "sum"),
             Number_of_Product_Lines=("Sales", "size"))
    )

    # Sorting: put the category with the largest total sales first.
    category_totals = category_totals.sort_values(
        "Total_Sales", ascending=False
    ).reset_index(drop=True)

    print(category_totals.to_string(
        index=False,
        formatters={"Total_Sales": lambda value: f"${value:,.2f}"}
    ))

    # Justification: compare the highest and lowest category totals.
    leader = category_totals.iloc[0]
    lowest = category_totals.iloc[-1]
    difference = leader["Total_Sales"] - lowest["Total_Sales"]

    print(
        f"Finding: {leader['Category']} ranks first with "
        f"${leader['Total_Sales']:,.2f} in total sales. "
        f"It generated ${difference:,.2f} more sales than "
        f"{lowest['Category']}, the lowest category in this dataset."
    )
    print(
        "Interpretation: this ranking compares total sales revenue, not profit. "
        "A category with higher sales does not automatically have the highest profit."
    )
    print()

    category_totals.to_csv(OUTPUT_DIR / "category_sales.csv", index=False)
    return category_totals


def analyze_markets(data):
    """Answer Question 2 by calculating average complete order value by market."""
    print("QUESTION 2: Which markets have the highest average sales per order?")
    print(
        "Operations: convert Sales to numeric during cleaning -> filter valid rows "
        "-> aggregate line items into orders -> aggregate by market -> sort"
    )

    # Filter: keep rows that have the fields required for this question.
    market_rows = data.dropna(
        subset=["Market", "Order ID", "Sales"]
    ).copy()

    # Important: one order can contain multiple product lines. First sum the
    # sales for each Order ID within its market to calculate a complete order.
    order_totals = (
        market_rows.groupby(["Market", "Order ID"], as_index=False)
        .agg(Order_Total=("Sales", "sum"))
    )

    # Aggregation: calculate the mean order total for each market.
    market_summary = (
        order_totals.groupby("Market", as_index=False)
        .agg(
            Average_Order_Value=("Order_Total", "mean"),
            Number_of_Orders=("Order ID", "nunique"),
            Total_Sales=("Order_Total", "sum"),
        )
    )

    # Sorting: rank markets by average order value, highest first.
    market_summary = market_summary.sort_values(
        "Average_Order_Value", ascending=False
    ).reset_index(drop=True)

    print(market_summary.to_string(
        index=False,
        formatters={
            "Average_Order_Value": lambda value: f"${value:,.2f}",
            "Total_Sales": lambda value: f"${value:,.2f}",
        }
    ))

    # Justification: compare the highest and lowest market averages.
    leader = market_summary.iloc[0]
    lowest = market_summary.iloc[-1]
    difference = leader["Average_Order_Value"] - lowest["Average_Order_Value"]

    print(
        f"Finding: {leader['Market']} has the highest average order value "
        f"at ${leader['Average_Order_Value']:,.2f}, based on "
        f"{int(leader['Number_of_Orders'])} orders. This is "
        f"${difference:,.2f} higher per order on average than "
        f"{lowest['Market']}."
    )
    print(
        "Interpretation: average order value is the average of each order's "
        "combined sales. It is not the average of individual product rows."
    )
    print()

    market_summary.to_csv(OUTPUT_DIR / "average_sales_by_market.csv", index=False)
    order_totals.to_csv(OUTPUT_DIR / "order_totals_by_market.csv", index=False)
    return market_summary


def analyze_years(data):
    """Answer Question 3 using date conversion, aggregation, sorting, and graphing."""
    print("QUESTION 3: Which year had the highest total sales?")
    print("Operations: convert Order Date -> extract year -> aggregate -> sort")

    # Filtering: keep rows with valid dates and sales.
    year_rows = data.dropna(subset=["Order Date", "Sales"]).copy()

    # Conversion: turn each date into its calendar year for grouping.
    year_rows["Year"] = year_rows["Order Date"].dt.year

    # Aggregation: add up sales within each year.
    yearly_totals = (
        year_rows.groupby("Year", as_index=False)
        .agg(Total_Sales=("Sales", "sum"),
             Number_of_Product_Lines=("Sales", "size"))
    )

    # Sorting: rank years from the highest total sales to the lowest.
    yearly_totals = yearly_totals.sort_values(
        "Total_Sales", ascending=False
    ).reset_index(drop=True)

    print(yearly_totals.to_string(
        index=False,
        formatters={"Total_Sales": lambda value: f"${value:,.2f}"}
    ))

    # Justification: compare the best year with the next-highest year.
    leader = yearly_totals.iloc[0]
    if len(yearly_totals) > 1:
        second = yearly_totals.iloc[1]
        difference = leader["Total_Sales"] - second["Total_Sales"]
        comparison = (
            f"This is ${difference:,.2f} more than "
            f"{int(second['Year'])}, the next-highest year."
        )
    else:
        comparison = "There is only one year in the dataset to compare."

    print(
        f"Finding: {int(leader['Year'])} had the highest total sales at "
        f"${leader['Total_Sales']:,.2f}. {comparison}"
    )
    print(
        "Interpretation: the result compares the total sales recorded in each "
        "year represented in this CSV. It does not predict future sales."
    )
    print()

    yearly_totals.to_csv(OUTPUT_DIR / "yearly_sales.csv", index=False)
    return yearly_totals


def create_sales_chart(category_totals):
    """Create a bar chart of total sales by category and save it to outputs."""
    # The table is already sorted, so the chart uses the same category ranking.
    chart_data = category_totals.sort_values("Total_Sales", ascending=False)

    plt.figure(figsize=(9, 5))
    plt.bar(chart_data["Category"], chart_data["Total_Sales"])
    plt.title("Total Sales by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales ($)")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    chart_path = OUTPUT_DIR / "sales_by_category.png"
    plt.savefig(chart_path, dpi=150)
    plt.close()
    print(f"Chart saved to: {chart_path}")
    print(
        "Chart explanation: each bar represents the sum of sales for one "
        "category. Taller bars indicate higher total sales."
    )


def main():
    """Run all three analyses and save tables and a chart."""
    print("E-COMMERCE SALES ANALYSIS")
    print("=" * 40)

    # Create the output folder if it does not already exist.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        data = load_and_clean_data(DATA_FILE)
        category_totals = analyze_categories(data)
        analyze_markets(data)
        analyze_years(data)
        create_sales_chart(category_totals)

        print()
        print("ANALYSIS COMPLETE")
        print(f"Output files are stored in: {OUTPUT_DIR}")
        print(
            "The CSV output files contain the calculated tables, and the PNG "
            "file contains the category sales chart."
        )

    except FileNotFoundError as error:
        print(f"File error: {error}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, pd.errors.ParserError) as error:
        print(f"Data error: {error}", file=sys.stderr)
        sys.exit(1)
    except OSError as error:
        print(f"File system error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
