import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration for a wide, professional layout
st.set_page_config(page_title="HCI Direct SEO Dashboard", layout="wide", page_icon="📊")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stMetric {background-color: #ffffff; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    .stSidebar {background-color: #ffffff;}
    h1 {color: #2c3e50; font-family: 'Arial', sans-serif;}
    .stButton>button {background-color: #3498db; color: white; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# Load CSV files
@st.cache_data
def load_data():
    countries = pd.read_csv("Countries.csv")
    dates = pd.read_csv("Dates.csv")
    devices = pd.read_csv("Devices.csv")
    pages = pd.read_csv("Pages.csv")
    queries = pd.read_csv("Queries.csv")
    search_appearance = pd.read_csv("Search appearance.csv")
    
    # Clean data
    for df in [countries, dates, devices, pages, queries, search_appearance]:
        df['CTR'] = df['CTR'].str.rstrip('%').astype(float)
    
    # Convert Date to datetime
    dates['Date'] = pd.to_datetime(dates['Date'])
    
    return countries, dates, devices, pages, queries, search_appearance

countries, dates, devices, pages, queries, search_appearance = load_data()

# Sidebar for filters
st.sidebar.header("Filter Options")
date_range = st.sidebar.date_input("Select Date Range", 
                                   [dates['Date'].min(), dates['Date'].max()])
country = st.sidebar.selectbox("Select Country", ["All"] + list(countries['Country'].unique()))
device = st.sidebar.selectbox("Select Device", ["All"] + list(devices['Device'].unique()))

# Filter data
filtered_dates = dates[(dates['Date'] >= pd.to_datetime(date_range[0])) & 
                      (dates['Date'] <= pd.to_datetime(date_range[1]))]
filtered_countries = countries if country == "All" else countries[countries['Country'] == country]
filtered_devices = devices if device == "All" else devices[devices['Device'] == device]

# Main dashboard title
st.title("📈 HCI Direct SEO Performance Dashboard")
st.markdown("Analyze SEO metrics for hcidirect.co.uk from Google Search Console")

# KPIs
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clicks", f"{int(dates['Clicks'].sum())}", 
            delta=f"{int(filtered_dates['Clicks'].sum() - dates['Clicks'].sum())}")
col2.metric("Total Impressions", f"{int(dates['Impressions'].sum())}", 
            delta=f"{int(filtered_dates['Impressions'].sum() - dates['Impressions'].sum())}")
col3.metric("Average CTR", f"{dates['CTR'].mean():.2f}%", 
            delta=f"{filtered_dates['CTR'].mean() - dates['CTR'].mean():.2f}%")
col4.metric("Average Position", f"{dates['Position'].mean():.2f}", 
            delta=f"{filtered_dates['Position'].mean() - dates['Position'].mean():.2f}")

# Visualizations
st.subheader("Performance Over Time")
fig_time = px.line(filtered_dates, x="Date", y=["Clicks", "Impressions"], 
                   title="Clicks and Impressions Trend",
                   labels={"value": "Count", "variable": "Metric"})
fig_time.update_layout(hovermode="x unified", template="plotly_white")
st.plotly_chart(fig_time, use_container_width=True)

st.subheader("Top Queries by Clicks")
fig_queries = px.bar(queries.head(10), x="Top queries", y="Clicks", 
                     title="Top 10 Search Queries",
                     color="CTR", color_continuous_scale="Viridis")
fig_queries.update_layout(template="plotly_white")
st.plotly_chart(fig_queries, use_container_width=True)

st.subheader("Top Pages by Clicks")
fig_pages = px.bar(pages.head(10), x="Top pages", y="Clicks", 
                   title="Top 10 Pages",
                   color="CTR", color_continuous_scale="Plasma")
fig_pages.update_layout(template="plotly_white", xaxis_tickangle=45)
st.plotly_chart(fig_pages, use_container_width=True)

st.subheader("Performance by Country")
fig_countries = px.choropleth(filtered_countries, 
                              locations="Country", 
                              locationmode="country names",
                              color="Clicks",
                              hover_data=["Impressions", "CTR", "Position"],
                              title="Clicks by Country",
                              color_continuous_scale="Blues")
fig_countries.update_layout(template="plotly_white")
st.plotly_chart(fig_countries, use_container_width=True)

st.subheader("Device Breakdown")
fig_devices = px.pie(filtered_devices, names="Device", values="Clicks", 
                     title="Clicks by Device",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
fig_devices.update_layout(template="plotly_white")
st.plotly_chart(fig_devices, use_container_width=True)

st.subheader("Search Appearance")
fig_search = px.bar(search_appearance, x="Search Appearance", y="Clicks", 
                    title="Clicks by Search Appearance",
                    color="CTR", color_continuous_scale="Inferno")
fig_search.update_layout(template="plotly_white")
st.plotly_chart(fig_search, use_container_width=True)

# Data tables
st.subheader("Detailed Data")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Queries", "Pages", "Countries", "Devices", "Search Appearance"])
with tab1:
    st.dataframe(queries)
with tab2:
    st.dataframe(pages)
with tab3:
    st.dataframe(filtered_countries)
with tab4:
    st.dataframe(filtered_devices)
with tab5:
    st.dataframe(search_appearance)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Data from Google Search Console")
