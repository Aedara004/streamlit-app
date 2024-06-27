import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but linexs--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
#st.dataframe(df.groupby("Category").sum())
#category = st.selectbox("Select a Category", df['Category'].unique())
#x=df.groupby("Category").sum()
#st.dataframe(x.loc[category])

# Calculate profit and profit margin
df['Profit'] = df['Sales'] - df['Discount']
df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

# Overall average profit margin (all products across all categories)
overall_avg_profit_margin = df['Profit_Marimport streamlit as st
import pandas as pd
import numpy as np

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Bar chart of sales by category
st.bar_chart(df, x="Category", y="Sales")

# Aggregated bar chart of sales by category
aggregated_df = df.groupby("Category", as_index=False).sum()
st.dataframe(aggregated_df)
st.bar_chart(aggregated_df, x="Category", y="Sales", color="#04f")

# Aggregated sales by month
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# Categorized data
data = {
    'Category': ['Technology', 'Furniture', 'Office Supplies'],
    'Sub_Category': {
        'Technology': ['Phones', 'Appliances', 'Machines', 'Copiers'],
        'Furniture': ['Bookcases', 'Chairs', 'Tables', 'Storage', 'Furnishings'],
        'Office Supplies': [
            'Labels', 'Art', 'Binders', 'Paper', 'Accessories', 'Envelopes',
            'Fasteners', 'Supplies'
        ]
    }
}

# Step (1): Add a dropdown for Category
category = st.selectbox("Select a Category", data['Category'])

# Step (2): Add a multi-select for Sub_Category in the selected Category
if category:
    sub_categories = data['Sub_Category'][category]
    selected_sub_categories = st.multiselect(f"Select Sub-Categories in {category}", sub_categories)

# Display selected options
st.write(f"Selected Category: {category}")
st.write(f"Selected Sub-Categories: {selected_sub_categories}")

# Filter the dataframe based on selected category and sub-categories
if selected_sub_categories:
    filtered_df = df[(df['Category'] == category) & (df['Sub_Category'].isin(selected_sub_categories))]

    # Step (3): Show a line chart of sales for the selected items in (2)
    st.write("### Sales Line Chart")
    sales_chart = filtered_df.groupby('Order_Date')['Sales'].sum().reset_index()
    st.line_chart(sales_chart, x='Order_Date', y='Sales')

    # Calculate metrics
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    overall_profit_margin = total_profit / total_sales * 100

    # Overall average profit margin for all products across all categories
    overall_avg_profit_margin = df['Profit'].sum() / df['Sales'].sum() * 100
    delta_profit_margin = overall_profit_margin - overall_avg_profit_margin

    # Step (4): Show three metrics
    st.write("### Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")

# Display selected options
st.write(f"Selected Category: {category}")
st.write(f"Selected Sub-Categories: {selected_sub_categories}")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
