import base64
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#     def set_png_as_page_bg(png_file):
#         bin_str = get_base64_of_bin_file(png_file)
#         #  background-size: contain;
#         page_bg_img = '''
#         <style>
#         .stApp {
#         background-image: url("data:image/png;base64,%s");
#         background-size: cover;
#         background-position: top;
#        /* margin-top: -40px;*/
#         background-repeat: no-repeat;
#         }
#         </style>
#         ''' % bin_str

#         st.markdown(page_bg_img, unsafe_allow_html=True)
#         return


#     set_png_as_page_bg('images/bg_org.png')

def start_page():
    # Header Section;
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
            margin-top: -120px;
            left: 0;
            # z-index: 300;
            # justify-content: center;
            
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
        .RFP-accelerator-text{
        # width: 820px;
        margin-top: -100px;
        # padding-top: 100px;
        text-align: center;
        font-size: 55px;
        font-style: normal;
        font-weight: 400;
        # line-height: 65px;
        position: flex;
        letter-spacing: -2px;
        background: linear-gradient(90deg, #267DF7 0%, #728AEC 38%, #B580D1 67%, #E4576D 93%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: Google Sans;
        # padding-left: 30px;
        }

        .icon-container {
            display: inline-block;
            margin-top: -100px;
            # margin-right: 100px;
            padding-left: 550px;
            # padding-top: -10px;
            padding-bottom: 35px;
            text-align: center;
            width: 820px;
            font-size: 30px;
            position: relative;
        }

        .star-icon {
            margin-top: -50px;
            margin-right: 30px;
            width: 25px;
            height: 25px;
        }
        h5 {
        align-items: center;
        text-align: center;
        # width: 90px;
        # padding-left: -300px;
        margin-left: -20px;
        color: grey;
        }
        </style>
        <span class="icon-container">
                <img src="https://rfp-frontend-newuiuxdemo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/rfp-text-icon.svg" class="star-icon">
        </span>
        <div style="align-items: center; justify-content: center; text-align: center; margin-top: -100px;">
        <h1 class="RFP-accelerator-text">
            RFP Accelerator, &nbsp<br>
            Reimagined with AI
        </h1>
        </div>
        <h5>
        Accelerate RFP responses and propel business growth <br> with GenAI, the intelligent RFP automation solution <br> powered by Vertex AI and Gemini.
        </h5>
        """,
        unsafe_allow_html=True
    )
    _, __, ___ = st.columns([.45, .4, .25])
    __.markdown(
        """
        <style>
        .stButton>button {
        background-color: #007bff; 
        border: soild;
        color: white;
        padding: 0px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 10px;
        border-radius: 30px;
        cursor: pointer;
        }
    
        .stButton>button::before{
            content: url("data:image/png;base64,%s"); /* The icon */
            # margin-right: 10px; /* Space between icon and text */
        }
        </style>
        """ % get_base64_of_bin_file('images/start.png'),
        unsafe_allow_html=True,
    )

    if __.button("", key="start_button"):
        st.switch_page("pages/dashboard.py")


    
    _, col1, col2, col3, __ = st.columns([.07, .4, .4, .4, .1])

    with col1.container(border=True):
        st.image("images/speed_up.png")  # Replace with your icon path
        st.write("**Speed up your RFP responses and win more business with Google Gemini Pro**")

    with col2.container(border=True):
        st.image("images/run_icon.png")  # Replace with your icon path
        st.write("**Expert-level accuracy and consistent high quality in every response**")

    with col3.container(border=True):
        st.image("images/aa.png")  # Replace with your icon path
        st.write("**Effortlessly streamline and accelerate your workflow with AI-powered tools**")

    # Footer Section
    st.markdown("""
        <style>
        footer {
            background-color: #F5FFFA;
            color: #666;
            padding: 18px;
            text-align: left;
            border-top: solid;
            position: fixed;
            bottom: 0;
            width: 100%;
            height: 20px;
            left: 0;
            z-index: 100;
            justify-content: Left;
            font-family: 'Roboto', sans-serif;
            padding-bottom: 50px;
            padding-top: 2px;
            # margin-top: -10px;
        }
                .footh3{
                font-size: 16px;
                font-family: 'Roboto', sans-serif;
                }            
        </style>
        <footer><h3 class = "footh3">Cognizant<h3></footer>
    """, unsafe_allow_html=True)


def main():
    # Set page configuration
    st.set_page_config(
        page_title="RFP Accelerator Demo",
        page_icon="images/star.png",  # Replace with your icon path
        layout="wide",
    )
    st.session_state.total_generated_rfps = 0
    st.session_state.generated_responses_count = 0
    st.session_state.average_response_time = 0
    st.session_state.my_proposals_df = pd.DataFrame(columns=["RFP ID", "RFP Name", "Account Name",  "Status", "Submission Date"])
    st.session_state.rfp_sheet_df = ""
    st.session_state.proposal_count = 0
    st.session_state.rfp_id = None
    st.session_state.generated_rfps = {}
    st.session_state.run_model = False
    st.session_state.df_with_answers = None
    st.session_state.processing_time = None
    st.session_state.mp_single_row_selection_callback = False
    st.session_state.selected_rfp_id = None
    st.session_state.csv = None
    start_page()

    

    
if __name__ == '__main__':
    main()
