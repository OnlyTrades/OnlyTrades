import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.title('OnlyTrades')


# Create two columns for the selectboxes
col1, col2, col3 = st.columns(3)
with col1:
    option = st.selectbox(
        'Stock',
        ['A', 'B', 'C', 'D', 'E']
    )

# In the first column, create the start period selectbox
with col2:
    start_period = st.selectbox('Start Period:', list(range(1, 16)))

# In the second column, create the end period selectbox
with col3:
    end_period = st.selectbox('End Period:', list(range(1, 16)))

# Ensure that the end period is greater than or equal to the start period
if end_period < start_period:
    st.error("The end period must be greater than or equal to the start period.")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
# df = pd.read_csv(uploaded_file)

if uploaded_file is not None:
    # Load the data from the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Check if 'bidPrice' exists in the dataframe
    if 'bidPrice' in df.columns:
        # Streamlit title
        st.title("Visualization")

        # Display the dataframe in the app
        # st.write(df)

        # Create the Plotly figure
        fig1 = go.Figure()

        # Add the bidPrice data as a line plot
        fig1.add_trace(go.Scatter(
            x=df['timestamp'].str[:8], 
            y=df['bidPrice'], 
            mode='lines', 
            name='Bid Price',
            text=df['bidPrice'],  # This is the value shown when hovering
            hovertemplate='Index: %{x}<br>Bid Price: %{y}<extra></extra>'  # Custom tooltip
        ))
        # tick_positions = np.linspace(0, len(df) - 1, 5).astype(int)
        # ticktext = [df['timestamp'].str[:8].iloc[i] for i in tick_positions]

        # Update layout
        fig1.update_layout(
            title="Bid Price over Index",
            xaxis_title="Index",
            yaxis_title="Bid Price",
            hovermode="x",  # Ensures hovering works well
            # xaxis=dict(
            #     tickvals=tick_positions,  # Positions of the ticks
            #     ticktext=ticktext
            # )
        )

        # Show the interactive plot in Streamlit
        

    else:
        st.error("The CSV file does not contain a 'bidPrice' column. Please check the file format.")

    # df = pd.read_csv(uploaded_file)
    
    # Check if 'bidPrice' exists in the dataframe
    # if 'bidPrice' in df.columns:
    #     # Streamlit title
    #     # st.title("Visualization")

    #     # Display the dataframe in the app
    #     # st.write(df)

    #     # Create the Plotly figure
    #     fig = go.Figure()

    #     # Add the bidPrice data as a line plot
    #     fig.add_trace(go.Scatter(
    #         x=df.index, 
    #         y=df['bidVolume'], 
    #         mode='lines', 
    #         name='Bid Volume',
    #         text=df['bidVolume'],  # This is the value shown when hovering
    #         hovertemplate='Index: %{x}<br>Bid Volume: %{y}<extra></extra>'  # Custom tooltip
    #     ))

    #     # Update layout
    #     fig.update_layout(
    #         title="Bid Volume over Index",
    #         xaxis_title="Index",
    #         yaxis_title="Bid Volume",
    #         hovermode="closest"  # Ensures hovering works well
    #     )

    #     # Show the interactive plot in Streamlit
       

    # else:
    #     st.error("The CSV file does not contain a 'bidPrice' column. Please check the file format.")


    # c1, c2 = st.columns(2)
    # with c1:
    st.plotly_chart(fig1)
    # with c2:
    #     st.plotly_chart(fig)

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