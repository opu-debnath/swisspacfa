import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

# Set up the page configuration
st.set_page_config(page_title="Model Evaluation", layout="wide")
st.title("Model Evaluation and Insights")
st.write("This page presents the evaluation of models used for customer purchase forecasting, including clustering for segmentation and performance metrics for both BG/NBD and deep learning models.")
st.write("Note:- We have trained the model upto 2023 dec data and later test the model on 2024 data.")
# Define the path to your image folder (adjust this based on your setup)
image_folder = os.path.join(os.getcwd(), "data", "images")

# Section: LSTM vs Other Models for Quarter-Wise Sales Probability Predictions
st.subheader("LSTM vs. Other Models for Quarter-Wise Sales Probability Predictions")
st.write("This section compares different deep learning models used to predict the probability of customer purchases in each quarter. The models were evaluated using Test AUC and Hamming Loss.")

# Create a table with model comparison data
model_data = {
    "Model": [
        "LSTM (32) + Dense (32)", 
        "LSTM (64) + Dense (32)", 
        "LSTM (128) + Dense (32)", 
        "LSTM Bidirectional (64)", 
        "GRU (64)"
    ],
    "Test AUC": [0.8211, 0.8240, 0.8154, 0.7697, 0.8134],
    "Hamming Loss": [0.2583, 0.2433, 0.2533, 0.2888, 0.2450]
}
model_df = pd.DataFrame(model_data)
st.write("**Model Performance Comparison Table**")
st.dataframe(model_df)

# Add a note on threshold tuning
st.write("Threshold tuning was performed for the LSTM (64) + Dense (32) model by testing thresholds from 0.1 to 0.9. The best threshold was found to be 0.5, achieving a Hamming Loss of 0.2433.")

