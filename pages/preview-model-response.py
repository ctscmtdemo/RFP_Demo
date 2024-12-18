import streamlit as st
import base64
import time
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

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
<img class = "step-icon active" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/checked-widget.svg"></img>
<p class="step-title">Preview Questions</p>
<section class="connector"></section>
<img class = "step-icon active" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/review-model-response.svg"></img>
<p class="step-title">Review Model Response</p>
</div>
""",
unsafe_allow_html=True
)

st.dataframe(
    pd.DataFrame(st.session_state.generated_rfps[st.session_state.selected_rfp_id]),
    use_container_width=True,
    height=400
)
csv = pd.DataFrame(st.session_state.generated_rfps[st.session_state.selected_rfp_id]).to_csv()
col1, col2, col3 = st.columns([0.1, 7, 2])  # Adjust proportions to push the button to the right
with col3:
    if st.download_button(
        label="Export to CSV",
        data=csv,
        file_name="generated_responses.csv",
        mime="text/csv",
        use_container_width=True,
        on_click=None
    ):
        with st.spinner("Downloading..."):
            time.sleep(10)
        st.success("Download Success")
    
    