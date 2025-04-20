
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Zechanah Tokar SEO Dashboard", layout="wide")

# Branding header
st.markdown("""
    <div style="background: linear-gradient(to right, #00FF00, #000000); padding: 20px; text-align: center;">
        <h1 style="color: #FFFFFF; font-family: 'Poppins', sans-serif;">Zechanah Tokar SEO Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# File uploader
st.sidebar.header("📤 Upload Your GSC CSV Files")
dates_file = st.sidebar.file_uploader("Upload Dates.csv", type="csv")
queries_file = st.sidebar.file_uploader("Upload Queries.csv", type="csv")
pages_file = st.sidebar.file_uploader("Upload Pages.csv", type="csv")
devices_file = st.sidebar.file_uploader("Upload Devices.csv", type="csv")
countries_file = st.sidebar.file_uploader("Upload Countries.csv", type="csv")

# Load files
if dates_file and queries_file and pages_file and devices_file and countries_file:
    dates_df = pd.read_csv(dates_file)
    queries_df = pd.read_csv(queries_file)
    pages_df = pd.read_csv(pages_file)
    devices_df = pd.read_csv(devices_file)
    countries_df = pd.read_csv(countries_file)

    # Clean CTR %
    if 'CTR' in dates_df.columns:
        dates_df['CTR'] = dates_df['CTR'].str.rstrip('%').astype(float)
    if 'CTR' in queries_df.columns:
        queries_df['CTR'] = queries_df['CTR'].str.rstrip('%').astype(float)
    if 'CTR' in pages_df.columns:
        pages_df['CTR'] = pages_df['CTR'].str.rstrip('%').astype(float)

    # KPI metrics
    st.markdown("""<h2 style='color:#FFFFFF;'>📊 Key Metrics</h2>""", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Clicks", int(dates_df['Clicks'].sum()))
    with col2:
        st.metric("Total Impressions", int(dates_df['Impressions'].sum()))
    with col3:
        st.metric("Average CTR", f"{dates_df['CTR'].mean():.1f}%")
    with col4:
        st.metric("Average Position", f"{dates_df['Position'].mean():.1f}")

    # Trend Chart
    st.markdown("""<h3 style='color:#FFFFFF;'>📈 Clicks & Impressions Over Time</h3>""", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates_df['Date'], y=dates_df['Clicks'], mode='lines', name='Clicks', line=dict(color='#00FF00')))
    fig.add_trace(go.Scatter(x=dates_df['Date'], y=dates_df['Impressions'], mode='lines', name='Impressions', line=dict(color='#FFFFFF')))
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    # Top Queries
    st.markdown("""<h3 style='color:#FFFFFF;'>🔎 Top Search Queries</h3>""", unsafe_allow_html=True)
    st.dataframe(queries_df.head(5))

    # Top Pages
    st.markdown("""<h3 style='color:#FFFFFF;'>📄 Top Pages</h3>""", unsafe_allow_html=True)
    st.dataframe(pages_df.head(5))

    # Devices Pie Chart
    st.markdown("""<h3 style='color:#FFFFFF;'>📱 Device Breakdown</h3>""", unsafe_allow_html=True)
    fig_device = px.pie(devices_df, names='Device', values='Clicks', color_discrete_sequence=['#00FF00', '#FFFFFF', '#333333'])
    fig_device.update_layout(template='plotly_dark')
    st.plotly_chart(fig_device, use_container_width=True)

    # Countries Bar Chart
    st.markdown("""<h3 style='color:#FFFFFF;'>🌍 Top Countries by Impressions</h3>""", unsafe_allow_html=True)
    fig_country = px.bar(countries_df.sort_values(by='Impressions', ascending=True), 
                         x='Impressions', y='Country', orientation='h',
                         color='Impressions', color_continuous_scale=['#333333', '#00FF00'])
    fig_country.update_layout(template='plotly_dark')
    st.plotly_chart(fig_country, use_container_width=True)

else:
    st.info("⬅️ Upload all 5 required CSV files from Google Search Console to view your dashboard.")

# Footer
st.markdown("""<div style='text-align:center; color:#00FF00;'>Powered by Zechanah Tokar · www.zechanahtokar.com</div>""", unsafe_allow_html=True)
