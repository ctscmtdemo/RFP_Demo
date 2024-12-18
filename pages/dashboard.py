import streamlit as st
import base64
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
        st.rerun()
        st.switch_page("pages/dashboard.py")
    if st.button(" Generate RFPs", use_container_width=True):
        st.switch_page("pages/generate-rfp.py")

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


# Main content
col1, _, col2 = st.columns([5, 3, 4])
with col1:
    st.markdown("""
        <div style="text-align: left; font-size: 16px; margin-bottom: 10px; margin-left: -40px; margin-top: -40px;">
            <h3 style="margin-bottom: -10px;">Welcome User</h3>
            <span style="margin-top: -20px;">Supercharge your productivity with the RFP Accelerator.</span>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(
        """
        <style>
        .st-key-generated_rfp_button_top{
        margin-left: 50px;
        margin-top: -40px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if not st.session_state.my_proposals_df.empty:
        if st.button("Generate RFP Response", key="generated_rfp_button_top", use_container_width=True):
            st.switch_page("pages/generate-rfp.py")


# Three Uniform Containers Below the Top Bar
container_col1, container_col2, container_col3 = st.columns(3)
container_style = """
    <div style="border: 1px solid #ddd; border-top: 2px solid {color}; padding: 20px; border-radius: 10px; height: 150px; position: relative;">
        <h3 style="margin: 0; font-size: 14px;">{title}</h3>
        <p style="font-size: 32px; margin: 10px 0;">{value}</p>
        <img src="{icon}" 
            style="position: absolute; bottom: 10px; right: 10px; width: 40px;" />
    </div>
"""
with container_col1:
    st.markdown(container_style.format(title="Total Generated RFPs", value=st.session_state.total_generated_rfps, icon="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/card1-icon.svg", color="blue"), unsafe_allow_html=True)
with container_col2:
    st.markdown(container_style.format(title="Generated Responses", value=st.session_state.generated_responses_count, icon="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/card2-icon.svg", color="#B2A4D4"), unsafe_allow_html=True)
with container_col3:
    st.markdown(container_style.format(title="Average Response Time (MM:SS)", value=f"{int(st.session_state.average_response_time//60):02d}:{int(st.session_state.average_response_time%60):02d}", icon="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/card3-icon.svg", color="red"), unsafe_allow_html=True)


st.markdown("""
        <div style="text-align: left; font-size: 16px; margin-bottom: 0px; margin-left: -40px; margin-top: 10px;">
            <h5>My proposals</h5>
        </div>
    """, 
    unsafe_allow_html=True
)

with st.container(border=True,height=500, key="my-proposals"):
    # st.markdown(
    #     """
    #     <style>
    #     .stHorizontalBlock>st-emotion-cache-ocqkz7>e1f1d6gn5 {
    #     font-size: 10px;
    #     background-color: #D2DAED;
    #     }

    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )
    # col1,  col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 2, 2, 1])
    # col1.header("**RFP ID**",divider=True)
    # col2.header("**RFP Name**", divider=True)
    # # col2.write()
    # st.markdown("---")
    def single_row_selection_callback():
        st.session_state.mp_single_row_selection_callback = True
    event = st.dataframe(
        st.session_state.my_proposals_df,
        use_container_width=True,
        selection_mode="single-row",
        on_select=single_row_selection_callback, 
        column_config={
            "RFP Name":st.column_config.Column(
                width="medium",
            ),
            "Account Name":st.column_config.Column(
                width="medium"
            )
        },
        hide_index=True,
    )
    modules = event.selection.rows
    if st.session_state.get("mp_single_row_selection_callback", False) is True:
        st.session_state["mp_single_row_selection_callback"] = False
        st.session_state.selected_rfp_id = st.session_state.my_proposals_df.iloc[modules[0]]["RFP ID"] if len(modules) > 0 else None
        if st.session_state.selected_rfp_id is not None and st.session_state.my_proposals_df.iloc[modules[0]]["Status"] == "Success":
            st.switch_page("pages/preview-model-response.py")
    if st.session_state.my_proposals_df.empty:
        st.markdown(
            """
            <div style="text-align: center;">
              <img src="https://rfp-frontend-demo-dot-rfp-automation-genai-demo.uc.r.appspot.com/assets/icons/nodata.svg">
              <p>No RFPs generated yet</p>
              <p>Start by creating your first RFP with the power of Gemini.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        _, __, ___ = st.columns(3)
        if __.button("Generate RFP Response", use_container_width=True):
            st.switch_page("pages/generate-rfp.py")


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
        padding-bottom: 40px;
        padding-top: 10px;
    }
            .footh3{
            font-size: 16px;
            font-family: 'Roboto', sans-serif;
            }            
    </style>
    <footer><h3 class = "footh3">Cognizant<h3></footer>
""", unsafe_allow_html=True)

