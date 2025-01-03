import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_excel("workdata/Enhanced_Dummy_HBL_Data.xlsx ")

# Set Streamlit page configuration
st.set_page_config(page_title="HBL Data Analysis", layout="wide")
st.title("HBL Data Analysis Dashboard")

# Set the background color to a milk-like color and custom styles
st.markdown(
     """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    .reportview-container {
        background: #e8d8c4;  /* Milk-like color */
        font-family: 'Roboto', sans-serif;  /* Custom font */
    }
    .sidebar .sidebar-content {
        background: #e8d8c4;  /* Milk-like color for sidebar */
    }
    h1 {
        text-align: center;  /* Center headers */
        margin: 20px 0;  /* Add spacing */
        font-size: 34px;  /* Adjust font size */
    }
    h2 {
        text-align: center;  /* Center subheaders */
        margin: 20px 0;  /* Add spacing */
       
    }
    h3 {
        text-align: center;  /* Center sub-subheaders */
        margin: 20px 0;  /* Add spacing */
       
    }
    .centered-table {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }
    .plot-container {
        margin: 20px 0;  /* Add spacing around plots */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Dataset Overview
st.header("Dataset Overview:")

# Center the dataset table
st.markdown('<div class="centered-table">', unsafe_allow_html=True)
st.write(data)
st.markdown('</div>', unsafe_allow_html=True)

st.write(f"Dataset size: {data.size}")

# Define custom colors
colors = {
    'dark_blue': '#B85042',
    'slate_blue': '#A7BEAE',
    'light_beige': '#E7E8D1',
    'dark_slate': '#A7BEAE'
}


# Task 1: Account Type Distribution
st.markdown("<h2 style='font-size: 40px;'>Task 1: Distribution of Account Types</h2>", unsafe_allow_html=True)
account_type_counts = data['Account Type'].value_counts()
fig1, ax1 = plt.subplots(figsize=(width, height))  # Smaller plot size
ax1.pie(account_type_counts, labels=account_type_counts.index, autopct=lambda p: f'{p:.1f}%', startangle=150,
         colors=[colors['dark_blue'], colors['slate_blue'], colors['light_beige'], colors['dark_slate']],
         textprops={'fontsize': label_font_size})  # Adjust label font size here
ax1.set_title('Distribution of Account Types', fontsize=title_font_size)  # Adjust title font size

# Display the pie chart
st.pyplot(fig1)

st.markdown("<p style='font-size: 21px;'>This pie chart visualizes the proportion of different account types in the dataset.
By understanding the share of each account type, you can identify which account types are most popular or prevalent in the data. 
For example, a dominance of one type may indicate customer preferences or organizational focus.</p>", unsafe_allow_html=True)
# Task 2: Transaction Flow by Beneficiary Bank
st.markdown("<h2 style='font-size: 40px;'>Task 2: Top 5 Beneficiary Banks with Highest Credit Transactions by Region</h2>", unsafe_allow_html=True)

top_banks = data.groupby(['Region', 'Transaction To'])['Credit'].sum().reset_index()
top_banks = top_banks.sort_values(by='Credit', ascending=False).groupby('Region').head(5)
fig2, ax2 = plt.subplots(figsize=(width, height))  # Smaller plot size
sns.barplot(data=top_banks, x='Transaction To', y='Credit', hue='Region', ax=ax2, 
            palette=[colors['dark_blue'], colors['slate_blue'], colors['light_beige'], colors['dark_slate']])
ax2.set_title('Top 5 Beneficiary Banks with Highest Credit Transactions by Region', fontsize=title_font_size)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, fontsize=label_font_size)

st.pyplot(fig2)
st.write("<p style='font-size: 21px;'>Purpose: Displays the top 5 beneficiary banks in terms of credit transactions for each region.
This chart helps identify key banks that handle the most credit transactions in different regions. 
It can uncover regional banking trends or potential hubs of financial activity, which might be useful for decision-making in targeted banking strategies.</p>", unsafe_allow_html=True)

# Task 3: Geographic Heatmap of Transactions
st.markdown("<h2 style='font-size: 40px;'>Task 3: Transaction Intensity by Region</h2>", unsafe_allow_html=True)


transaction_intensity = data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()

# Create a custom colormap using the defined colors
custom_cmap = sns.color_palette([colors['dark_blue'], colors['slate_blue'], colors['light_beige'], colors['dark_slate']])

fig3, ax3 = plt.subplots(figsize=(width, height))  # Smaller plot size
sns.heatmap(transaction_intensity.set_index('Region'), annot=True, cmap=custom_cmap, fmt='.0f', ax=ax3)
ax3.set_title('Transaction Intensity by Region', fontsize=title_font_size)

st.pyplot(fig3)
st.write("<p style='font-size: 21px;'>Purpose: Shows transaction intensities (credit and debit amounts) across different regions. A heatmap provides a geographical perspective, making it easy to see which regions have the highest or lowest transaction activities. This can inform decisions about resource allocation, regional market focus, or potential risk areas.</p>", unsafe_allow_html=True)

# Task 4: Anomalies in Transactions
st.markdown("<h2 style='font-size: 40px;'>Task 4: Anomalies in Credit Transactions</h2>", unsafe_allow_html=True)

data['Credit_Z'] = (data['Credit'] - data['Credit'].mean()) / data['Credit'].std()
data['Debit_Z'] = (data['Debit'] - data['Debit'].mean()) / data['Debit'].std()
outliers_credit = data[data['Credit_Z'].abs() > 3]
fig4, ax4 = plt.subplots(figsize=(width, height))  # Smaller plot size
ax4.scatter(data.index, data['Credit'], label='Credit', alpha=0.5, color=colors['dark_blue'])
ax4.scatter(outliers_credit.index, outliers_credit['Credit'], color='red', label='Outliers (Credit)', alpha=0.7)
ax4.set_title('Anomalies in Credit Transactions', fontsize=title_font_size)
ax4.set_xlabel('Index', fontsize=label_font_size)
ax4.set_ylabel('Credit Amount', fontsize=label_font_size)
ax4.legend(fontsize=legend_font_size)

st.pyplot(fig4)
st.write("<p style='font-size: 21px;'>Purpose: Identifies outliers in the credit and debit transactions based on Z-scores. Outliers often represent unusual behavior or potential errors. By isolating these, you can investigate fraud, transaction errors, or extraordinary activities, enhancing data integrity and risk management.</p>", unsafe_allow_html=True)

# Task 5: Comparative Analysis of Transaction Types
st.markdown("<h2 style='font-size: 40px;'>Task 5: Comparative Analysis of Credit and Debit Transactions by Account Type</h2>", unsafe_allow_html=True)

fig5, ax5 = plt.subplots(figsize=(width, height))  # Smaller plot size
sns.boxplot(
    data=data.melt(id_vars='Account Type', value_vars=['Credit', 'Debit']),
    x='Account Type', y='value', hue='variable', ax=ax5, palette=[colors['dark_blue'], colors['slate_blue']]
)
ax5.set_title('Comparative Analysis of Credit and Debit Transactions by Account Type', fontsize=title_font_size)
ax5.set_xlabel('Account Type', fontsize=label_font_size)
ax5.set_ylabel('Transaction Amount', fontsize=label_font_size)
ax5.legend(title='Transaction Type', fontsize=legend_font_size)

st.pyplot(fig5)
st.write("<p style='font-size: 21px;'>
Purpose: Compares the distribution of credit and debit transaction amounts across different account types. Box plots show the central tendency (median) and spread (interquartile range) of transactions for each account type. It helps pinpoint which account types have higher variability or larger transactions, aiding in customer segmentation and strategy.</p>", unsafe_allow_html=True)

# Task 6: Transaction Trends Over Time
st.markdown("<h2 style='font-size: 40px;'>Task 6: Time-Based Analysis (if applicable)</h2>", unsafe_allow_html=True)

if 'Time' in data.columns:
    st.subheader("Task 6: Transaction Trends Over Time")
    data['Time'] = pd.to_datetime(data['Time'])
    data = data.dropna(subset=['Time'])
    if not data.empty:
 
        data.set_index('Time', inplace=True)
        time_series = data.resample('D')[['Credit', 'Debit']].sum().reset_index()
        if not time_series.empty:
            fig6, ax6 = plt.subplots(figsize=(width, height))  # Smaller plot size
            ax6.plot(time_series['Time'], time_series['Credit'], label='Credit', color=colors['dark_blue'])
            ax6.plot(time_series['Time'], time_series['Debit'], label='Debit', color=colors['slate_blue'])
            ax6.set_title("Transaction Trends Over Time", fontsize=title_font_size)
            ax6.set_xlabel("Time", fontsize=label_font_size)
            ax6.set_ylabel("Transaction Amount", fontsize=label_font_size)
            ax6.legend(fontsize=legend_font_size)

            st.pyplot(fig6)
        else:
            st.write("Time series data is empty after processing.")
    else:
        st.write("No valid time data found in the dataset.")
else:
    st.write("The 'Time' column is not available in the dataset.")

st.write("<p style='font-size: 21px;'>Purpose: Tracks trends in credit and debit transactions over time. Observing transaction trends over time can reveal seasonality, growth patterns, or unusual spikes/dips in activity. These insights can inform operational planning or promotional campaigns aligned with customer behavior.</p>", unsafe_allow_html=True)

# Task 7: Total Credit and Debit Amounts by Account Type
st.markdown("<h2 style='font-size: 40px;'>Task 7: Total Credit and Debit Amounts by Account Type</h2>", unsafe_allow_html=True)

customer_transactions = data.groupby('Account Type')[['Credit', 'Debit']].sum().reset_index()
fig7, ax7 = plt.subplots(figsize=(width, height))  # Smaller plot size
customer_transactions.set_index('Account Type').plot(kind='bar', stacked=True, ax=ax7, color=[colors['dark_blue'], colors['slate_blue']])
ax7.set_title('Total Credit and Debit Amounts by Account Type', fontsize=title_font_size)
ax7.set_xlabel('Account Type', fontsize=label_font_size)
ax7.set_ylabel('Transaction Amount', fontsize=label_font_size)
ax7.legend(title='Transaction Type', fontsize=legend_font_size)

st.pyplot(fig7)
st.write("<p style='font-size: 21px;'>Purpose: Displays total credit and debit amounts for each customer type. This chart helps understand customer type dynamics—e.g., which customer groups contribute most to credit or debit transactions. It can guide tailored marketing efforts or highlight reliance on specific customer segments.</p>", unsafe_allow_html=True)


# Task: Correlation Matrix (if applicable)
st.markdown("<h2 style='font-size: 40px;'> BONUS:  Correlation Matrix</h2>", unsafe_allow_html=True)

# Ensure only numeric columns are included
numeric_data = data[['Credit', 'Debit']].dropna()  # Use 'data' instead of 'filtered_data'

if not numeric_data.empty:
    corr_matrix = numeric_data.corr()
    fig_corr, ax_corr = plt.subplots(figsize=(width, height))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax_corr)
    ax_corr.set_title('Correlation Matrix', fontsize=title_font_size)
    st.pyplot(fig_corr)
else:
    st.write("No numeric data available for correlation analysis.")

# Bonus Task: Distribution of Transaction Amounts by Account Type
st.markdown("<h2 style='font-size: 40px;'>Bonus Task: Distribution of Transaction Amounts by Account Type</h2>", unsafe_allow_html=True)

fig9, ax9 = plt.subplots(figsize=(width, height))
# Use the defined colors for the box plot
sns.boxplot(data=data, x='Account Type', y='Credit', ax=ax9, palette=[colors['dark_blue'], colors['slate_blue']])
ax9.set_title('Distribution of Credit Transactions by Account Type', fontsize=title_font_size)
ax9.set_xlabel('Account Type', fontsize=label_font_size)
ax9.set_ylabel('Transaction Amount', fontsize=label_font_size)

# Display the box plot
st.pyplot(fig9)
st.write("<p style='font-size: 21px;'>Explanation: This box plot shows the distribution of credit transaction amounts across different account types. It helps identify the variability in transaction amounts and the presence of any outliers.</p>", unsafe_allow_html=True)
