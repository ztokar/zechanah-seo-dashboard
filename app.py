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

# Load CSV files with caching
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

# Sidebar for date range filter
st.sidebar.header("Filter Options")
date_range = st.sidebar.date_input("Select Date Range", 
                                   [dates['Date'].min(), dates['Date'].max()])

# Filter data
filtered_dates = dates[(dates['Date'] >= pd.to_datetime(date_range[0])) & 
                      (dates['Date'] <= pd.to_datetime(date_range[1]))]

# Main dashboard title
st.title("📈 HCI Direct SEO Performance Dashboard")
st.markdown("Analyze SEO metrics for hcidirect.co.uk from Google Search Console")

# Key Metrics (for selected date range)
st.subheader("Key Metrics (for selected date range)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Clicks", f"{int(filtered_dates['Clicks'].sum())}")
col2.metric("Total Impressions", f"{int(filtered_dates['Impressions'].sum())}")
col3.metric("Average CTR", f"{filtered_dates['CTR'].mean():.2f}%")
col4.metric("Average Position", f"{filtered_dates['Position'].mean():.2f}")

# Performance Over Time
st.subheader("Performance Over Time")
metrics = st.multiselect("Select metrics", ["Clicks", "Impressions", "CTR", "Position"], 
                         default=["Clicks", "Impressions"])
fig_time = px.line(filtered_dates, x="Date", y=metrics, 
                   title="Performance Trend",
                   labels={"value": "Value", "variable": "Metric"})
fig_time.update_layout(hovermode="x unified", template="plotly_white")
st.plotly_chart(fig_time, use_container_width=True)

# Correlation Heatmap
st.subheader("Correlation Between Metrics")
corr_matrix = filtered_dates[["Clicks", "Impressions", "CTR", "Position"]].corr()
fig_corr = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.index,
    colorscale="Viridis",
    zmin=-1, zmax=1,
    text=corr_matrix.values.round(2),
    texttemplate="%{text}",
    hovertemplate="%{x} vs %{y}: %{z:.2f}"
))
fig_corr.update_layout(title="Correlation Heatmap", template="plotly_white")
st.plotly_chart(fig_corr, use_container_width=True)

# Top Queries by Clicks
st.subheader("Top Queries by Clicks")
top_n_queries = st.slider("Show top N queries", 5, 20, 10)
fig_queries = px.bar(queries.head(top_n_queries), x="Top queries", y="Clicks", 
                     title=f"Top {top_n_queries} Search Queries",
                     color="CTR", color_continuous_scale="Viridis")
fig_queries.update_layout(template="plotly_white")
st.plotly_chart(fig_queries, use_container_width=True)

# Top Pages by Clicks
st.subheader("Top Pages by Clicks")
top_n_pages = st.slider("Show top N pages", 5, 20, 10)
fig_pages = px.bar(pages.head(top_n_pages), x="Top pages", y="Clicks", 
                   title=f"Top {top_n_pages} Pages",
                   color="CTR", color_continuous_scale="Plasma")
fig_pages.update_layout(template="plotly_white", xaxis_tickangle=45)
st.plotly_chart(fig_pages, use_container_width=True)

# Performance by Country
st.subheader("Performance by Country")
map_metric = st.selectbox("Select metric for map", ["Clicks", "Impressions", "CTR", "Position"])
fig_countries = px.choropleth(countries, 
                              locations="Country", 
                              locationmode="country names",
                              color=map_metric,
                              hover_data=["Clicks", "Impressions", "CTR", "Position"],
                              title=f"{map_metric} by Country",
                              color_continuous_scale="Blues")
fig_countries.update_layout(template="plotly_white")
st.plotly_chart(fig_countries, use_container_width=True)

# Device Breakdown
st.subheader("Device Breakdown")
device_metric = st.selectbox("Select metric for device breakdown", ["Clicks", "Impressions", "CTR", "Position"])
fig_devices = px.pie(devices, names="Device", values=device_metric, 
                     title=f"{device_metric} by Device",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
fig_devices.update_layout(template="plotly_white")
st.plotly_chart(fig_devices, use_container_width=True)

# Search Appearance
st.subheader("Search Appearance")
search_metric = st.selectbox("Select metric for search appearance", ["Clicks", "Impressions", "CTR", "Position"])
fig_search = px.bar(search_appearance, x="Search Appearance", y=search_metric, 
                    title=f"{search_metric} by Search Appearance",
                    color="CTR", color_continuous_scale="Inferno")
fig_search.update_layout(template="plotly_white")
st.plotly_chart(fig_search, use_container_width=True)

# Detailed Data Tabs
st.subheader("Detailed Data")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Queries", "Pages", "Countries", "Devices", "Search Appearance"])
with tab1:
    st.dataframe(queries)
    st.download_button(label="Download Queries Data", 
                       data=queries.to_csv(index=False).encode('utf-8'), 
                       file_name='queries.csv', mime='text/csv')
with tab2:
    st.dataframe(pages)
    st.download_button(label="Download Pages Data", 
                       data=pages.to_csv(index=False).encode('utf-8'), 
                       file_name='pages.csv', mime='text/csv')
with tab3:
    st.dataframe(countries)
    st.download_button(label="Download Countries Data", 
                       data=countries.to_csv(index=False).encode('utf-8'), 
                       file_name='countries.csv', mime='text/csv')
with tab4:
    st.dataframe(devices)
    st.download_button(label="Download Devices Data", 
                       data=devices.to_csv(index=False).encode('utf-8'), 
                       file_name='devices.csv', mime='text/csv')
with tab5:
    st.dataframe(search_appearance)
    st.download_button(label="Download Search Appearance Data", 
                       data=search_appearance.to_csv(index=False).encode('utf-8'), 
                       file_name='search_appearance.csv', mime='text/csv')

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Data from Google Search Console")
