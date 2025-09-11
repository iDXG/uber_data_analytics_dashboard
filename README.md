# 🚗 Uber Data Analytics Dashboard

A comprehensive Streamlit dashboard for analyzing Uber ride booking data with interactive visualizations and insights.

## 📊 Features

### 📈 Overview Dashboard
- **Key Performance Indicators (KPIs)**
  - Total number of trips
  - Total booking value
  - Unique customers count
- **Interactive Charts**
  - Booking status distribution
  - Customer ratings histogram
  - Driver ratings histogram

### 🚕 Trip Experience Dashboard
- Booking status pie chart
- Average VTAT (Vehicle Turn Around Time) by vehicle type
- Average CTAT (Customer Turn Around Time) by vehicle type

### 💰 Revenue Dashboard
- Booking value by vehicle type (bar chart)
- Revenue share by vehicle type (pie chart)
- Daily revenue trend over time

## 🔍 Interactive Filters
- **Year Filter**: Select specific years for analysis
- **Month Filter**: Filter data by months
- Real-time data filtering across all visualizations

## 🛠️ Technologies Used
- **Streamlit**: Web framework for the dashboard
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **Matplotlib & Seaborn**: Additional plotting capabilities

## 🚀 Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run app.py
```

## 📁 Project Structure
```
Streamlit_App/
├── app.py                 # Main dashboard application
├── cleaned_uber.csv       # Dataset file
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 📊 Dataset
The dashboard uses Uber ride booking data with the following columns:
- Booking ID, Booking Status, Customer ID
- Vehicle Type, Pickup/Drop Locations
- VTAT, CTAT, Booking Value, Ride Distance
- Driver/Customer Ratings, Payment Method
- DateTime, Year, Month, Day of Week

## 🎨 Design Features
- **Modern UI**: Clean, professional design with vibrant colors
- **Responsive Layout**: Works on different screen sizes
- **Interactive Elements**: Hover effects and smooth transitions
- **Consistent Color Scheme**: Coordinated colors across all visualizations

## 🌐 Live Demo
https://uberdataanalyticsdashboard-am9eksnt3rpnwzhdzf6ty7.streamlit.app/)
