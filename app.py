import streamlit as st
import base64
# Configure the page layout
st.set_page_config(page_title="RFP Accelerator", layout="wide")

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "landing"  # Default page

# Function to encode a local image file to Base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Background image not found at {image_path}. Please check the file path.")
        return None

# Encode the local background image
background_image_base64 = encode_image_to_base64("image/bg_image.png")  # Replace with your image file path



# CSS for Background Image
if background_image_base64:
    BACKGROUND_CSS = f"""
    <style>
    body {{
        background-image: url('data:image/png;base64,{background_image_base64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: "Roboto", sans-serif;
    }}
    </style>
    """
else:
    BACKGROUND_CSS = """
    <style>
    body {{
        background-color: #f0f0f0; /* Fallback color if image is missing */
        font-family: "Roboto", sans-serif;
        overflow: hidden;
    }}
    </style>
    """

# Custom CSS to hide Streamlit elements
HIDE_STREAMLIT_STYLE = """
<style>
/* Hide Streamlit header, footer, and three-dot menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

# Custom CSS to hide Streamlit elements
HIDE_STREAMLIT_STYLE = """
<style>
/* Hide Streamlit header, footer, and three-dot menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
HEADER_HTML = """
<div style="
    width: 100%;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    background-color: #C4CED2;
    padding: 10px 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: Left;"
    <img src="" alt="Google Logo" style="height: 40px; margin-right: 10px;">
    <h2 style="margin: 0; font-family: 'Roboto', sans-serif; color: #666;">RFP Accelerator</h2>
</div>
"""


FOOTER_HTML = """
<div style="
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    z-index: 1000;
    background-color: #F5FFFA;
    padding: 10px 20px;
    box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.1);
    text-align: left;">
    <p style="margin: 0; font-family: 'Roboto', sans-serif; font-size: 20px; color: #666;">Cognizant</p>
</div>
"""

# Function for the landing page
def landing_page():
    st.markdown(BACKGROUND_CSS, unsafe_allow_html=True)
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)
    st.markdown(HEADER_HTML, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        body {{
            font-family: "Roboto", sans-serif;
            margin: 0;
            padding: 0;
            background-image: url('data:image/png;base64,{background_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            overflow: hidden;
        }}
        .landing-container {
            text-align: center;
            margin-top: -100px;
            margin: auto;
            padding: 50px;
            
        }
        .title {
            font-size: 58px;
            margin: 0;
            margin-top: -50px;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            font-size: 20px;
            color: #6c757d;
            margin: 20px 0 30px;
        }
        .start-button {
            font-size: 18px;
            margin-top: -15px;
            padding: 15px 30px;
            color: white !important;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .start-button:hover{{background:linear-gradient(to right, #2575fc, #6a11cb);
        }}
        .features {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            gap: 20px;
        }
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: left;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            flex: 1;
            max-width: 400px;
        }
        .feature-icon {
            width: 50px;
            margin-bottom: 10px;
        }
        .feature-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        }
        .feature-desc {
            font-size: 16px;
            color: #666;
        }
        </style>
        <div class="landing-container">
            <h1 class="title">RFP Accelerator, <br> Reimagined with AI</h1>
            <p class="subtitle">
                Accelerate RFP responses and propel business growth<br> with GenAI, 
                the intelligent RFP automation solution <br> powered by Vertex AI and Gemini.
            </p>
            <form action="/" method="get">
                <button type="submit" class="start-button" name="page" value="dashboard">Start</button>
            </form>
            <div class="features">
                <div class="feature-card">
                    <img class="feature-icon" src="https://img.icons8.com/ios-filled/50/6a11cb/file.png" alt="Feature Icon">
                    <p class="feature-title">Speed up your RFP responses Win more business with Google Gemini</p>
                </div>
                <div class="feature-card">
                    <img class="feature-icon" src="https://img.icons8.com/ios-filled/50/2575fc/lightning-bolt.png" alt="Feature Icon">
                    <p class="feature-title">Expert-level accuracy Consistent high quality in every response</p>
                </div>
                <div class="feature-card">
                    <img class="feature-icon" src="https://img.icons8.com/ios-filled/50/ff5733/note.png" alt="Feature Icon">
                    <p class="feature-title">Streamline workflows Accelerate your workflow with AI-powered tools</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Button navigation to Upload RFP
    if st.button("button"):
        st.session_state["page"] = "dashboard"
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

# Function for the dashboard page
def dashboard_page():
    st.markdown(
        """
        <style>
        body {
            font-family: "Roboto", sans-serif;
            background-color: #f9f9f9;
        }
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background-color: white;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        .dashboard-header h1 {
            font-size: 24px;
            font-weight: bold;
        }
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }
        .stat-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .stat-title {
            font-size: 18px;
            color: #333;
        }
        .stat-value {
            font-size: 24px;
            color: #6a11cb;
            font-weight: bold;
        }
        .proposals {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
        }
        .proposals h2 {
            margin-bottom: 20px;
        }
        </style>
        <div class="dashboard-header">
            <h1>Welcome Ashutosh Kumar (xWF)</h1>
            <div class="user-info">
                <p>ashutoshkumar@google.com</p>
            </div>
        </div>
        <div class="stats-container">
            <div class="stat-card">
                <p class="stat-title">Total Generated RFPs</p>
                <p class="stat-value">0</p>
            </div>
            <div class="stat-card">
                <p class="stat-title">Generated Responses</p>
                <p class="stat-value">0</p>
            </div>
            <div class="stat-card">
                <p class="stat-title">Average Response Time (MM:SS)</p>
                <p class="stat-value">-</p>
            </div>
        </div>
        <div class="proposals">
            <h2>My Proposals</h2>
            <p>No RFPs generated yet.<br>Start by creating your first RFP with the power of Gemini.</p>
            <button style="padding: 10px 20px; background-color: #6a11cb; color: white; border: none; border-radius: 5px;">Generate RFP</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Button navigation to Upload RFP
    if st.button("Go to Upload RFP"):
        st.session_state["page"] = "upload_rfp"


# Function for the upload RFP page
def upload_rfp_page():
    st.title("Upload RFP")
    st.markdown("Please provide the required details for the RFP below:")
    st.text_input("RFP Name")
    st.text_input("Account Name")
    st.text_input("RFP URL")
    if st.button("Preview Questions"):
        st.success("Questions preview is under construction!")
    if st.button("Back"):
        st.session_state["page"] = "dashboard"


# Page routing logic
if st.session_state["page"] == "landing":
    landing_page()
elif st.session_state["page"] == "dashboard":
    dashboard_page()
elif st.session_state["page"] == "upload_rfp":
    upload_rfp_page()