import streamlit as st
import base64
import time
import pandas as pd
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Define CSS styles for the sidebar
st.markdown(
    """
    <style>
    .stSidebar{
    background-color: #E6F0FF;
    z-index:1;
    margin-top: 20px;
    position: fixed;
    }
        .stButton>button {
        # background-color: #B1F0F7; 
        # border: soild;
        color: black;
        padding: 0px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 10px;
        border-radius: 30px;
        cursor: pointer;
        }
         
</style>
    """,
    unsafe_allow_html=True,
)
# ☰ 
# Create the sidebar
with st.sidebar:
    st.button("Menu", use_container_width=True)
    if st.button("Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")
        st.rerun()
    if st.button("Generate RFPs", use_container_width=True, disabled=True):
        pass
st.markdown(
    """
    <style>
    header {
        background-color: #E6F0FF;
        color: #666;
        padding-left: 50px;
        padding-top: 45px;
        padding-bottom: 0px;
        text-align: left;
        position: fixed;
        width: 100%;
        top: 25;
        margin-top: -140px;
        left: 0;
        z-index: 2;
        justify-content: center;
    }
    h3{
    font-size: 30px;
    font-family: 'Roboto', sans-serif;
    }
    </style>
    <header><h3>RFP Accelerator</h3></header>""", 
    unsafe_allow_html=True
)


st.markdown(
"""
<style>
.container {
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
.step-icon {
            width: 40px;
            height: 40px;
            border-radius: 100%;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto 20px;
        }
.step-icon.active {
            background-color: #007bff; /* Example active color */
            color: white;
        }
.step-title {
            font-weight: bold;
        }
        .connector {
            width: 100px;
            height: 2px;
            background-color: #ccc;
            margin: 0px 10px 15px;
        }
</style>
<div class="container">
<img class = "step-icon active" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/checked-widget.svg"></img>
<p class="step-title">Upload RFP</p>
<section class="connector"></section>
<img class = "step-icon active" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/preview-questions.svg"></img>
<p class="step-title">Preview Questions</p>
<section class="connector"></section>
<img class = "step-icon" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/review-model-response.svg"></img>
<p class="step-title">Review Model Response</p>
</div>
""",
unsafe_allow_html=True
)
try:
    st.dataframe(st.session_state.rfp_sheet_df, use_container_width=True, height=350)
except:
    if st.session_state.rfp_sheet_df.read() == b'':
        st.error("Something went wrong please start again.😔")
    _, __, ___ = st.columns([.4, .3, .3])
    if __.button("Restart", key="start_button"):
        st.switch_page("main.py")

col1, col2, col3, col4 = st.columns([1, 1, 4, 4])  # Adjust widths to push buttons to the right

# Use the last column (col4) for the buttons
with col4:
    col4_1, col4_2 = st.columns([2, 4])  # Adjust ratio for smaller gap
    with col4_1:
        
        if st.button("Back", key="back_button_preview"):
            st.switch_page("main.py")
    with col4_2:
        if st.button("Generate Responses", key="generate_rfp_button", use_container_width=True):
            st.session_state.run_model = True
            st.switch_page("pages/model-response.py")
        