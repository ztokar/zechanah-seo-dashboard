
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit page configuration
st.set_page_config(
    page_title="Zechanah Tokar SEO Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Zechanah Tokar branding
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: bold;
    }
    .kpi-card {
        background-color: #333333;
        border: 1px solid #00FF00;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .kpi-value {
        color: #00FF00;
        font-size: 32px;
        font-weight: bold;
    }
    .kpi-label {
        color: #FFFFFF;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Placeholder GSC Data
def get_data():
    dates = pd.date_range(datetime.now() - timedelta(days=29), datetime.now())
    data = {
        'date': dates,
        'clicks': [50 + i * 2 for i in range(len(dates))],
        'impressions': [300 + i * 5 for i in range(len(dates))]
    }
    queries = pd.DataFrame({
        'Query': ['seo tips', 'keyword research', 'backlinks', 'meta tags', 'google ranking'],
        'Clicks': [500, 300, 200, 150, 100],
        'Impressions': [2000, 1500, 1000, 800, 600],
        'CTR': [25, 20, 20, 18.75, 16.67],
        'Position': [1.8, 2.5, 3.2, 3.8, 4.4]
    })
    pages = pd.DataFrame({
        'Page': ['/seo-tips', '/research', '/links', '/tags', '/ranking'],
        'Clicks': [400, 320, 180, 130, 90],
        'Impressions': [1800, 1600, 900, 700, 500],
        'CTR': [22.2, 20.0, 20.0, 18.6, 18.0],
        'Position': [1.9, 2.2, 3.0, 3.5, 4.0]
    })
    devices = pd.DataFrame({
        'Device': ['Desktop', 'Mobile', 'Tablet'],
        'Clicks': [1000, 1500, 300],
        'Impressions': [4000, 6000, 1000]
    })
    countries = pd.DataFrame({
        'Country': ['USA', 'UK', 'India', 'Canada', 'Australia'],
        'Impressions': [5000, 3000, 2000, 1000, 800]
    })
    return pd.DataFrame(data), queries, pages, devices, countries

# Load data
performance_df, queries_df, pages_df, devices_df, countries_df = get_data()

# Layout
st.markdown("""
    <div style="background: linear-gradient(to right, #00FF00, #000000); padding: 20px; text-align: center;">
        <h1 style="font-size: 24px;">Zechanah Tokar SEO Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# KPI Cards
st.markdown("<h2>Key Metrics</h2>", unsafe_allow_html=True)
kpi_cols = st.columns(4)
total_clicks = performance_df['clicks'].sum()
total_impressions = performance_df['impressions'].sum()
avg_ctr = round((total_clicks / total_impressions) * 100, 1)
avg_position = 3.6  # Placeholder

metrics = [
    (total_clicks, "Total Clicks"),
    (total_impressions, "Total Impressions"),
    (f"{avg_ctr}%", "Average CTR"),
    (avg_position, "Average Position")
]

for i in range(4):
    with kpi_cols[i]:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{metrics[i][0]}</div>
                <div class="kpi-label">{metrics[i][1]}</div>
            </div>
        """, unsafe_allow_html=True)

# Charts
st.markdown("### Performance Trend")
fig = go.Figure()
fig.add_trace(go.Scatter(x=performance_df['date'], y=performance_df['clicks'], name='Clicks', line=dict(color='#00FF00')))
fig.add_trace(go.Scatter(x=performance_df['date'], y=performance_df['impressions'], name='Impressions', line=dict(color='#FFFFFF')))
fig.update_layout(
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    font_color='#FFFFFF',
    xaxis_title='Date',
    yaxis_title='Value'
)
st.plotly_chart(fig, use_container_width=True)

# Tables
st.markdown("### Top Queries")
st.dataframe(queries_df)

st.markdown("### Top Pages")
st.dataframe(pages_df)

st.markdown("### Device Breakdown")
fig_device = px.pie(devices_df, names='Device', values='Clicks', color_discrete_sequence=['#00FF00', '#FFFFFF', '#333333'])
st.plotly_chart(fig_device, use_container_width=True)
