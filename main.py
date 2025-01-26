import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import time

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


# if 'slider_min' not in st.session_state:
#     st.session_state.slider_min = time(0, 0, 0)  # Default to 00:00:00
# if 'slider_max' not in st.session_state:
#     st.session_state.slider_max = time(23, 59, 59)  # Default to 23:59:59

# hide_decoration_bar_style = '''
#     <style>
#         header {visibility: hidden;}
#     </style>
# '''
# st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.title('OnlyTrades')

# if "a" not in st.session_state:
#     st.session_state.a = 5

# cols = st.columns(2)
# minimum = cols[0].number_input("Min", 1, 5, key="min")
# maximum = cols[1].number_input("Max", 6, 10, 10, key="max")


# # def update_value():
# #     # Helper function to ensure consistency between widget parameters and value
# #     st.session_state.a = min(st.session_state.a, maximum)
# #     st.session_state.a = max(st.session_state.a, minimum)


# # # Validate the slider value before rendering
# # update_value()
# st.slider("A", minimum, maximum, key="a")

# Create two columns for the selectboxes
col1, col2, col3 = st.columns(3)
# with col1:
#     option = st.selectbox(
#         'Stock',
#         ['A', 'B', 'C', 'D', 'E']
#     )

# with col2:
#     option = st.selectbox(
#         'Period',
#         options=list(range(1, 16))  # List of numbers from 1 to 15

#     )

# # def updateSlider():
# #     st.session_state.slider_max = df['timestamp'].max()
# #     st.session_state.slider_min = df['timestamp'].min()
#     #st.rerun()  # Rerun to update the slider with new max
# # def updateSlider():
# #         if 
# #         st.session_state.slider_max = df['timestamp'].max()
# #         st.session_state.slider_min = df['timestamp'].min()
# # updateSlider()

# # In the first column, create the start period selectbox
# with col3:
#     min_value, max_value = st.slider(
#     'Select the range', 
#     min_value=st.session_state.slider_min, 
#     max_value=st.session_state.slider_max, 
#     value=(st.session_state.slider_min, st.session_state.slider_max),  # Initial range selection
#     format="HH:mm:ss"
# )

# st.write(f"You selected an interval from {min_value} to {max_value}.")

# # Ensure that the end period is greater than or equal to the start period
# if end_period < start_period:
#     st.error("The end period must be greater than or equal to the start period.")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
# df = pd.read_csv(uploaded_file)

if uploaded_file is not None:
    # Load the data from the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f').dt.time
    st.session_state.slider_max = df['timestamp'].max()
    st.session_state.slider_min = df['timestamp'].min()
    # updateSlider()
    # Check if 'bidPrice' exists in the dataframe
    if 'bidPrice' in df.columns:
        # Streamlit title
        st.title("Visualization")

        # Display the dataframe in the app
        # st.write(df)
        # st.session_state.slider_max = df['timestamp'].max()
        # st.session_state.slider_min = df['timestamp'].min()
        # st.rerun()  # Rerun to update the slider with new max

        # with col3:
        #     min_value, max_value = st.slider(
        #     'Select the range', 
        #     min_value=minimum, 
        #     max_value=maximum, 
        #     # value=(10, 40),  # Initial range selection
        # )

        # Create the Plotly figure
        fig1 = go.Figure()

        # Add the bidPrice data as a line plot
        fig1.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['bidPrice'], 
            mode='lines', 
            name='Bid Price',
            # text=df['bidPrice'],  # This is the value shown when hovering
            hovertemplate='Index: %{x}<br>Bid Price: %{y}<extra></extra>',  # Custom tooltip
            hoverinfo='none'
        ))

        # Update layout
        fig1.update_layout(
            title="Bid Price over Index",
            xaxis_title="Index",
            yaxis_title="Bid Price",
            # showspikes=False,  # Removes the vertical spike line on hover
            # showticklabels=False,
            hovermode="x"  # Ensures hovering works well
        )

        # Show the interactive plot in Streamlit
        

    else:
        st.error("The CSV file does not contain a 'bidPrice' column. Please check the file format.")

    # df = pd.read_csv(uploaded_file)
    
    # Check if 'bidPrice' exists in the dataframe
    if 'bidPrice' in df.columns:
        # Streamlit title
        # st.title("Visualization")

        # Display the dataframe in the app
        # st.write(df)

        # Create the Plotly figure
        fig = go.Figure()

        # Add the bidPrice data as a line plot
        fig.add_trace(go.Scatter(
            x=df['timestamp'], 
            y=df['bidVolume'], 
            mode='lines', 
            name='Bid Volume',
            text=df['bidVolume'],  # This is the value shown when hovering
            hovertemplate='Index: %{x}<br>Bid Volume: %{y}<extra></extra>'  # Custom tooltip
        ))

        # Update layout
        fig.update_layout(
            title="Bid Volume over Index",
            xaxis_title="Time",
            yaxis_title="Bid Volume",
            hovermode="x"  # Ensures hovering works well
        )

        # Show the interactive plot in Streamlit
       

    else:
        st.error("The CSV file does not contain a 'bidPrice' column. Please check the file format.")


    c1, c2 = st.columns(2)
    with c1:
            st.plotly_chart(fig1)
    with c2:
        st.plotly_chart(fig)
with col1:
    option = st.selectbox(
        'Stock',
        ['A', 'B', 'C', 'D', 'E']
    )

with col2:
    option = st.selectbox(
        'Period',
        options=list(range(1, 16))  # List of numbers from 1 to 15

    )

# def updateSlider():
#     st.session_state.slider_max = df['timestamp'].max()
#     st.session_state.slider_min = df['timestamp'].min()
    #st.rerun()  # Rerun to update the slider with new max
# def updateSlider():
#         if 
#         st.session_state.slider_max = df['timestamp'].max()
#         st.session_state.slider_min = df['timestamp'].min()
# updateSlider()

# In the first column, create the start period selectbox
with col3:
    print(st.session_state.slider_min)
    min_value, max_value = st.slider(
    'Select the range', 
    min_value=st.session_state.slider_min, 
    max_value=st.session_state.slider_max, 
    step =  time(0, 0, 1),
    value=(st.session_state.slider_min, st.session_state.slider_max),  # Initial range selection
    format="HH:mm:ss"
)

# st.write(f"You selected an interval from {min_value} to {max_value}.")
    
    # 
    # 
    # if 'timestamp' in df.columns:
        # st.session_state.slider_max = df['timestamp'].max()
        # st.session_state.slider_min = df['timestamp'].min()
    #     st.rerun()  # Rerun to update the slider with new max
    # else:
    #     st.error("The 'timestamp' column is missing from the dataframe.")

# if uploaded_file is not None:
#     # Load the data from the uploaded CSV file
#     df = pd.read_csv(uploaded_file)
    
#     # Check if 'bidPrice' exists in the dataframe
#     if 'bidPrice' in df.columns:
#         # Streamlit title
#         st.title("Bid Price Visualization")

#         # Display the dataframe in the app
#         # st.write(df)

#         # Plot the data
#         fig, ax = plt.subplots()
#         ax.plot(df.index, df['bidPrice'], marker='o', color='b', label='Bid Price')
#         ax.set_xlabel('Index')
#         ax.set_ylabel('Bid Price')
#         ax.set_title('Bid Price over Index')
#         ax.legend()

#         # Display the plot in Streamlit
#         st.pyplot(fig)
#     else:
#         st.error("The CSV file does not contain a 'bidPrice' column. Please check the file format.")