import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Load the three datasets given for the assignment
# ---------------------------------------------------------
orders = pd.read_excel('List_of_Orders.xlsx')
details = pd.read_excel('Order_Details.xlsx')
target = pd.read_excel('Sales_target.xlsx')

# Quick sanity check - see what each file actually contains
# before doing any real analysis
print(orders.head())
print(orders.shape)

print(details.head())
print(details.shape)

print(target.head())
print(target.shape)


# ===========================================================
# PART 1 - Sales and Profitability Analysis
# ===========================================================

# List_of_Orders has the order/customer/location info, and
# Order_Details has the Amount/Profit/Category info for each
# order. Need both together, so merging on Order ID.
merged = pd.merge(orders, details, on='Order ID', how='inner')

print("\n--- MERGED DATA ---")
print(merged.head())
print(merged.shape)   # should be 1500 rows if every order matched properly

# Group everything by Category to get sales/profit per category
category_summary = merged.groupby('Category').agg(
    Total_Sales=('Amount', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Order_Count=('Order ID', 'count')
).reset_index()

# Avg profit per order = how much profit, on average, one order
# in that category brings in
category_summary['Avg_Profit_Per_Order'] = category_summary['Total_Profit'] / category_summary['Order_Count']

# Profit margin % = profit as a percentage of sales
# (this is the real indicator of category health, not just total profit)
category_summary['Profit_Margin_%'] = (category_summary['Total_Profit'] / category_summary['Total_Sales']) * 100

print("\n--- CATEGORY SUMMARY ---")
print(category_summary)


# ===========================================================
# PART 2 - Target Achievement Analysis (Furniture)
# ===========================================================

# The "Month of Order Date" column got misread by Excel/pandas.
# It was originally something like "Apr-18" (April 2018), but it
# got parsed as a full date where the 2-digit year (18) landed in
# the day slot, and the current year got used instead.
# Fixing that here: month stays the same, day (18/19) is actually
# the last 2 digits of the real year.
def fix_date(d):
    return pd.Timestamp(year=2000 + d.day, month=d.month, day=1)

target['Month_Fixed'] = target['Month of Order Date'].apply(fix_date)

print("\n--- TARGET DATE FIXED ---")
print(target[['Month_Fixed', 'Category', 'Target']].head(15))

# Filter down to just Furniture, sorted chronologically
furniture = target[target['Category'] == 'Furniture'].sort_values('Month_Fixed').reset_index(drop=True)

# pct_change() automatically gives % change from the previous row
# first row will be NaN since there's nothing before it to compare
furniture['MoM_%_Change'] = furniture['Target'].pct_change() * 100

print("\n--- FURNITURE MoM % CHANGE ---")
print(furniture[['Month_Fixed', 'Target', 'MoM_%_Change']])


# ===========================================================
# PART 3 - Regional Performance Insights
# ===========================================================

# Using 'nunique' (not 'count') for Order_Count here, since one
# order can have multiple line items in Order_Details - we want
# actual number of distinct orders per state, not number of rows
state_summary = merged.groupby('State').agg(
    Order_Count=('Order ID', 'nunique'),
    Total_Sales=('Amount', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()

state_summary['Avg_Profit_Per_Order'] = state_summary['Total_Profit'] / state_summary['Order_Count']
state_summary['Profit_Margin_%'] = (state_summary['Total_Profit'] / state_summary['Total_Sales']) * 100

# Top 5 states by number of orders (as the assignment asks for)
top5_states = state_summary.sort_values('Order_Count', ascending=False).head(5)

print("\n--- TOP 5 STATES BY ORDER COUNT ---")
print(top5_states)

# Also checking top states by sales - helps spot states that are
# smaller in volume but punch above their weight in profitability
print("\n--- ALL STATES BY TOTAL SALES (Top 10) ---")
print(state_summary.sort_values('Total_Sales', ascending=False).head(10))


# ===========================================================
# CHARTS - visualizing the three parts above
# ===========================================================

# Chart 1: which category brings in the most total sales
plt.figure(figsize=(8, 5))
plt.bar(category_summary['Category'], category_summary['Total_Sales'],
        color=['#F59E0B', '#2563EB', '#10B981'])
plt.title('Category-wise Total Sales')
plt.xlabel('Category')
plt.ylabel('Total Sales (₹)')
plt.tight_layout()
plt.savefig('chart1_category_sales.png')
plt.show()

# Chart 2: how the Furniture target has been growing month by month
plt.figure(figsize=(8, 5))
plt.plot(furniture['Month_Fixed'], furniture['Target'], marker='o', color='#2563EB', linewidth=2)
plt.title('Furniture Category — Monthly Target Trend')
plt.xlabel('Month')
plt.ylabel('Target (₹)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('chart2_furniture_target.png')
plt.show()

# Chart 3: combining order volume (bars) and profitability (line) for
# the top 5 states in one view - makes it easy to spot a state like
# Punjab that has decent volume but is actually losing money
fig, ax1 = plt.subplots(figsize=(8, 5))

ax1.bar(top5_states['State'], top5_states['Order_Count'], color='#10B981')
ax1.set_xlabel('State')
ax1.set_ylabel('Order Count', color='#10B981')
plt.xticks(rotation=20)

ax2 = ax1.twinx()
ax2.plot(top5_states['State'], top5_states['Avg_Profit_Per_Order'], color='black', marker='o', linewidth=2)
ax2.set_ylabel('Avg Profit per Order (₹)', color='black')

plt.title('Top 5 States — Order Count vs Avg Profit')
plt.tight_layout()
plt.savefig('chart3_top5_states.png')
plt.show()