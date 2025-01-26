from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path
    
def load_csv_data(csv_file):
    df = pd.read_csv(csv_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f')
    min_time = df['timestamp'].min()
    max_time = df['timestamp'].max()
    
    return df, min_time, max_time

@st.cache_data
def load_all_data():
    data = {}
    min_times = {}
    max_times = {}
    dataset_path = "./TrainingData"
    stocks = ["A", "B", "C", "D", "E"]
    periods = [idx for idx in range(1, 16)]
    for stock in stocks:
        data[stock] = {}
        min_times[stock] = {}
        max_times[stock] = {}
        
        for period in periods:
            csv_files = (
                Path(dataset_path)
                .joinpath(f"Period{period}")
                .joinpath(stock)
            )
            for csv_file in csv_files.iterdir():
                if str(csv_file.stem)!=f"market_data_{stock}_0":
                    continue
                data[stock][period], min_times[stock][period], max_times[stock][period] = load_csv_data(csv_file)
    
    return data, min_times, max_times


def fetch_data(data, min_times, max_times):
    stock = st.session_state.stock
    period = st.session_state.period
    return data[stock][period], min_times[stock][period], max_times[stock][period]
         
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        body {
            background-color: #241E3A;
            color: #C84E11;
            margin-toop: 0;
            padding-top: 0;
        }

        # /* Ensure the main content stretches across the full width /
        # .stApp {
        #     width: 100% !important;
        # }

        / Ensure background of the entire Streamlit app is styled /
        .stApp {
            background-color: #241E3A;
        }

        / Apply text color to Markdown, text, and other Streamlit text components /
        .stMarkdown, .stText, .stTextInput, .stButton, .stSlider, .stRadio, .stCheckbox, .stFileUploader, .stSelectbox, .stMultiselect {
            color: #C84E11 !important;
        }

        / Update the color for all headers /
        h1, h2, h3, h4, h5, h6, p {
            color: #C84E11 !important;
        }

        / For Streamlit buttons, widgets, sliders, checkboxes, etc. /
        .stButton>button, .stSlider>div, .stRadio>div, .stCheckbox>div, .stSelectbox>div, .stMultiselect>div {
            color: #C84E11 !important;
        }

        / Targeting links inside Streamlit for consistent color */
        .css-1v0mbdj a, .css-1v0mbdj a:visited {
            color: #C84E11 !important;
        }

        .centered-text {
            font-size: 50px;
            color: #C84E11;
            text-align: center;
        }
        .st-emotion-cache-yw8pof {
            padding-top: 0;
        }
    </style>
    <hr style='margin: 0; border: 20px solid #C84E11; width: 100%;' />
    <div class="centered-text">OnlyTrades</div>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

data, min_times, max_times = load_all_data()

stock_col, time_col = st.columns(2)

# init
if st.session_state.get("stock") is None:
    st.session_state.stock = "A"
if st.session_state.get("period") is None:
    st.session_state.period = 1
stock = st.session_state.stock
period = st.session_state.period
st.session_state.display_data = data[stock][period]
st.session_state.min_time = min_times[stock][period]
st.session_state.max_time = max_times[stock][period]
if st.session_state.get("start_time") is None:
    st.session_state.start_time = st.session_state.min_time.strftime(format='%H:%M:%S.%f')
if st.session_state.get("end_time") is None:
    st.session_state.end_time = st.session_state.max_time.strftime(format='%H:%M:%S.%f')
if st.session_state.get("displayed_price") is None:
    st.session_state.displayed_price = ["bidPrice", "askPrice"]
if st.session_state.get("displayed_volume") is None:
    st.session_state.displayed_volume = ["bidVolume", "askVolume"]

def on_content_change():
    st.session_state.display_data, st.session_state.min_time, st.session_state.max_time = fetch_data(data, min_times, max_times)
    st.session_state.start_time = st.session_state.min_time.strftime(format='%H:%M:%S.%f')
    st.session_state.end_time = st.session_state.max_time.strftime(format='%H:%M:%S.%f')
    
def on_time_change():
    current_data, _, _ = fetch_data(data, min_times, max_times)
    try:
        start_time = datetime.strptime(st.session_state.start_time, '%H:%M:%S.%f')
    except ValueError:
        start_time = st.session_state.min_time
        st.session_state.start_time = str(st.session_state.min_time)
    try:
        end_time = datetime.strptime(st.session_state.end_time, '%H:%M:%S.%f')
    except ValueError:
        end_time = st.session_state.max_time
        st.session_state.end_time = str(st.session_state.max_time)
        
    st.session_state.display_data = current_data.loc(
        current_data["timestamp"] >= start_time
        and current_data["timestamp"] <= end_time
    )
    
    
def on_display_change():
    st.session_state.displayed_price = []
    st.session_state.displayed_volume = []
    if st.session_state.show_bid_price:
        st.session_state.displayed_price.append("bidPrice")
    if st.session_state.show_ask_price:
        st.session_state.displayed_price.append("askPrice")
    if st.session_state.show_bid_volume:
        st.session_state.displayed_volume.append("bidVolume")
    if st.session_state.show_ask_volume:
        st.session_state.displayed_volume.append("askVolume")
    
with stock_col:
    stock_option = st.selectbox(
        label='Stock',
        options=['A', 'B', 'C', 'D', 'E'],
        key="stock",
        on_change=on_content_change
    )
    period_option = st.selectbox(
        label='Period',
        options=list(range(1, 16)),  # List of numbers from 1 to 15
        key="period",
        on_change=on_content_change
    )

with time_col:
    _, min_time, max_time = fetch_data(data, min_times, max_times)
    
    start_time = st.text_input(
        label="Start time",
        key="start_time"
    )
    end_time = st.text_input(
        label="End time",
        key="end_time"
    )
    submit_botton = st.button(
        label="Confirm",
        on_click=on_time_change

    )

st.subheader("Bid Price & Ask Price")
st.checkbox("Bid Price", key="show_bid_price", value=True, on_change=on_display_change)
st.checkbox("Ask Price", key="show_ask_price", value=True, on_change=on_display_change)
price_figure = go.Figure()
# Add traces for each line
for column in st.session_state.displayed_price:
    price_figure.add_trace(
        go.Scatter(
            x=st.session_state.display_data["timestamp"], 
            y=st.session_state.display_data[column], 
            mode='lines', 
            name=column
        )
    )
# Customize layout
price_figure.update_layout(
    title="Price Chart",
    xaxis_title="Time",
    yaxis_title="Price",
    legend_title="Lines",
    template="plotly_white",
    hovermode="x",
    xaxis=dict(
        tickformat='%H:%M:%S.%f',
        dtick=600000
    )
)
# Display the chart in Streamlit
st.plotly_chart(price_figure)

st.subheader("Bid Volume & Ask Volume")
st.checkbox("Bid Volume", key="show_bid_volume", value=True, on_change=on_display_change)
st.checkbox("Ask Volume", key="show_ask_volume", value=True, on_change=on_display_change)
volume_figure = go.Figure()
# Add traces for each line
for column in st.session_state.displayed_volume:
    volume_figure.add_trace(
        go.Scatter(
            x=st.session_state.display_data["timestamp"], 
            y=st.session_state.display_data[column], 
            mode='lines', 
            name=column
        )
    )
    # Customize layout
volume_figure.update_layout(
    title="Price Chart",
    xaxis_title="Time",
    yaxis_title="Volume",
    legend_title="Lines",
    template="plotly_white",
    hovermode="x",
    xaxis=dict(
        tickformat='%H:%M:%S.%f',
        dtick=600000
    )
)
# Display the chart in Streamlit
st.plotly_chart(volume_figure)

