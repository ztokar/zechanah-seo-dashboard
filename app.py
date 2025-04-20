
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Zechanah Tokar SEO Dashboard", layout="wide")

# Custom Header with Branding
st.markdown("""
    <div style="background: linear-gradient(to right, #00FF00, #000000); padding: 30px 0; text-align: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Picton_Upload_arrow_up.svg/240px-Picton_Upload_arrow_up.svg.png" width="60" />
        <h1 style="color:#fff; font-family:Poppins,sans-serif; font-size:32px;">Zechanah Tokar SEO Dashboard</h1>
        <p style="color:#ccc;">Interactive performance insights using Google Search Console data</p>
    </div>
""", unsafe_allow_html=True)

# Upload files sidebar
st.sidebar.header("📤 Upload GSC CSV Files")
dates_file = st.sidebar.file_uploader("Upload Dates.csv", type="csv")
queries_file = st.sidebar.file_uploader("Upload Queries.csv", type="csv")
pages_file = st.sidebar.file_uploader("Upload Pages.csv", type="csv")
devices_file = st.sidebar.file_uploader("Upload Devices.csv", type="csv")
countries_file = st.sidebar.file_uploader("Upload Countries.csv", type="csv")

if all([dates_file, queries_file, pages_file, devices_file, countries_file]):
    # Load data
    dates_df = pd.read_csv(dates_file)
    queries_df = pd.read_csv(queries_file)
    pages_df = pd.read_csv(pages_file)
    devices_df = pd.read_csv(devices_file)
    countries_df = pd.read_csv(countries_file)

    # Format %
    for df in [dates_df, queries_df, pages_df]:
        if 'CTR' in df.columns:
            df['CTR'] = df['CTR'].astype(str).str.rstrip('%').astype(float)

    # KPI Metrics
    st.subheader("🔢 Key Metrics Overview")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Clicks", int(dates_df['Clicks'].sum()))
    k2.metric("Total Impressions", int(dates_df['Impressions'].sum()))
    k3.metric("Average CTR", f"{dates_df['CTR'].mean():.1f}%")
    k4.metric("Average Position", f"{dates_df['Position'].mean():.1f}")

    st.markdown("----")

    # Performance Trend
    st.markdown("### 📈 Clicks & Impressions Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates_df['Date'], y=dates_df['Clicks'], name='Clicks', line=dict(color='#00FF00')))
    fig.add_trace(go.Scatter(x=dates_df['Date'], y=dates_df['Impressions'], name='Impressions', line=dict(color='#FFFFFF')))
    fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📘 What does this chart mean?"):
        st.markdown("This shows daily visibility and engagement. Spikes mean strong performance or keyword lifts.")

    # Tabs: Queries, Pages, Devices, Countries
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Queries", "📄 Pages", "📱 Devices", "🌍 Countries"])

    with tab1:
        st.markdown("#### Top Queries by Clicks")
        st.dataframe(queries_df.head(10))
        selected_query = st.selectbox("View query trend", queries_df['Top queries'].head(10))
        filtered = queries_df[queries_df['Top queries'] == selected_query]
        st.markdown(f"**Performance for:** `{selected_query}`")
        st.dataframe(filtered)

    with tab2:
        st.markdown("#### Top Pages by Clicks")
        st.dataframe(pages_df.head(10))
        st.markdown("Hover over each column to sort and discover which URLs drive the most clicks.")

    with tab3:
        st.markdown("#### Device Click Distribution")
        fig = px.pie(devices_df, names='Device', values='Clicks', color_discrete_sequence=['#00FF00', '#FFFFFF', '#333333'])
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.markdown("#### Top Countries by Impressions")
        fig = px.bar(countries_df.sort_values(by='Impressions', ascending=True),
                     x='Impressions', y='Country', orientation='h',
                     color='Impressions', color_continuous_scale=['#333333', '#00FF00'])
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("⬅️ Please upload all 5 required GSC CSV files to begin.")

# Footer
st.markdown("""
    <hr>
    <div style='text-align:center; color:#00FF00; font-family: Poppins'>
        Powered by Zechanah Tokar · <a style='color:#00FF00' href='https://www.zechanahtokar.com' target='_blank'>www.zechanahtokar.com</a>
    </div>
""", unsafe_allow_html=True)
