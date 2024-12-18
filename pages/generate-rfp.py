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

# Create the sidebar
with st.sidebar:
    st.button("Menu", use_container_width=True)
    if st.button("Dashboard", use_container_width=True):
        st.switch_page("pages/dashboard.py")
        st.rerun()
    if st.button("Generate RFPs", use_container_width=True):
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
<img class = "step-icon active" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/upload-rfp.svg"></img>
<p class="step-title">Upload RFP</p>
<section class="connector"></section>
<img class = "step-icon" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/preview-questions.svg"></img>
<p class="step-title">Preview Questions</p>
<section class="connector"></section>
<img class = "step-icon" src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/review-model-response.svg"></img>
<p class="step-title">Review Model Response</p>
</div>
""",
unsafe_allow_html=True
)
_, __ = st.columns([.4, .6])
_.header("RFP Details")
_.write("Please provide the required details for the RFP below, including the account/company name, and the questions sheet. Ensure all fields are accurately completed to proceed.")
rfp_name = __.text_input("RFP Name")
account_name = __.text_input("Account Name")
rfp_sheet = __.file_uploader("Provide RFP Sheet", type=["csv", "xlsx"])    
___, _, __ = __.columns([.4, .2, .4])

if rfp_sheet==None or rfp_name=='' or account_name=='':
    __.button("Preview Question", use_container_width=True,  disabled=True)
else:
    if __.button("Preview Question", use_container_width=True):
        if rfp_sheet.name.endswith(".csv"):
            df = pd.read_csv(rfp_sheet, encoding="utf-8", delimiter=",")
        elif rfp_sheet.name.endswith(".xlsx"):
            df = pd.read_excel(rfp_sheet)
        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid file.")
        else:
            st.session_state.rfp_sheet_df = df.copy(deep=True)
        new_entry = {
            "RFP ID":f"{st.session_state.my_proposals_df.shape[0]+1}",
            "RFP Name":rfp_name,
            "Account Name": account_name,
            "Status":"In Progress",
            "Submission Date":time.strftime("%Y-%m-%d", time.localtime())
        }
        st.session_state.rfp_id = new_entry["RFP ID"]
        st.session_state.my_proposals_df = pd.concat([st.session_state.my_proposals_df, pd.DataFrame([new_entry])])
        st.switch_page("pages/preview-questions.py")

if _.button("Back", use_container_width=True):
    st.switch_page("pages/dashboard.py")
    
