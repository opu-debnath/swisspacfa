import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set up the page
st.set_page_config(page_title="2025 Forecasting", layout="wide")
st.title(":dart: 2025 Forecasting Section")
st.write("~ Explore predictions and customer segmentation for 2025.")

# Path to your data file
cluster_summary_path = "data/cluster_summary.xlsx"


cluster_summary_path = "data/new_cluster_summary.xlsx"
rfm_path = 'data/new_rfm.xlsx'
vip_predictions_path = "data/new_vip_frequency_prediction.xlsx"
potential_loyal_predictions_path = "data/new_potential_loyalist_frequency_predictions.xlsx"
vip_quarter_prob_path = "data/new_vip_quater_predictions.xlsx"
potential_loyal_quarter_prob_path = "data/new_potential_loyalist_quater_predictions.xlsx"
# model_metrics_path = os.path.join(data_folder, "model_metrics.csv")


# Function to load data
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

# # Load and display cluster summary
# try:
#     cluster_summary = load_data(cluster_summary_path)
#     st.subheader("Customer Segmentation Summary")
#     st.dataframe(cluster_summary)  # Show the table
# except FileNotFoundError:
#     st.error("Error: Could not find the cluster summary file at the specified path.")

# Load all CSV files
try:
    cluster_summary = load_data(cluster_summary_path)
    rfm = load_data(rfm_path)
    vip_predictions = load_data(vip_predictions_path)
    potential_loyal_predictions = load_data(potential_loyal_predictions_path)
    # model_metrics = load_data(model_metrics_path)
except FileNotFoundError as e:
    st.error("Error: Could not find the cluster summary file at the specified path.")
    st.stop()

# Subsection 1: Customer Segmentation Summary & RFM
with st.expander("Customer Segmentation Summary", expanded=False):
    st.write("Segments derived from RFM analysis and K-means clustering (k=4, Silhouette score: 0.51).")
    st.dataframe(cluster_summary)
    # Optional: Add a simple visualization (e.g., bar chart of cluster sizes)
    fig_clusters = px.bar(cluster_summary, x="Cluster", y="Count", 
                          title="Number of Customers per Cluster")
    st.plotly_chart(fig_clusters, use_container_width=True)

with st.expander("RFM Value For All VIP & Potential Loyal Customers", expanded=False):
    st.dataframe(rfm)

# Subsection 2: VIP Customer Predictions
with st.expander("VIP Customer Sales Frequency Predictions ~ 2025", expanded=False):
    st.write("Predicted purchases for VIP customers using the BG/NBD model.")
    vip_predictions = vip_predictions.rename(columns={
    'CLV_2025': 'CLV_2025 ($)',
    'predicted_purchases_2025': 'predicted_purchases_2025 (frequency)'})
    st.dataframe(vip_predictions)
    fig_vip = px.bar(vip_predictions, x="CUSTOMER NAME", y="predicted_purchases_2025 (frequency)", 
                     hover_name="CUSTOMER NAME",
                     title="Predicted Purchases for VIP Customers")
    fig_vip.update_layout(
        title={
            'text': "Predicted Purchases for VIP Customers",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
            title="CUSTOMER NAME (Hover Over the Bar)",
    )
    )
    st.plotly_chart(fig_vip, use_container_width=True)

