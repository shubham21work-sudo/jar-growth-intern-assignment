# Jar — Growth Intern Assignment

Sales analysis assignment completed as part of the interview process for the Growth Intern role at Jar.

## What's in this repo

- `analysis.py` — Python script covering all three parts of Question 1 (Sales Analysis)
- `List_of_Orders.xlsx`, `Order_Details.xlsx`, `Sales_target.xlsx` — datasets provided for the assignment
- `chart1_category_sales.png` — category-wise total sales
- `chart2_furniture_target.png` — Furniture category monthly target trend
- `chart3_top5_states.png` — top 5 states by order count vs. average profit

## Approach

**Part 1 — Sales & Profitability:** Merged `List_of_Orders` and `Order_Details` on Order ID, then calculated total sales, average profit per order, and profit margin % for each category.

**Part 2 — Target Achievement:** Fixed a date-parsing issue in the target dataset (Excel's "MMM-YY" format was being misread), then calculated month-over-month % change in Furniture targets.

**Part 3 — Regional Performance:** Identified the top 5 states by order count and analyzed their sales and profitability, including a couple of regional disparities worth flagging.

## How to run

pip install pandas openpyxl matplotlib
python analysis.py

## Author

Shubham