# Bar chart comparison using Plotly
st.write("**Model Performance Comparison Graph**")
fig = go.Figure()
fig.add_trace(go.Bar(
    x=model_df["Model"], 
    y=model_df["Test AUC"], 
    name="Test AUC", 
    marker_color="skyblue",
    text=[f"{x:.4f}" for x in model_df["Test AUC"]],
    textposition="auto"
))
fig.add_trace(go.Bar(
    x=model_df["Model"], 
    y=model_df["Hamming Loss"], 
    name="Hamming Loss", 
    marker_color="salmon",
    text=[f"{x:.4f}" for x in model_df["Hamming Loss"]],
    textposition="auto"
))
fig.update_layout(
    title="Comparison of Test AUC and Hamming Loss Across Models",
    xaxis_title="Model",
    yaxis_title="Score",
    barmode="group",
    legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# Display the ROC curve screenshot for the best model
st.write("**ROC Curve for LSTM (64) + Dense (32) Model**")
st.write("This plot shows the Receiver Operating Characteristic (ROC) curve for the best-performing model, illustrating its ability to distinguish between positive and negative classes.")
try:
    roc_curve_plot = os.path.join(image_folder, "new_roc.png")
    st.image(roc_curve_plot, use_container_width=True)
except FileNotFoundError:
    st.error("ROC curve plot not found. Please check the file path: data/images/new_roc.png")

# Explanation of metrics
with st.expander("Understanding AUC and Hamming Loss"):
    st.write("""
    - **AUC (Area Under the Curve)**: Measures the model's ability to distinguish between classes. AUC ranges from 0 to 1, with higher values indicating better performance.
    - **Hamming Loss**: Measures the fraction of incorrect predictions. Lower values are better, with 0 being perfect.
    """)

# Section 1: Clustering Evaluation
st.subheader("Clustering Evaluation for Customer Segmentation")
st.write("Customer segmentation was performed using K-means clustering based on RFM (Recency, Frequency, Monetary) analysis. The following visuals assess the clustering performance.")

# Elbow Method Plot
st.write("**Elbow Method for K-means Clustering**")
st.write("This plot shows the distortion score to determine the optimal number of clusters.")
try:
    elbow_plot = os.path.join(image_folder, "elbow_method.png")
    st.image(elbow_plot, use_container_width=True)
except FileNotFoundError:
    st.error("Elbow Method plot not found. Please check the file path: data/images/elbow_method.png")

# Silhouette Score Comparison Table
st.write("**Silhouette Scores: K-means vs. GMM Comparison Table**")
st.write("This table compares the Silhouette Scores for K-means and Gaussian Mixture Models (GMM).")
try:
    silhouette_table = os.path.join(image_folder, "silhouette_table.png")
    st.image(silhouette_table, use_container_width=True)
except FileNotFoundError:
    st.error("Silhouette Score table not found. Please check the file path: data/images/silhouette_table.png")

# Silhouette Score Comparison Graph
st.write("**Silhouette Scores: K-means vs. GMM Comparison Graph**")
st.write("This graph visualizes the Silhouette Score comparison between K-means and GMM.")
try:
    silhouette_graph = os.path.join(image_folder, "silhouette_graph.png")
    st.image(silhouette_graph, use_container_width=True)
except FileNotFoundError:
    st.error("Silhouette Score graph not found. Please check the file path: data/images/silhouette_graph.png")

# RFM Clusters Plot
st.write("**RFM Clusters Using K-means**")
st.write("This plot shows the resulting customer segments based on RFM analysis with K-means.")
try:
    rfm_clusters = os.path.join(image_folder, "rfm_clusters.png")
    st.image(rfm_clusters, use_container_width=True)
except FileNotFoundError:
    st.error("RFM clusters plot not found. Please check the file path: data/images/rfm_clusters.png")

# Section 2: BG/NBD Model Performance Metrics
st.subheader("BG/NBD Model Performance Metrics")
st.write("The BG/NBD model predicts customer purchase behavior. Below are the metrics for VIP and Potential Loyal customers, compared to a Naive baseline model.")

# VIP Customers Metrics
st.write("**VIP Customers**")
st.write("- **BG/NBD Model**: MAE = 2.96, R² = 0.48")
st.write("- **Naive Model**: MAE = 33.00, R² = -64.52")

# Potential Loyal Customers Metrics
st.write("**Potential Loyal Customers**")
st.write("- **BG/NBD Model**: MAE = 2.76, R² = 0.14")
st.write("- **Naive Model**: MAE = 21.01, R² = -37.30")

# Section 3: Actual vs. Predicted Purchases
st.subheader("Actual vs. Predicted Purchases")
st.write("These plots compare the actual and predicted purchase counts for VIP and Potential Loyal customers using the BG/NBD model.")

# VIP Customers Plot
st.write("**VIP Customers: Actual vs. Predicted Purchases**")
try:
    vip_plot = os.path.join(image_folder, "vip_actual_vs_predicted.png")
    st.image(vip_plot, use_container_width=True)
except FileNotFoundError:
    st.error("VIP actual vs. predicted plot not found. Please check the file path: data/images/vip_actual_vs_predicted.png")

# Potential Loyal Customers Plot
st.write("**Potential Loyal Customers: Actual vs. Predicted Purchases**")
try:
    potential_loyal_plot = os.path.join(image_folder, "potential_loyal_actual_vs_predicted.png")
    st.image(potential_loyal_plot, use_container_width=True)
except FileNotFoundError:
    st.error("Potential Loyal actual vs. predicted plot not found. Please check the file path: data/images/potential_loyal_actual_vs_predicted.png")

# Optional: Explanations
with st.expander("Understanding the Metrics and Plots"):
    st.write("""
    - **MAE (Mean Absolute Error)**: Measures the average difference between predicted and actual purchases. Lower values indicate better predictions.
    - **R² (R-squared)**: Shows how well the model fits the data. Values closer to 1 are better; negative values (as in the Naive Model) indicate poor performance compared to a simple average.
    - **Silhouette Score**: Assesses clustering quality. Scores closer to 1 mean well-separated clusters.
    - **Elbow Method**: Identifies the optimal number of clusters by finding where adding more clusters yields diminishing returns in distortion score reduction.
    """)