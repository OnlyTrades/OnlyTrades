import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta

# Helper Functions
def time_to_seconds(t: time) -> float:
    """Convert a datetime.time object to total seconds since midnight."""
    return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1_000_000

def seconds_to_time(seconds: float) -> time:
    """Convert total seconds since midnight to a datetime.time object."""
    return (datetime.min + timedelta(seconds=seconds)).time()

# Initialize session state for slider_min and slider_max if not already done
if 'slider_min_seconds' not in st.session_state:
    st.session_state.slider_min_seconds = 0.0  # 00:00:00.000
if 'slider_max_seconds' not in st.session_state:
    st.session_state.slider_max_seconds = 86399.999  # 23:59:59.999

st.title('OnlyTrades')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load the data from the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        
        # Check if 'timestamp' column exists
        if 'timestamp' in df.columns:
            try:
                # Attempt to parse 'timestamp' with fractional seconds
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f').dt.time
            except ValueError:
                st.warning("Failed to parse 'timestamp' with format '%H:%M:%S.%f'. Attempting to parse without fractional seconds.")
                try:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S').dt.time
                except ValueError as ve:
                    st.error(f"Unable to parse 'timestamp' column: {ve}")
                    st.stop()
            
            # Convert to total seconds and update session state
            df['timestamp_seconds'] = df['timestamp'].apply(time_to_seconds)
            st.session_state.slider_min_seconds = df['timestamp_seconds'].min()
            st.session_state.slider_max_seconds = df['timestamp_seconds'].max()
            
            st.success("CSV file loaded and 'timestamp' parsed successfully!")
        else:
            st.error("The uploaded CSV does not contain a 'timestamp' column.")
            st.stop()
        
        # Check if 'bidPrice' exists in the dataframe
        if 'bidPrice' in df.columns:
            st.title("Visualization")
            
            # Create three columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                stock_option = st.selectbox(
                    'Stock',
                    ['A', 'B', 'C', 'D', 'E']
                )
            
            with col2:
                period_option = st.selectbox(
                    'Period',
                    options=list(range(1, 16))  # List of numbers from 1 to 15
                )
        else:
            st.error("The uploaded CSV does not contain a 'bidPrice' column.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")

# Render the slider only if 'bidPrice' exists and data is loaded
if uploaded_file is not None and 'bidPrice' in df.columns:
    with col3:
        min_seconds = st.session_state.slider_min_seconds
        max_seconds = st.session_state.slider_max_seconds
        
        # Define the step size for the slider (e.g., 0.1 seconds for 100ms precision)
        step_size = 0.1  # Adjust as needed
        
        selected_min, selected_max = st.slider(
            'Select the time range', 
            min_value=min_seconds, 
            max_value=max_seconds, 
            value=(min_seconds, max_seconds),
            step=step_size,
            format="%.3f"  # Display up to milliseconds
        )
        
        # Convert selected seconds back to time format
        selected_min_time = seconds_to_time(selected_min)
        selected_max_time = seconds_to_time(selected_max)
        
        st.write(f"You selected a time range from {selected_min_time} to {selected_max_time}.")

# (Optional) Display the DataFrame for verification
if uploaded_file is not None and 'timestamp_seconds' in df.columns:
    st.write("DataFrame Preview:", df.head())