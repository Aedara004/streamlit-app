import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
#st.dataframe(df.groupby("Category").sum())
#category = st.selectbox("Select a Category", df['Category'].unique())
#x=df.groupby("Category").sum()
#st.dataframe(x.loc[category])
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")
st.write("## Your additions")

# Calculate profit and profit margin
df['Profit'] = df['Sales'] - df['Discount']
df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

# Overall average profit margin (all products across all categories)
overall_avg_profit_margin = df['Profit_Margin'].mean()

# Grouping by "Category" and "Sub_Category", and summing the "Sales", "Profit", and "Profit_Margin" columns
grouped = df.groupby(["Category", "Sub_Category"]).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Profit_Margin': 'mean'  # Average profit margin within each group
}).reset_index()

# Streamlit app
st.title('Sales and Profit Analysis')

# Print the available categories
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
available_categories = grouped['Category'].unique()
selected_category = st.selectbox('Select a category', available_categories)

if selected_category:
    # Filter subcategories based on selected category
    subcategories = grouped[grouped['Category'] == selected_category]['Sub_Category'].unique()

    # Multi-select for subcategories
    st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
    selected_subcategories = st.multiselect('Select subcategories', subcategories)
    
    if selected_subcategories:
        st.write(f"Selected subcategories for Category '{selected_category}': {selected_subcategories}")

        # Filter data for selected subcategories
        filtered_data = df[(df['Category'] == selected_category) &
                           (df['Sub_Category'].isin(selected_subcategories))].copy()

        if not filtered_data.empty:
            # Aggregate sales data by month for each subcategory
            sales_by_month_and_subcategory = filtered_data.groupby([pd.Grouper(freq='M'), 'Sub_Category']).agg({
                'Sales': 'sum'
            }).reset_index()

            st.subheader(f'Sales for Selected Subcategories in Category {selected_category}')
            for subcategory in selected_subcategories:
                subcategory_data = sales_by_month_and_subcategory[sales_by_month_and_subcategory['Sub_Category'] == subcategory]

                st.write(f"### (3) show a line chart of sales for {subcategory}")
                st.line_chart(subcategory_data.set_index('Order_Date')['Sales'], use_container_width=True)

            # Calculate metrics for selected subcategories
            total_sales = filtered_data['Sales'].sum()
            total_profit = filtered_data['Profit'].sum()
            overall_profit_margin = filtered_data['Profit_Margin'].mean()

            # Display metrics using st.metric
            st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
            st.subheader('Metrics for Selected Subcategories')
            st.metric(label='Total Sales', value=f"${total_sales:,}")
            st.metric(label='Total Profit', value=f"${total_profit:,}")
            st.metric(label='Overall Profit Margin (%)', value=f"{overall_profit_margin:.2f}%")

            # Delta with overall average profit margin
            delta_profit_margin = overall_profit_margin - overall_avg_profit_margin
            st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
            st.metric(label='Delta Overall Profit Margin (%)', value=f"{overall_profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")

        else:
            st.write("No data available for the selected subcategories.")
    else:
        st.write("No subcategories selected.")
else:
    st.write("Please select a category.")

# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the dataframe index and we would need to use x=None to tell bar_chart to use the index
