import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import zscore

# Title and description
st.title("HBL Dummy Data Visualization")
st.write("This application visualizes insights from the HBL Dummy Dataset.")

# Load data
data_path = '/mnt/data/Enhanced_Dummy_HBL_Data.xlsx'
data = pd.read_excel(data_path)
st.write("## Dataset Preview")
st.dataframe(data.head())

# Task 1: Account Type Distribution
st.write("## Task 1: Account Type Distribution")
account_type_counts = data['Account Type'].value_counts()
fig1, ax1 = plt.subplots(figsize=(8, 6))
account_type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='tab20', ax=ax1)
ax1.set_title('Account Type Distribution')
ax1.set_ylabel('')  # Hide y-axis label
st.pyplot(fig1)

# Task 2: Transaction Flow by Beneficiary Bank
st.write("## Task 2: Transaction Flow by Beneficiary Bank")
top_banks = (data.groupby(['Region', 'Transaction To'])['Credit']
             .sum()
             .reset_index()
             .sort_values(by='Credit', ascending=False)
             .groupby('Region')
             .head(5))
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.barplot(data=top_banks, x='Transaction To', y='Credit', hue='Region', ax=ax2)
ax2.set_title('Top 5 Beneficiary Banks by Credit Transactions per Region')
ax2.set_xlabel('Beneficiary Bank')
ax2.set_ylabel('Credit Amount')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# Task 3: Geographic Heatmap of Transactions
st.write("## Task 3: Geographic Heatmap of Transactions")
region_agg = data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(region_agg.set_index('Region'), annot=True, fmt=".2f", cmap='YlGnBu', ax=ax3)
ax3.set_title('Geographic Heatmap of Transactions')
ax3.set_xlabel('Transaction Type')
ax3.set_ylabel('Region')
st.pyplot(fig3)

# Task 4: Anomalies in Transactions
st.write("## Task 4: Anomalies in Transactions")
data['Credit_Z'] = zscore(data['Credit'])
data['Debit_Z'] = zscore(data['Debit'])
outliers_credit = data[data['Credit_Z'].abs() > 3]
outliers_debit = data[data['Debit_Z'].abs() > 3]
fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.scatter(data.index, data['Credit'], label='Credit', alpha=0.5)
ax4.scatter(outliers_credit.index, outliers_credit['Credit'], color='red', label='Outliers (Credit)', alpha=0.7)
ax4.set_title('Anomalies in Credit Transactions')
ax4.set_xlabel('Index')
ax4.set_ylabel('Credit Amount')
ax4.legend()
st.pyplot(fig4)

# Task 5: Comparative Analysis of Transaction Types
st.write("## Task 5: Comparative Analysis of Transaction Types")
fig5, ax5 = plt.subplots(figsize=(12, 8))
sns.boxplot(data=data.melt(id_vars='Account Type', value_vars=['Credit', 'Debit']),
            x='Account Type', y='value', hue='variable', ax=ax5)
ax5.set_title('Comparative Analysis of Transaction Types by Account Type')
ax5.set_xlabel('Account Type')
ax5.set_ylabel('Transaction Amount')
st.pyplot(fig5)

# Task 6: Time-Based Analysis (if applicable)
if 'Time' in data.columns:
    st.write("## Task 6: Time-Based Analysis")
    data['Time'] = pd.to_datetime(data['Time'])
    data = data.dropna(subset=['Time'])
    if not data.empty:
        data.set_index('Time', inplace=True)
        time_series = data.resample('D')[['Credit', 'Debit']].sum().reset_index()
        if not time_series.empty:
            fig6, ax6 = plt.subplots(figsize=(12, 6))
            ax6.plot(time_series['Time'], time_series['Credit'], label='Credit', color='blue')
            ax6.plot(time_series['Time'], time_series['Debit'], label='Debit', color='red')
            ax6.set_title("Transaction Trends Over Time")
            ax6.set_xlabel("Time")
            ax6.set_ylabel("Transaction Amount")
            ax6.legend()
            st.pyplot(fig6)
        else:
            st.write("Time series data is empty after processing.")
    else:
        st.write("No valid time data found in the dataset.")
else:
    st.write("The 'Time' column is not available in the dataset.")

# Task 7: Customer Insights
st.write("## Task 7: Customer Insights")
customer_transactions = data.groupby('Account Type')[['Credit', 'Debit']].sum().reset_index()
fig7, ax7 = plt.subplots(figsize=(10, 6))
customer_transactions.set_index('Account Type').plot(kind='bar', stacked=True, ax=ax7, cmap='tab10')
ax7.set_title('Total Credit and Debit Amounts by Account Type')
ax7.set_xlabel('Account Type')
ax7.set_ylabel('Transaction Amount')
st.pyplot(fig7)
