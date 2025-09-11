import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Uber Data Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 30px;
        background: linear-gradient(90deg, #FF6B35, #F7931E, #FFD23F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .page-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2E86AB;
        margin-bottom: 20px;
        border-bottom: 3px solid #2E86AB;
        padding-bottom: 10px;
        background: linear-gradient(90deg, #2E86AB, #A23B72, #F18F01);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-container {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 8px 25px 0 rgba(255, 107, 53, 0.4);
        backdrop-filter: blur(4px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        transform: translateY(0px);
        transition: all 0.3s ease;
    }
    .kpi-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px 0 rgba(255, 107, 53, 0.6);
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .kpi-label {
        font-size: 1.1rem;
        color: white;
        margin-top: 8px;
        font-weight: 500;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .chart-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"C:\Users\dxgam\Streamlit_App\cleaned_uber.csv")
        # Convert DateTime column to datetime
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        # Extract additional time features if not present
        if 'Year' not in df.columns:
            df['Year'] = df['DateTime'].dt.year
        if 'Month' not in df.columns:
            df['Month'] = df['DateTime'].dt.month
        return df
    except FileNotFoundError:
        st.error("❌ Dataset file not found. Please ensure 'cleaned_uber.csv' exists in the specified directory.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Load the data
df = load_data()

if df is not None:
    # Main title
    st.markdown('<h1 class="main-header">Uber Data Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 **Filters**")
    st.sidebar.markdown("---")
    
    # Year filter
    years = sorted(df['Year'].unique())
    selected_years = st.sidebar.multiselect(
        "📅 **Select Year(s):**",
        years,
        default=years,
        help="Choose one or more years to analyze"
    )
    
    # Month filter
    months = sorted(df['Month'].unique())
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    
    selected_months = st.sidebar.multiselect(
        "📊 **Select Month(s):**",
        months,
        format_func=lambda x: month_names.get(x, x),
        default=months,
        help="Choose one or more months to analyze"
    )
    
    # Filter data based on selections
    if selected_years and selected_months:
        filtered_df = df[
            (df['Year'].isin(selected_years)) & 
            (df['Month'].isin(selected_months))
        ]
    else:
        filtered_df = pd.DataFrame()  # Empty dataframe if no filters selected
    
    # Display data info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 **Data Summary**")
    if not filtered_df.empty:
        st.sidebar.info(f"📈 **Filtered Records:** {len(filtered_df):,}")
        st.sidebar.info(f"📅 **Date Range:** {filtered_df['DateTime'].min().strftime('%Y-%m-%d')} to {filtered_df['DateTime'].max().strftime('%Y-%m-%d')}")
    else:
        st.sidebar.warning("⚠️ No data available for selected filters")
    
    # Page navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🧭 **Navigation**")
    page = st.sidebar.selectbox(
        "**Select Dashboard Page:**",
        ["📈 Overview", "🚕 Trip Experience", "💰 Revenue"],
        help="Navigate between different dashboard views"
    )
    
    # Check if filtered data is available
    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your filter selections.")
        st.stop()
    
    # Page 1: Overview
    if page == "📈 Overview":
        st.markdown('<div class="page-header">Overview Dashboard</div>', unsafe_allow_html=True)
        
        # KPIs Section
        st.markdown("#### 🎯 **Key Performance Indicators**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_trips = len(filtered_df)
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{total_trips:,}</div>
                <div class="kpi-label">🚗 Total Trips</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_value = filtered_df['Booking Value'].fillna(0).sum()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">${total_value:,.0f}</div>
                <div class="kpi-label">💰 Total Booking Value</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            unique_customers = filtered_df['Customer ID'].nunique()
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-value">{unique_customers:,}</div>
                <div class="kpi-label">👥 Unique Customers</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Graphs Section
        st.markdown("#### 📊 **Performance Analytics**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Completed Trips by Status")
            status_counts = filtered_df['Booking Status'].value_counts()
            
            # Create brighter color palette
            colors = ['#FF6B35', '#F7931E', '#FFD23F', '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83']
            
            fig_status = px.bar(
                x=status_counts.index, 
                y=status_counts.values,
                title="Number of Trips by Booking Status",
                color=status_counts.index,
                color_discrete_sequence=colors
            )
            fig_status.update_layout(
                xaxis_title="Booking Status",
                yaxis_title="Number of Trips",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            st.markdown("##### ⭐ Customer Ratings Distribution")
            customer_ratings = filtered_df['Customer Rating'].dropna()
            customer_ratings = customer_ratings[customer_ratings > 0]  # Remove -1 values
            
            if len(customer_ratings) > 0:
                fig_cust_rating = px.histogram(
                    customer_ratings,
                    nbins=20,
                    title="Customer Ratings Distribution",
                    color_discrete_sequence=["#FF6B35"]
                )
                fig_cust_rating.update_layout(
                    xaxis_title="Customer Rating",
                    yaxis_title="Frequency",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig_cust_rating, use_container_width=True)
            else:
                st.info("ℹ️ No valid customer ratings available for the selected period.")
        
        # Driver Ratings (full width)
        st.markdown("##### 🚗 Driver Ratings Distribution")
        driver_ratings = filtered_df['Driver Ratings'].dropna()
        driver_ratings = driver_ratings[driver_ratings > 0]  # Remove -1 values
        
        if len(driver_ratings) > 0:
            fig_driver_rating = px.histogram(
                driver_ratings,
                nbins=20,
                title="Driver Ratings Distribution",
                color_discrete_sequence=["#2E86AB"]
            )
            fig_driver_rating.update_layout(
                xaxis_title="Driver Rating",
                yaxis_title="Frequency",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_driver_rating, use_container_width=True)
        else:
            st.info("ℹ️ No valid driver ratings available for the selected period.")
    
    # Page 2: Trip Experience
    elif page == "🚕 Trip Experience":
        st.markdown('<div class="page-header">🚕 Trip Experience Dashboard</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Booking Status Distribution")
            status_counts = filtered_df['Booking Status'].value_counts()
            
            fig_pie = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Booking Status Distribution",
                color_discrete_sequence=['#FF6B35', '#F7931E', '#FFD23F', '#2E86AB', '#A23B72', '#F18F01']
            )
            fig_pie.update_layout(
                font=dict(size=12),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("##### ⏱️ Average VTAT by Vehicle Type")
            vtat_by_vehicle = filtered_df.groupby('Vehicle Type')['Avg VTAT'].mean().dropna()
            if len(vtat_by_vehicle) > 0:
                fig_vtat = px.bar(
                    x=vtat_by_vehicle.index,
                    y=vtat_by_vehicle.values,
                    title="Average VTAT by Vehicle Type",
                    color=vtat_by_vehicle.values,
                    color_continuous_scale=[[0, '#FFD23F'], [0.5, '#F7931E'], [1, '#FF6B35']]
                )
                fig_vtat.update_layout(
                    xaxis_title="Vehicle Type",
                    yaxis_title="Average VTAT (minutes)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig_vtat, use_container_width=True)
            else:
                st.info("ℹ️ No VTAT data available for the selected period.")
        
        # CTAT by Vehicle Type (full width)
        st.markdown("##### 🕐 Average CTAT by Vehicle Type")
        ctat_by_vehicle = filtered_df.groupby('Vehicle Type')['Avg CTAT'].mean().dropna()
        if len(ctat_by_vehicle) > 0:
            fig_ctat = px.bar(
                x=ctat_by_vehicle.index,
                y=ctat_by_vehicle.values,
                title="Average CTAT by Vehicle Type",
                color=ctat_by_vehicle.values,
                color_continuous_scale=[[0, '#2E86AB'], [0.5, '#A23B72'], [1, '#F18F01']]
            )
            fig_ctat.update_layout(
                xaxis_title="Vehicle Type",
                yaxis_title="Average CTAT (minutes)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_ctat, use_container_width=True)
        else:
            st.info("ℹ️ No CTAT data available for the selected period.")
    
    # Page 3: Revenue
    elif page == "💰 Revenue":
        st.markdown('<div class="page-header">Revenue Dashboard</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💵 Booking Value by Vehicle Type")
            revenue_by_vehicle = filtered_df.groupby('Vehicle Type')['Booking Value'].sum().dropna()
            if len(revenue_by_vehicle) > 0:
                # Create distinct colors for each vehicle type
                distinct_colors = ['#FF6B35', '#F7931E', '#FFD23F', '#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#592E83']
                vehicle_colors = distinct_colors[:len(revenue_by_vehicle)]
                
                fig_revenue_bar = px.bar(
                    x=revenue_by_vehicle.index,
                    y=revenue_by_vehicle.values,
                    title="Total Booking Value by Vehicle Type",
                    color=revenue_by_vehicle.index,
                    color_discrete_sequence=vehicle_colors
                )
                fig_revenue_bar.update_layout(
                    xaxis_title="Vehicle Type",
                    yaxis_title="Total Booking Value (₹)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig_revenue_bar, use_container_width=True)
            else:
                st.info("ℹ️ No booking value data available for the selected period.")
        
        with col2:
            st.markdown("##### 🥧 Revenue Share by Vehicle Type")
            if len(revenue_by_vehicle) > 0:
                fig_revenue_pie = px.pie(
                    values=revenue_by_vehicle.values,
                    names=revenue_by_vehicle.index,
                    title="Revenue Share by Vehicle Type",
                    color_discrete_sequence=['#FF6B35', '#F7931E', '#FFD23F', '#2E86AB', '#A23B72', '#F18F01']
                )
                fig_revenue_pie.update_layout(
                    font=dict(size=12),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_revenue_pie, use_container_width=True)
            else:
                st.info("ℹ️ No booking value data available for the selected period.")
        
        # Revenue over time (full width)
        st.markdown("##### 📈 Revenue Trend Over Time")
        if 'Booking Value' in filtered_df.columns and filtered_df['Booking Value'].notna().sum() > 0:
            # Group by date and sum booking values
            daily_revenue = filtered_df.groupby(filtered_df['DateTime'].dt.date)['Booking Value'].sum().reset_index()
            daily_revenue.columns = ['Date', 'Revenue']
            
            fig_revenue_line = px.line(
                daily_revenue,
                x='Date',
                y='Revenue',
                title="Daily Revenue Trend",
                markers=True,
                color_discrete_sequence=["#F18F01"]
            )
            fig_revenue_line.update_layout(
                xaxis_title="Date",
                yaxis_title="Revenue (₹)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_revenue_line, use_container_width=True)
        else:
            st.info("ℹ️ No booking value data available for the selected period.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px; margin-top: 30px;'>
        <p>📊 <strong>Uber Data Analytics Dashboard</strong> | Built with ❤️ using Streamlit</p>
        <p>🔍 Comprehensive analysis of ride booking data with interactive visualizations</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Unable to load the dataset. Please ensure 'cleaned_uber.csv' exists in the specified directory and is accessible.")
    st.markdown("""
    ### 📋 Expected file location:
    `C:\\Users\\dxgam\\Streamlit_App\\cleaned_uber.csv`
    
    ### 📊 Expected columns:
    - Booking ID, Booking Status, Customer ID, Vehicle Type
    - Pickup Location, Drop Location, Avg VTAT, Avg CTAT
    - Booking Value, Ride Distance, Driver Ratings, Customer Rating
    - Payment Method, DateTime, Year, Month, DayOfWeek, IsWeekend, Reason
    """)
