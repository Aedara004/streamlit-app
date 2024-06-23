import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])

# Calculate profit and profit margin
df['Profit'] = df['Sales'] - df['Discount']
df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

# Grouping by "Category" and "Sub_Category", and summing the "Sales", "Profit", and "Profit_Margin" columns
grouped = df.groupby(["Category", "Sub_Category"]).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Profit_Margin': 'mean'  # Average profit margin within each group
}).reset_index()

# Overall average profit margin (all products across all categories)
overall_avg_profit_margin = df['Profit_Margin'].mean()

# Streamlit app
st.title('Sales and Profit Analysis')

# Print the available categories
available_categories = grouped['Category'].unique()
selected_category = st.selectbox('Select a category', available_categories)

if selected_category:
    # Filter subcategories based on selected category
    subcategories = grouped[grouped['Category'] == selected_category]['Sub_Category'].unique()
    
    # Multi-select for subcategories
    selected_subcategories = st.multiselect('Select subcategories', subcategories)
    
    if selected_subcategories:
        st.write(f"Selected subcategories for Category '{selected_category}': {selected_subcategories}")
        
        # Filter data for selected subcategories
        filtered_data = grouped[(grouped['Category'] == selected_category) &
                                (grouped['Sub_Category'].isin(selected_subcategories))]
        
        if not filtered_data.empty:
            # Line chart for sales using st.line_chart
            st.subheader(f'Sales for Selected Subcategories in Category {selected_category}')
            for subcategory in selected_subcategories:
                subcategory_data = filtered_data[filtered_data['Sub_Category'] == subcategory]
                st.line_chart(subcategory_data.set_index('Sub_Category')['Sales'])
            
            # Calculate metrics for selected subcategories
            total_sales = filtered_data['Sales'].sum()
            total_profit = filtered_data['Profit'].sum()
            overall_profit_margin = filtered_data['Profit_Margin'].mean()
            
            # Display metrics using st.metric
            st.subheader('Metrics for Selected Subcategories')
            st.metric(label='Total Sales', value=f"${total_sales:,.2f}")
            st.metric(label='Total Profit', value=f"${total_profit:,.2f}")
            st.metric(label='Overall Profit Margin (%)', value=f"{overall_profit_margin:.2f}%")
            
            # Delta with overall average profit margin
            delta_profit_margin = overall_avg_profit_margin - overall_profit_margin
            st.metric(label='Delta Overall Profit Margin (%)', value=f"{delta_profit_margin:.2f}%", delta=delta_profit_margin)
            
        else:
            st.write("No data available for the selected subcategories.")
    else:
        st.write("No subcategories selected.")
else:
    st.write("Please select a category.")
