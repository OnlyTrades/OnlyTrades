import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pathlib import Path
import time

data = {}
min_times = {}
max_times = {}
    
def load_csv_data(csv_file):
    print(csv_file)
    df = pd.read_csv(csv_file)
    print(df.head())
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f').dt.time
    min_time = df['timestamp'].min()
    max_time = df['timestamp'].max()
    
    return df, min_time, max_time

def load_all_data():
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


def fetch_data(data, min_time, max_time):
    stock = st.session_state.stock
    period = st.session_state.period
    return data[stock][period], min_time[stock][period], max_time[stock][period]
         

st.title('OnlyTrades')

with st.spinner('Loading data...'):
    load_all_data()
    print(data)
st.success("Done!")

stock_col, period_col, time_col = st.columns(3)

# init
st.session_state.stock = "A"
st.session_state.period = 1
st.session_state.display_data = data["A"][1]
st.session_state.min_time = min_times["A"][1]
st.session_state.max_time = max_times["A"][1]
st.session_state.start_time = str(st.session_state.min_time)
st.session_state.end_time = str(st.session_state.max_time)
st.session_state.show_bid_price = True
st.session_state.show_ask_price = True
st.session_state.show_bid_volume = True
st.session_state.show_ask_volume = True

def on_content_change():
    st.session_state.display_data, st.session_state.min_time, st.session_state.max_time = fetch_data(data, min_times, max_times)
    
def on_time_change():
    current_data, _, _ = fetch_data(data, min_times, max_times)
    try:
        start_time = time.strptime(st.session_state.start_time, format='%H:%M:%S.%f')
    except ValueError:
        start_time = st.session_state.min_time
        st.session_state.start_time = str(st.session_state.min_time)
    try:
        end_time = time.strptime(st.session_state.end_time, format='%H:%M:%S.%f')
    except ValueError:
        end_time = st.session_state.max_time
        st.session_state.end_time = str(st.session_state.max_time)
        
    st.session_state.display_data = current_data.loc(
        current_data["timestamp"] >= start_time
        and current_data["timestamp"] <= end_time
    )
    
def on_display_change():
    pass
    
with stock_col:
    stock_option = st.selectbox(
        label='Stock',
        options=['A', 'B', 'C', 'D', 'E'],
        key="stock",
        on_change=on_content_change
    )

with period_col:
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

st.title("Bid Price & Ask Price")
st.line_chart(
    st.session_state.display_data,
    x="timestamp",
    y=["bidPrice", "askPrice"],
)
#fig1 = go.Figure()
#fig1.add_trace(go.Scatter(
#    x=st.session_state.display_data['timestamp'], 
#    y=st.session_state.display_data['bidPrice'], 
#    mode='lines', 
#    name='Bid Price',
#    hovertemplate='Index: %{x}<br>Bid Price: %{y}<extra></extra>', 
#    hoverinfo='none'
#))
## Update layout
#fig1.update_layout(
#    title="Bid Price over Index",
#    xaxis_title="Index",
#    yaxis_title="Bid Price",
#    hovermode="x"
#)
## Show the interactive plot in Streamlit
#    
#fig = go.Figure()
## Add the bidPrice data as a line plot
#fig.add_trace(go.Scatter(
#    x=st.session_state.display_data['timestamp'], 
#    y=st.session_state.display_data['bidVolume'], 
#    mode='lines', 
#    name='Bid Volume',
#    text=st.session_state.display_data['bidVolume'],  # This is the value shown when hovering
#    hovertemplate='Index: %{x}<br>Bid Volume: %{y}<extra></extra>'  # Custom tooltip
#))
## Update layout
#fig.update_layout(
#    title="Bid Volume over Index",
#    xaxis_title="Time",
#    yaxis_title="Bid Volume",
#    hovermode="x"  # Ensures hovering works well
#)
## Show the interactive plot in Streamlit
   
    
#c1, c2 = st.columns(2)
#with c1:
#        st.plotly_chart(fig1)
#with c2:
#    st.plotly_chart(fig)
    