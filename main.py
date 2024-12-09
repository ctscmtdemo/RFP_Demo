import streamlit as st
import pandas as pd
import time
from langchain_google_genai import ChatGoogleGenerativeAI

# Set the page configuration
st.set_page_config(layout="wide")  # Enables a wide layout

# Set up the LLM (Gemini model)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="AIzaSyBtQpBgRyi4jneypTye4O4tvprx5riOeNc"  # Replace with your actual API key
)

# Function to generate responses using the Gemini model
def generate_responses(df, model, delay=1.0):
    """
    Generate responses using the Gemini model.
    
    Args:
        df (pd.DataFrame): The input DataFrame with "Question" and "Related Area" columns.
        model: The LLM model instance (e.g., ChatGoogleGenerativeAI).
        delay (float): The delay in seconds between API calls to prevent quota exhaustion.
    
    Returns:
        pd.DataFrame: The input DataFrame with an additional "Answer" column containing generated responses.
    """
    if "Question" not in df.columns or "Related Area" not in df.columns:
        st.error("The uploaded file must contain 'Question' and 'Related Area' columns.")
        return None

    responses = []
    for question in df["Question"]:
        try:
            print(f"Processing question: {question}")
            
            # Prepare the messages input as expected by the model
            messages = [{"role": "user", "content": question}]
            
            # Pass the messages to the generate() method
            response = model.invoke(messages)
            
            # Extract the generated response (assuming it's returned in a specific format)
            generated_content = response.content  
            responses.append(generated_content)
            
            # Introduce a delay between requests to prevent quota exhaustion
            time.sleep(delay)

        except Exception as e:
            st.error(f"Error generating response for '{question}': {e}")
            responses.append(f"Error: {e}")
    
    # Add the generated answers to the DataFrame
    df["Answer"] = responses
    return df





# Custom CSS for layout and styling
custom_css = """
    <style>
        /* Reduce the visible height of the sidebar */
        .css-1d391kg { /* Sidebar container */
            width: 250px;
            padding-top: 100px; /* Increase top padding */
            padding-bottom: 100px; /* Increase bottom padding */
            height: auto; /* Let height adjust to content and padding */
            display: flex;
            flex-direction: column;
            justify-content: space-between; /* Distribute space evenly */
        }

        /* Sidebar content adjustment */
        .css-1lcbmhc { /* Inner content of the sidebar */
            overflow-y: auto; /* Enable scrolling if content overflows */
        }

        /* Header styling */
        header {
            background-color: #C4CED2;
            color: #666;
            padding: 21.5px;
            text-align: left;
            font-size: 20px;
            position: fixed;
            width: 100%;
            top: 25;
            margin-top: -120px;
            left: 0;
            z-index: 100;
            justify-content: Left;
            font-family: 'Roboto', sans-serif;
        }

        /* Footer styling */
        footer {
            background-color: #F5FFFA;
            color: #666;
            padding: 18px;
            text-align: left;
            font-size: 16px;
            position: fixed;
            bottom: 0;
            width: 100%;
            height: 60px;
            left: 0;
            z-index: 100;
            justify-content: Left;
            font-family: 'Roboto', sans-serif;
        }

        /* Main content padding adjustments */
        .css-18e3th9 {
            padding-top: 100px; /* Space for the fixed header */
            padding-bottom: 80px; /* Space for the fixed footer */
        }

        /* Sidebar button styling */
        .sidebar-button {
            display: flex;
            align-items: center;
            justify-content: left;
            padding: 12px 15px;
            margin: 10px 0;
            color: white;
            text-decoration: none;
            background-color: #0073e6;
            border-radius: 15px;
            border: none;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s;
            width: 100%;
            box-sizing: border-box;
            left: 0;
            
        }

        .sidebar-button img {
            width: 20px;
            height: 20px;
            margin-right: 10px;
        }

        .sidebar-button:hover {
            background-color: #005bb5;
            transform: scale(1.02);
        }
        .css-18e3th9 {
            padding-top: 80px;
            padding-bottom: 60px;
        }
        .right-table-container {
            float: right;
            width: 25%;
            margin-left: 40px;
        }
        .left-form-container {
            width: 65%;
            float: left;
        }
        .sidebar-visible {
            display: block !important; /* Show sidebar */
        }
        body {
            font-family: "Roboto", sans-serif;
            margin: 0;
            padding: 0;
            background-image: url('data:image/png;base64,{background_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            overflow: hidden;
            overflow: hidden; /* Prevent scrolling */
            height: 50vh;
        }
        .landing-container {
            text-align: center;
            margin-top: -100px;
            margin: auto;
            padding: 50px;
            
        }
        .title {
            font-size: 48px;
            margin: 0;
            margin-top: -170px;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            background-clip: text;
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
            padding: 12px 24px;
            color: white !important;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .start-button:hover{background:linear-gradient(to right, #2575fc, #6a11cb);
        }
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
            max-width:400px;
            max-height:180px;
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
    <script>
    function navigateToDashboard() {
        const queryString = new URLSearchParams({page: 'dashboard'}).toString();
        window.location.search = queryString;
    }
    </script>
"""

