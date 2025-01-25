import streamlit as st
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
