import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set Page Configuration
st.set_page_config(
    page_title="Real Estate Market Trends",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 14px;
        color: #7f8c8d;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        border-bottom: 2px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("real_estate_data.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run 'data_generator.py' first.")
        return pd.DataFrame()

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")

if not df.empty:
    # ROI Filter
    regions = st.sidebar.multiselect(
        "Select Region",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

    prop_types = st.sidebar.multiselect(
        "Select Property Type",
        options=df['Property_Type'].unique(),
        default=df['Property_Type'].unique()
    )

    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter Data
    filtered_df = df[
        (df['Region'].isin(regions)) &
        (df['Property_Type'].isin(prop_types)) &
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1]))
    ]
else:
    filtered_df = pd.DataFrame()
    st.sidebar.warning("No data available.")

# Main Title
st.title("🏠 Real Estate Market Trends Dashboard")
st.markdown("Analyze property prices, rental yields, market demand, and economic indicators.")

if not filtered_df.empty:
    # Top-Level Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_price = filtered_df['Price'].mean()
    avg_yield = filtered_df['Rental_Yield_Pct'].mean()
    avg_demand = filtered_df['Demand_Score'].mean()
    total_listings = len(filtered_df)

    with col1:
        st.metric("Avg Property Price", f"${avg_price:,.0f}", delta=None)
    with col2:
        st.metric("Avg Rental Yield", f"{avg_yield:.2f}%", delta=None)
    with col3:
        st.metric("Demand Score (Avg)", f"{avg_demand:.0f}/100", delta=None)
    with col4:
        st.metric("Total Listings", f"{total_listings}", delta=None)

    # Tabs for detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Price & Yield", "📈 Market Dynamics", "🌍 Geographical Insights", "📉 Data Table"])

    with tab1:
        st.subheader("Property Price & Rental Yield Analysis")
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Price Trend Over Time
            price_trend = filtered_df.groupby(pd.Grouper(key='Date', freq='M'))['Price'].mean().reset_index()
            fig_price = px.line(
                price_trend, x='Date', y='Price',
                title='Average Property Price Trend (Monthly)',
                markers=True,
                line_shape='spline',
                color_discrete_sequence=['#0083B8']
            )
            st.plotly_chart(fig_price, use_container_width=True)
            
        with c2:
            # Yield by Property Type
            fig_yield = px.box(
                filtered_df, x='Property_Type', y='Rental_Yield_Pct',
                color='Property_Type',
                title='Rental Yield Distribution by Property Type',
                points="all"
            )
            st.plotly_chart(fig_yield, use_container_width=True)

        # Price vs Yield Scatter
        fig_scatter = px.scatter(
            filtered_df, x='Price', y='Rental_Yield_Pct',
            color='Region',
            size='item_size' if 'item_size' in filtered_df.columns else None, # avoiding error if I don't create size col
            hover_data=['Property_Type', 'Date'],
            title='Price vs. Rental Yield Correlation'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab2:
        st.subheader("Market Demand, Supply & Economic Indicators")
        
        c1, c2 = st.columns(2)
        
        with c1:
            # Demand vs Supply Over Time
            market_trend = filtered_df.groupby(pd.Grouper(key='Date', freq='M')).agg({
                'Demand_Score': 'mean',
                'Supply_Score': 'mean'
            }).reset_index()
            
            fig_market = go.Figure()
            fig_market.add_trace(go.Scatter(x=market_trend['Date'], y=market_trend['Demand_Score'], name='Demand', line=dict(color='green')))
            fig_market.add_trace(go.Scatter(x=market_trend['Date'], y=market_trend['Supply_Score'], name='Supply', line=dict(color='red')))
            fig_market.update_layout(title='Market Demand vs. Supply Trends', xaxis_title='Date', yaxis_title='Score (0-100)')
            st.plotly_chart(fig_market, use_container_width=True)

        with c2:
             # Correlation Matrix Heatmap (Simplified for this view)
            corr_cols = ['Price', 'Rental_Yield_Pct', 'Demand_Score', 'Supply_Score', 'Economic_Indicator']
            corr_matrix = filtered_df[corr_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix, 
                text_auto=True, 
                aspect="auto",
                title='Correlation Matrix: Economic Indicators',
                color_continuous_scale='RdBu_r'
            )
            st.plotly_chart(fig_corr, use_container_width=True)

    with tab3:
        st.subheader("Geographical Hotspots")
        st.info("Interactive Map showing Price distribution across regions.")
        
        # Plotly Mapbox
        # Note: Using open-street-map style to avoid token requirement
        fig_map = px.density_mapbox(
            filtered_df, 
            lat='Latitude', 
            lon='Longitude', 
            z='Price', 
            radius=20,
            center=dict(lat=40.7128, lon=-74.0060), 
            zoom=9,
            mapbox_style="open-street-map",
            title="Property Price Heatmap"
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.subheader("Regional Performance Comparison")
        regional_stats = filtered_df.groupby('Region').agg({
            'Price': 'mean', 
            'Rental_Yield_Pct': 'mean',
            'Demand_Score': 'mean'
        }).reset_index()
        
        fig_bar = px.bar(
            regional_stats, 
            x='Region', 
            y='Price', 
            color='Rental_Yield_Pct',
            title='Average Price by Region (Color represents Rental Yield)',
            text_auto='.2s'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab4:
        st.subheader("Raw Data View")
        st.dataframe(filtered_df.sort_values(by='Date', ascending=False), use_container_width=True)

else:
    st.info("Please adjust filters to view data.")

# Footer
st.markdown("---")
st.markdown("Generated by Agentic AI Coding Assistant")