# Subsection 3: Potential Loyal Customer Predictions
with st.expander("Potential Loyal Customer Sales Predictions ~ 2025", expanded=False):
    st.write("Predicted purchases for Potential Loyalists using the BG/NBD model.")
    potential_loyal_predictions = potential_loyal_predictions.rename(columns={
    'CLV_2025': 'CLV_2025 ($)',
    'predicted_purchases_2025': 'predicted_purchases_2025 (frequency)'})
    st.dataframe(potential_loyal_predictions)
    fig_potential = px.bar(potential_loyal_predictions, x="CUSTOMER NAME", y="predicted_purchases_2025 (frequency)", 
                           hover_name="CUSTOMER NAME",
                           title="Predicted Purchases for Potential Loyalists Customers")
    fig_potential.update_layout(
        title={
            'text': "Predicted Purchases for Potential Loyalist Customers",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis=dict(
        title="CUSTOMER NAME (Hover Over the Bar)",
        showticklabels=False  # This hides customer names on x-axis
    )
)
    st.plotly_chart(fig_potential, use_container_width=True)


# Subsection 4: VIP Customer Quarter-Wise Purchase Probabilities
with st.expander("VIP Customer Quarter-Wise Purchase Probabilities ~ 2025", expanded=False):
    try:
        # Load the VIP customer data
        vip_quarter_prob = load_data(vip_quarter_prob_path)
        
        # Quarter selection dropdown with "All" option
        quarter_options = ["All", "Q1", "Q2", "Q3", "Q4"]
        selected_quarter = st.selectbox("Select Quarter for VIP Customers", quarter_options)
        
        if selected_quarter == "All":
            # Display the full dataframe with all columns
            st.dataframe(vip_quarter_prob)
            # Download the full dataset
            csv = vip_quarter_prob.to_csv(index=False)
            st.download_button(
                label="Download All Data for VIP Customers",
                data=csv,
                file_name="vip_all_quarters_probabilities.csv",
                mime="text/csv"
            )
        else:
            # Filter data for the selected quarter
            quarter_column = f"{selected_quarter}_Prob (%)"
            filtered_vip_quarter = vip_quarter_prob[["Customer", quarter_column]]
            st.dataframe(filtered_vip_quarter)
            # Download the filtered data
            csv = filtered_vip_quarter.to_csv(index=False)
            st.download_button(
                label=f"Download {selected_quarter} Data for VIP Customers",
                data=csv,
                file_name=f"vip_{selected_quarter}_probabilities.csv",
                mime="text/csv"
            )
        
        # Placeholder for bar chart (uncomment and adjust as needed)
        # st.plotly_chart(your_vip_barchart_function(vip_quarter_prob))
        
    except FileNotFoundError:
        st.error("Error: Could not find the VIP quarter probabilities file.")

# Subsection 5: Potential Loyal Customer Quarter-Wise Purchase Probabilities
with st.expander("Potential Loyal Customer Quarter-Wise Purchase Probabilities ~ 2025", expanded=False):
    try:
        # Load the Potential Loyal customer data
        potential_loyal_quarter_prob = load_data(potential_loyal_quarter_prob_path)
        
        # Quarter selection dropdown with "All" option
        quarter_options = ["All", "Q1", "Q2", "Q3", "Q4"]
        selected_quarter = st.selectbox("Select Quarter for Potential Loyal Customers", quarter_options)
        
        if selected_quarter == "All":
            # Display the full dataframe with all columns
            st.dataframe(potential_loyal_quarter_prob)
            # Download the full dataset
            csv = potential_loyal_quarter_prob.to_csv(index=False)
            st.download_button(
                label="Download All Data for Potential Loyal Customers",
                data=csv,
                file_name="potential_loyal_all_quarters_probabilities.csv",
                mime="text/csv"
            )
        else:
            # Filter data for the selected quarter
            quarter_column = f"{selected_quarter}_Prob (%)"
            filtered_potential_loyal_quarter = potential_loyal_quarter_prob[["Customer", quarter_column]]
            st.dataframe(filtered_potential_loyal_quarter)
            # Download the filtered data
            csv = filtered_potential_loyal_quarter.to_csv(index=False)
            st.download_button(
                label=f"Download {selected_quarter} Data for Potential Loyal Customers",
                data=csv,
                file_name=f"potential_loyal_{selected_quarter}_probabilities.csv",
                mime="text/csv"
            )
        
        # Placeholder for bar chart (uncomment and adjust as needed)
        # st.plotly_chart(your_potential_loyal_barchart_function(potential_loyal_quarter_prob))
        
    except FileNotFoundError:
        st.error("Error: Could not find the Potential Loyal quarter probabilities file.")