st.markdown("""
    <style>
      section[data-testid="stSidebar"] {
        top: 9.5%; 
        height: 82% !important;
      }
    </style>""", unsafe_allow_html=True)




# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Header Section
st.markdown("<header>RFP Accelerator</header>", unsafe_allow_html=True)

# Footer Section
st.markdown("<footer>Cognizant</footer>", unsafe_allow_html=True)




# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "index"  # Default page is the landing page

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None

# Navigation Logic
if st.session_state["page"] == "index":
    # Render Landing Page
    st.markdown("""
    <div class="landing-container" style="text-align: center; margin-top: 10vh;">
        <h1 class="title" style="font-size: 3rem; color: #6a11cb; margin-bottom: 0;">RFP Accelerator, Reimagined with AI</h1>
        <p class="subtitle" style="font-size: 1.5rem; margin-top: 0; margin-bottom: 0;">
            Accelerate RFP responses and propel business growth<br>
            with GenAI, the intelligent RFP automation solution powered by Vertex AI and Gemini.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # # Start Button (handles navigation to dashboard)
    # button_style = """
    # <style>
    #     .start-button {
    #         background-color: #6a11cb;
    #         color: white;
    #         border: none;
    #         padding: 10px 20px;
    #         font-size: 1.2rem;
    #         cursor: pointer;
    #         border-radius: 5px;
    #         margin-top: 0;
    #         margin-bottom: 0;
    #     }
    # </style>
    # """
    # st.markdown(button_style, unsafe_allow_html=True)
    
    # Create empty columns to center the button
    col1, col2, col3 = st.columns([3, 2, 1.3])

    with col2:  # Place the button in the center column
        if st.button("Start", key="start_button"):
            st.session_state["page"] = "dashboard"

    # Features Section
    st.markdown("""
                
    <div class="features" style="display: flex; justify-content: center; margin-top: 50px; gap: 20px;">
        <div class="feature-card" style="text-align: center; width: 200px;">
            <img class="feature-icon" src="https://img.icons8.com/ios-filled/50/6a11cb/file.png" alt="Feature Icon">
            <p class="feature-title" style="font-size: 1rem;">
                Speed up your RFP responses<br>Win more business with Google Gemini
            </p>
        </div>
        <div class="feature-card" style="text-align: center; width: 200px;">
            <img class="feature-icon" src="https://img.icons8.com/ios-filled/50/2575fc/lightning-bolt.png" alt="Feature Icon">
            <p class="feature-title" style="font-size: 1rem;">
                Expert-level accuracy<br>Consistent high quality in every response
            </p>
        </div>
        <div class="feature-card" style="text-align: center; width: 200px;">
            <img class="feature-icon" src="https://img.icons8.com/ios-filled/50/ff5733/note.png" alt="Feature Icon">
            <p class="feature-title" style="font-size: 1rem;">
                Streamline workflows<br>Accelerate your workflow with AI-powered tools
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Dashboard Page
elif st.session_state["page"] == "dashboard":
    # Sidebar with icons
    with st.sidebar:
        # Custom HTML for Menu Heading
        st.markdown("""
            <div style="display: flex; align-items: center; font-size: 18px; margin-bottom: 20px;">
                <img src="https://img.icons8.com/ios-glyphs/20/menu--v1.png" alt="menu-icon" style="margin-right: 8px;">
                <span>Menu</span>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Dashboard", key="dashboard_button_dashboard"):
            st.session_state["page"] = "dashboard"
        if st.button("Generated RFP", key="generated_rfp_button_dashboard"):
            st.session_state["page"] = "generated_rfp"

    # Main content
    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown("""
            <div style="text-align: left; font-size: 16px; margin-top: -50px; margin-bottom: 10px;">
                <strong>Welcome User</strong><br>
                <span>Supercharge your productivity with the RFP Accelerator.</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("Generated RFP", key="generated_rfp_button_top"):
            st.session_state["page"] = "generated_rfp"

    # Three Uniform Containers Below the Top Bar
    container_col1, container_col2, container_col3 = st.columns(3)

    container_style = """
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; height: 150px; position: relative;">
            <h3 style="margin: 0; font-size: 18px;">{title}</h3>
            <p style="font-size: 32px; font-weight: bold; margin: 10px 0;">{value}</p>
            <img src="{icon}" 
                style="position: absolute; bottom: 10px; right: 10px; width: 40px;" />
        </div>
    """

    with container_col1:
        st.markdown(container_style.format(title="Total Generated RFPs", value="123", icon="https://img.icons8.com/material-outlined/48/000000/folder-invoices.png"), unsafe_allow_html=True)

    with container_col2:
        st.markdown(container_style.format(title="Generated Responses", value="456", icon="https://img.icons8.com/ios/50/000000/reply-arrow.png"), unsafe_allow_html=True)

    with container_col3:
        st.markdown(container_style.format(title="Average Response Time (MM:SS)", value="02:15", icon="https://img.icons8.com/ios-glyphs/50/000000/stopwatch.png"), unsafe_allow_html=True)

    st.subheader("My Proposals")

# Generated RFP Page
elif st.session_state["page"] == "generated_rfp":
    with st.sidebar:
        # Custom HTML for Menu Heading
        st.markdown("""
            <div style="display: flex; align-items: center; font-size: 18px; margin-bottom: 20px;">
                <img src="https://img.icons8.com/ios-glyphs/20/menu--v1.png" alt="menu-icon" style="margin-right: 8px;">
                <span>Menu</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Dashboard", key="dashboard_button_generated_rfp"):
            st.session_state["page"] = "dashboard"
        if st.button("Generated RFP", key="generated_rfp_button_generated_rfp"):
            st.session_state["page"] = "generated_rfp"

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown("""
            <div style="text-align: left; font-size: 14px; margin-top: -70px; margin-bottom: 10px;">
                <strong>Home / Create new RFP</strong><br>
                <span>Upload RFP</span>
            </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("RFP Details")
        st.markdown("Please provide the required details for the RFP below, including <br> the account/company name, and the URL of the question sheet.<br> Ensure all the fields are accurately completed to proceed.", unsafe_allow_html=True)

    with col2:
        with st.form(key="rfp_form"):
            rfp_name = st.text_input("RFP Name", placeholder=" ")
            account_name = st.text_input("Account Name", placeholder=" ")
            uploaded_file = st.file_uploader("Upload RFP File", type=["csv", "xlsx"])
            
            col1_form, col2_form = st.columns(2)
            with col1_form:
                back_button = st.form_submit_button("Back")
            with col2_form:
                preview_button = st.form_submit_button("Preview Questions")
            
            if preview_button and uploaded_file:
                st.session_state["uploaded_file"] = uploaded_file
                st.session_state["page"] = "generated_rfp_preview_question"

# Preview Uploaded File Page
elif st.session_state["page"] == "generated_rfp_preview_question":
    with st.sidebar:
        # Custom HTML for Menu Heading
        st.markdown("""
            <div style="display: flex; align-items: center; font-size: 18px; margin-bottom: 20px;">
                <img src="https://img.icons8.com/ios-glyphs/20/menu--v1.png" alt="menu-icon" style="margin-right: 8px;">
                <span>Menu</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Dashboard", key="dashboard_button_preview"):
            st.session_state["page"] = "dashboard"
        if st.button("Generated RFP", key="generated_rfp_button_preview"):
            st.session_state["page"] = "generated_rfp"

    st.subheader("Preview Questions")

    # Retrieve or upload file
    uploaded_file = st.session_state.get("uploaded_file", None)
    if uploaded_file is None:
        st.warning("Please upload a file to preview.")
    else:
        try:
            # Load file from session state (if previously loaded)
            if "preview_df" in st.session_state:
                df = st.session_state["preview_df"]
            else:
                # Read file and save to session state
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file, encoding="utf-8", delimiter=",")
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)

                if df.empty:
                    st.error("The uploaded file is empty. Please upload a valid file.")
                
                # Save the DataFrame for future use
                st.session_state["preview_df"] = df

            # Display the DataFrame
            st.dataframe(df)

        except pd.errors.EmptyDataError:
            st.error("No columns found in the uploaded file. Please upload a valid CSV or Excel file.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back_button_preview"):
            st.session_state["page"] = "dashboard"
    with col2:
        if st.button("Generate RFP", key="generate_rfp_button"):
            if "preview_df" in st.session_state:
                st.session_state["page"] = "generate_rfp"
            else:
                st.error("No data to generate RFP. Please upload and preview a valid file.")



# Generate RFP Responses Page
elif st.session_state["page"] == "generate_rfp":
    with st.sidebar:
        # Custom HTML for Menu Heading
        st.markdown("""
            <div style="display: flex; align-items: center; font-size: 18px; margin-bottom: 20px;">
                <img src="https://img.icons8.com/ios-glyphs/20/menu--v1.png" alt="menu-icon" style="margin-right: 8px;">
                <span>Menu</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Dashboard", key="dashboard_button_generate"):
            st.session_state["page"] = "dashboard"
        if st.button("Generated RFP", key="generated_rfp_button_generate"):
            st.session_state["page"] = "generated_rfp"

    st.subheader("Generated RFP Answers (Gemini Responses)")
    if "preview_df" in st.session_state:
        df = st.session_state["preview_df"]
        # Generate responses
        with st.spinner("Generating responses..."):
            df_with_answers = generate_responses(df, llm)
            if df_with_answers is not None:
                st.dataframe(df_with_answers)  # Display the updated DataFrame
                st.session_state["generated_responses"] = df_with_answers

                # Option to download the file
                csv = df_with_answers.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Generated Responses",
                    data=csv,
                    file_name="generated_responses.csv",
                    mime="text/csv",
                )
                # Navigation buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Done", key="done_button_generate"):
                        st.session_state["page"] = "dashboard"
                # Clear session state and reset the app
                st.session_state.clear()  # Clear all session state variables
                st.session_state["page"] = "dashboard"  # Redirect to the initial page
                # st.experimental_set_query_params(page="index")  # Update query params
    else:
        st.error("No data available. Please go back and upload a file.")

    
    # if "uploaded_file" in st.session_state:
    #     st.markdown("Below are the simulated Gemini answers based on the uploaded file:")
    #     st.write("Generated Answers for the uploaded questions go here...")
    
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button("Done", key="done_button_generate"):
    #         st.session_state["page"] = "dashboard"
    # with col2:
    #     if st.button("Download", key="download_button_generate"):
    #         st.markdown("[Download Generated RFP Answers](#)")