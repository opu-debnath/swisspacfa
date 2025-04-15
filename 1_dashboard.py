import streamlit as st 
import plotly.express as px 
import pandas as pd 
import os
import warnings
warnings.filterwarnings('ignore') 
from PIL import Image

# Page configuration
st.set_page_config(page_title="Swisspac F&A!!!", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Swisspac Demand Forecasting & Analytics")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Add custom sidebar content */
    [data-testid="stSidebarNav"]::before {
        content: "";
        display: block;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Add logo and welcome message */
    [data-testid="stSidebarNav"]::before {
        content: "Welcome to SFA";
        display: block;
        font-size: 20px;
        font-weight: bold;
        color: #f5f5f5;
        padding: 10px 0;
        text-align: center;
    }

    </style>
""", unsafe_allow_html=True)

# # File upload section
# fl = st.file_uploader(":file_folder: Upload a file", type=(["xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = pd.read_excel(filename)
# else:
#     os.chdir(r"/Users/opudebnath/Desktop/swisspac_analytics")
df = pd.read_excel("new_copy6.xlsx")

# Convert 'INVOICE DATE' to datetime
df["INVOICE DATE"] = pd.to_datetime(df["INVOICE DATE"])

# Date range filter
col1, col2 = st.columns(2)
startDate = pd.to_datetime(df["INVOICE DATE"]).min()
endDate = pd.to_datetime(df["INVOICE DATE"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["INVOICE DATE"] >= date1) & (df["INVOICE DATE"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("Choose your filter: ")

customer_segment = st.sidebar.multiselect("Pick your customer segment", df["VIP/POTENTIAL_LOYAL"].unique())
product_segment = st.sidebar.multiselect("Pick the product segment", df["CUST/STOCK"].unique())
product_name = st.sidebar.multiselect("Pick the product name", df["PRODUCT NAME"].unique())

# Apply filters
filtered_df = df.copy()

if customer_segment:
    filtered_df = filtered_df[filtered_df["VIP/POTENTIAL_LOYAL"].isin(customer_segment)]
if product_segment:
    filtered_df = filtered_df[filtered_df["CUST/STOCK"].isin(product_segment)]
if product_name:
    filtered_df = filtered_df[filtered_df["PRODUCT NAME"].isin(product_name)]

# Display filtered data in an expander
with st.expander("View Filtered Data"):
    st.dataframe(filtered_df, height=150)

# Key Metrics
st.subheader('Key Metrics')
total_sales = filtered_df['TOTAL'].sum()
total_qty = filtered_df['QTY'].sum()
num_customers = filtered_df['CUSTOMER NAME'].nunique()
num_vip_customers = filtered_df[filtered_df['VIP/POTENTIAL_LOYAL'] == 'Vip']['CUSTOMER NAME'].nunique()
num_potential_loyal_customers = filtered_df[filtered_df['VIP/POTENTIAL_LOYAL'] == 'Potential_loyal']['CUSTOMER NAME'].nunique()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Sales', f'${total_sales:,.2f}')
    st.metric('VIP Customers', num_vip_customers)
with col2:
    st.metric('Total Quantity Sold', f'{total_qty:,.0f}')
    st.metric('Potential Loyal Customers', num_potential_loyal_customers)
with col3:
    st.metric('Number of Customers', num_customers)

# Sales Over Time
st.subheader('Sales Over Time')

# Monthly Sales Line Chart
monthly_sales = filtered_df.groupby(filtered_df['INVOICE DATE'].dt.to_period('M'))['TOTAL'].sum().reset_index()
monthly_sales['INVOICE DATE'] = monthly_sales['INVOICE DATE'].dt.to_timestamp()
fig1 = px.line(
    monthly_sales,
    x='INVOICE DATE',
    y='TOTAL',
    title='Monthly Sales Over Time',
    labels={'INVOICE DATE': 'Month', 'TOTAL': 'Total Sales ($)'},
    color_discrete_sequence=["#d4a017"]  # Golden amber line
)
fig1.update_layout(
    plot_bgcolor="#0a1e3d",  # Midnight blue background
    paper_bgcolor="#0a1e3d",
    font_color="#f5f5f5",    # Off-white text
    title_font_color="#f5f5f5",
    legend_title_font_color="#f5f5f5"
)
st.plotly_chart(fig1, use_container_width=True)

# Yearly Sales Bar Chart
yearly_sales = filtered_df.groupby(filtered_df['INVOICE DATE'].dt.year)['TOTAL'].sum().reset_index()
yearly_sales.columns = ['YEAR', 'TOTAL']
fig2 = px.bar(
    yearly_sales,
    x='YEAR',
    y='TOTAL',
    title='Yearly Sales',
    labels={'YEAR': 'Year', 'TOTAL': 'Total Sales ($)'},
    text=yearly_sales['TOTAL'].round(2),
    color_discrete_sequence=["#d4a017"]  # Golden amber bars
)
fig2.update_traces(textposition='auto')
fig2.update_layout(
    plot_bgcolor="#0a1e3d",
    paper_bgcolor="#0a1e3d",
    font_color="#f5f5f5",
    title_font_color="#f5f5f5",
    legend_title_font_color="#f5f5f5"
)
st.plotly_chart(fig2, use_container_width=True)

# Product Analysis
st.subheader('Product Analysis')
product_sales = filtered_df.groupby('PRODUCT NAME')['TOTAL'].sum().sort_values(ascending=False).reset_index()
fig3 = px.bar(
    product_sales.head(10),
    x='PRODUCT NAME',
    y='TOTAL',
    title='Top 10 Product Categories by Sales',
    labels={'PRODUCT NAME': 'Product Category', 'TOTAL': 'Total Sales ($)'},
    color_discrete_sequence=["#d4a017"]  # Golden amber bars
)
fig3.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="#0a1e3d",
    paper_bgcolor="#0a1e3d",
    font_color="#f5f5f5",
    title_font_color="#f5f5f5"
)
st.plotly_chart(fig3, use_container_width=True)

# Product Sales Breakdown (Treemap)
st.subheader('Product Sales Breakdown')
product_sales = filtered_df.groupby('PRODUCT NAME')['TOTAL'].sum().reset_index()
fig_treemap = px.treemap(
    product_sales,
    path=['PRODUCT NAME'],
    values='TOTAL',
    title='Product Sales Treemap',
    color='TOTAL',
    color_continuous_scale=[(0, "#1e3a6d"), (0.5, "#d4a017"), (1, "#f5f5f5")]  # Custom scale
)
fig_treemap.update_layout(
    plot_bgcolor="#0a1e3d",
    paper_bgcolor="#0a1e3d",
    font_color="#f5f5f5",
    title_font_color="#f5f5f5"
)
st.plotly_chart(fig_treemap, use_container_width=True)

# Customer Analysis
st.subheader('Customer Analysis')
customer_sales = filtered_df.groupby('CUSTOMER NAME')['TOTAL'].sum().sort_values(ascending=False).reset_index()
fig4 = px.bar(
    customer_sales.head(10),
    x='CUSTOMER NAME',
    y='TOTAL',
    title='Top 10 Customers by Sales',
    labels={'CUSTOMER NAME': 'Customer', 'TOTAL': 'Total Sales ($)'},
    color_discrete_sequence=["#d4a017"]  # Golden amber bars
)
fig4.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor="#0a1e3d",
    paper_bgcolor="#0a1e3d",
    font_color="#f5f5f5",
    title_font_color="#f5f5f5"
)
st.plotly_chart(fig4, use_container_width=True)

# Pie Charts for VIP Status and Custom vs Stock
col1, col2 = st.columns(2)

with col1:
    vip_sales = filtered_df.groupby('VIP/POTENTIAL_LOYAL')['TOTAL'].sum().reset_index()
    fig5 = px.pie(
        vip_sales,
        values='TOTAL',
        names='VIP/POTENTIAL_LOYAL',
        title='Sales Distribution by Status',
        color_discrete_sequence=["#d4a017", "#1e3a6d", "#f5f5f5"]  # Amber, blue, off-white
    )
    fig5.update_layout(
        plot_bgcolor="#0a1e3d",
        paper_bgcolor="#0a1e3d",
        font_color="#f5f5f5",
        title_font_color="#f5f5f5"
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    cust_stock_sales = filtered_df.groupby('CUST/STOCK')['TOTAL'].sum().reset_index()
    fig6 = px.pie(
        cust_stock_sales,
        values='TOTAL',
        names='CUST/STOCK',
        title='Sales by Custom vs. Stock',
        color_discrete_sequence=["#d4a017", "#1e3a6d"]  # Amber and blue
    )
    fig6.update_layout(
        plot_bgcolor="#0a1e3d",
        paper_bgcolor="#0a1e3d",
        font_color="#f5f5f5",
        title_font_color="#f5f5f5"
    )
    st.plotly_chart(fig6, use_container_width=True)