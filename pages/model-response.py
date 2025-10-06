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

def generate_responses(df, delay=1.0):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key= st.secrets["GEMINI_API_KEY"] 
    )
    # if "Question" not in df.columns:
    #     st.error("The uploaded file must contain 'Question' scolumn.")
    #     return None

    responses = []
    start_time = time.time()  # Start timing the processing
    for question in df.iloc[:,0]: #df["Question"]:
        try:
            print(f"Processing question: {question}")
            messages = [{"role": "user", "content": f"Answer the following question in one line. Question : {question}"}]
            response = llm.invoke(messages)
            generated_content = response.content  
            responses.append(generated_content)
            time.sleep(delay)

        except Exception as e:
            print(e)
            responses.append(f"Error: {e}")
    end_time = time.time()  # End timing
    df["Model Response"] = responses
    processing_time = end_time - start_time
    return df, processing_time

df = st.session_state.rfp_sheet_df

if df.shape[0] > 100:
    st.error("The file contains too many questions. Please limit it to 100 entries.")
# elif "Question" not in df.columns:
#     st.error("The file must contain 'Question' column.")
else:
    # Generate responses
    if st.session_state.run_model:
        with st.spinner("Generating responses..."):
            st.session_state.df_with_answers, st.session_state.processing_time = generate_responses(df)
        if st.session_state.df_with_answers is not None:
            st.session_state.df_with_answers[" "] = ["📝" for _ in range(len(df))]  # Add pen with paper icon 
            st.session_state.generated_responses_count += st.session_state.df_with_answers.shape[0]
            st.session_state.total_generated_rfps += 1
            st.session_state.my_proposals_df.loc[st.session_state.my_proposals_df["RFP ID"] == st.session_state.rfp_id, 'Status'] = 'Success'
            # st.session_state.my_proposals_df.loc[st.session_state.my_proposals_df["RFP ID"] == st.session_state.rfp_id, ' '] = 'pages/model-response.py'
            st.session_state.average_response_time = (st.session_state.average_response_time+st.session_state.processing_time)/2
            st.session_state.generated_rfps[st.session_state.rfp_id] = st.session_state.df_with_answers.to_dict()
            st.session_state.run_model = False
            st.session_state.csv = st.session_state.df_with_answers.to_csv(index=False).encode("utf-8")
    
    st.dataframe(
            st.session_state.df_with_answers,
            use_container_width=True,
            # width=2000,  # Adjust width to fill the screen
            height=400,  # Adjust height as needed
            )
    col1, col2, col3 = st.columns([0.1, 7, 2])  # Adjust proportions to push the button to the right
    with col3:
        st.download_button(
            label="Export to CSV",
            data=st.session_state.csv,
            file_name="generated_responses.csv",
            mime="text/csv",
            use_container_width=True,
            on_click=None
        )
            # with st.spinner("Downloading..."):
            #     time.sleep(10)
            # st.success("Download Success")
    
    