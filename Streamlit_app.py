import streamlit as st
import pandas as pd
import datetime
import pyrebase
from io import BytesIO
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
# Initialize Google Sheets client
def init_gsheets():
    try:
        # Define required scopes
        scopes = ["https://www.googleapis.com/auth/spreadsheets", 
                  "https://www.googleapis.com/auth/drive"]

        # Load credentials from secrets
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )

        # Authorize client
        client = gspread.authorize(creds)
        return client

    except Exception as e:
        st.error(f"Google Sheets initialization failed: {str(e)}")
        return None

# Load data from Google Sheet
def load_sheet_data(sheet_name):
    try:
        client = init_gsheets()
        if not client:
            return pd.DataFrame()
            
        spreadsheet = client.open(st.secrets["gcp_service_account"]["V2 Database"])
        worksheet = spreadsheet.worksheet(sheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading {sheet_name} data: {str(e)}")
        return pd.DataFrame()

# Save data to Google Sheet
def save_sheet_data(sheet_name, df):
    try:
        client = init_gsheets()
        if not client:
            st.error("Google Sheets client not initialized")
            return False
            
        spreadsheet = client.open(st.secrets["gcp_service_account"]["spreadsheet_name"])
        worksheet = spreadsheet.worksheet(sheet_name)
        
        # Clear existing data and update with new
        worksheet.clear()
        
        # Handle empty DataFrames
        if df.empty:
            # Initialize with column headers
            worksheet.append_row(df.columns.tolist())
            return True
            
        # Convert DataFrame to list of lists
        data = [df.columns.tolist()] + df.values.tolist()
        worksheet.update('A1', data)
        return True
    except Exception as e:
        st.error(f"Error saving {sheet_name} data: {str(e)}")
        return False

# Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyBAgKUj_k6LWknvQNcOd8MCuyZ2Fr-CZ4g",
    "authDomain": "fmcg-crm.firebaseapp.com",
    "projectId": "fmcg-crm",
    "storageBucket": "fmcg-crm.appspot.com",
    "messagingSenderId": "707121794976",
    "appId": "1:707121794976:web:4447f153b9051498a71ec5",
    "databaseURL": "https://fmcg-crm-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Set page config
st.set_page_config(
    page_title="V2-Value Variety Global Trading company ",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f0f7ff 0%, #e6f7ff 100%);
    }

    .header {
        background: linear-gradient(120deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 1rem 1rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .hero {
        background: linear-gradient(120deg, #ffffff, #f0f9ff);
        border-radius: 15px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border: 1px solid #d1e8ff;
    }

    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.8rem;
        height: 100%;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
    }

    .login-card {
        background: white;
        border-radius: 15px;
        padding: 2.5rem;
        margin: 0 auto;
        max-width: 500px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 5px solid #3b82f6;
    }

    .btn-primary {
        background: linear-gradient(120deg, #1e3a8a, #3b82f6);
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
        width: 100%;
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
    }

    .error-message {
        color: #ff4b4b;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }
    .success-message {
        color: #4ade80;
        text-align: center;
        margin: 1rem 0;
        font-weight: 500;
    }

    .stTextInput>div>div>input, 
    .stTextInput>div>div>input:focus {
        border: 1px solid #d1e8ff !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.05) !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

    .stButton>button {
        width: 100%;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
    }

    .stButton>button:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }

    .footer {
        background: linear-gradient(120deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 2rem 1rem;
        border-radius: 15px 15px 0 0;
        margin-top: 3rem;
        text-align: center;
    }

    .form-title {
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }

    .link-button {
        background: none !important;
        border: none;
        color: #3b82f6 !important;
        text-decoration: underline;
        cursor: pointer;
        padding: 0 !important;
        font-weight: 500;
    }

    .link-button:hover {
        color: #1e3a8a !important;
        text-decoration: underline;
    }

    .login-options {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }

    /* Fix for text color */
    .stMarkdown, .stTextInput>label, .stButton>button, .stAlert {
        color: #333333 !important;
    }

    /* Fix for form labels */
    .stTextInput>label {
        font-weight: 500;
        color: #1e3a8a !important;
    }

    /* App specific styles */
    .app-header {font-size:24px !important; font-weight:bold; color:#1e3a8a;}
    .subheader {font-size:18px !important; font-weight:600; color:#3b82f6; border-bottom:1px solid #eee; padding-bottom:5px;}
    .metric {background-color:#f0f9ff; padding:15px; border-radius:10px; text-align:center; box-shadow:0 2px 5px rgba(0,0,0,0.05);}
    .metric-value {font-size:24px; font-weight:bold; color:#1e3a8a;}
    .metric-label {font-size:14px; color:#6b7280;}
    .stDataFrame {border-radius:10px !important;}
    .stTextInput>div>div>input, .stSelectbox>div>div>select {border-radius:8px !important;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.auth_message = {'type': None, 'text': None}
    st.session_state.show_password_reset = False
    st.session_state.show_signup = False
    st.session_state.edit_customer = None
    
    # Initialize empty DataFrames with proper columns
    st.session_state.customers = pd.DataFrame(columns=[
        'Name', 'Contact', 'Email', 'Address', 'Company', 'Category'
    ])
    st.session_state.leads = pd.DataFrame(columns=[
        'Customer', 'Status', 'Value', 'Salesperson', 'Notes', 'FollowUp'
    ])
    st.session_state.interactions = pd.DataFrame(columns=[
        'Customer', 'Type', 'Date', 'Notes'
    ])

# Firebase authentication functions
def signup_user(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
        st.session_state.auth_message = {
            'type': 'success',
            'text': 'Account created! Please check your email to verify your account.'
        }
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False

def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        user_info = auth.get_account_info(user['idToken'])
        if not user_info['users'][0]['emailVerified']:
            st.session_state.auth_message = {
                'type': 'error',
                'text': 'Please verify your email before logging in.'
            }
            return False

        st.session_state.authenticated = True
        st.session_state.user = email
        
        # LOAD DATA FROM GOOGLE SHEETS AFTER LOGIN
        try:
            # Load customers
            customers_df = load_sheet_data("Customers")
            if not customers_df.empty:
                st.session_state.customers = customers_df
            
            # Load leads
            leads_df = load_sheet_data("Leads")
            if not leads_df.empty:
                st.session_state.leads = leads_df
                
            # Load interactions
            interactions_df = load_sheet_data("Interactions")
            if not interactions_df.empty:
                st.session_state.interactions = interactions_df
                
            st.session_state.auth_message = {'type': 'success', 'text': 'Login successful! Data loaded.'}
        except Exception as e:
            st.session_state.auth_message = {'type': 'error', 'text': f'Data load error: {str(e)}'}
            
        st.session_state.page = "app"
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False

def reset_password(email):
    try:
        auth.send_password_reset_email(email)
        st.session_state.auth_message = {
            'type': 'success',
            'text': 'Password reset email sent! Please check your inbox.'
        }
        st.session_state.show_password_reset = False
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False

# Page functions
def home_page():
    # Header section
    st.markdown("""
    <div class="header">
        <div style="display:flex; align-items:center; justify-content:space-between; max-width:1200px; margin:0 auto;">
            <div>
                <h1 style="font-size:2.8rem; margin-bottom:0.5rem; color:white;">FMCG CRM</h1>
                <p style="font-size:1.2rem; opacity:0.9; color:white;">Transform Your Sales Process with Intelligent CRM</p>
            </div>
            <div style="font-size: 3rem; color:white;">
                🚀
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div style="max-width:1200px; margin:0 auto; padding:0 1rem;">
        <div class="hero">
            <h2 style="color:#1e3a8a; margin-top:0; font-size:2.2rem;">Transform Your Sales Process</h2>
            <p style="font-size:1.1rem; line-height:1.7; color:#333;">
                Manage customers, track leads, and analyze sales performance in one powerful platform 
                designed specifically for the FMCG industry. Our CRM helps you optimize your sales pipeline, 
                improve customer relationships, and boost revenue growth.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats section
    st.markdown("""
    <div style="max-width:1200px; margin:2rem auto; padding:0 1rem;">
        <h3 style="color:#1e3a8a; font-size:1.5rem; margin-bottom:1rem;">Why Companies Choose Us</h3>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:1.5rem; margin-bottom:2rem;">
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; font-weight:700; margin-bottom:0.5rem;">45%</div>
                <p style="color:#333;">Increase in Sales</p>
            </div>
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; font-weight:700; margin-bottom:0.5rem;">60%</div>
                <p style="color:#333;">Reduced Admin Time</p>
            </div>
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; font-weight:700; margin-bottom:0.5rem;">35%</div>
                <p style="color:#333;">Customer Retention</p>
            </div>
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; font-weight:700; margin-bottom:0.5rem;">200+</div>
                <p style="color:#333;">Happy Companies</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("""
    <div style="max-width:1200px; margin:2rem auto; padding:0 1rem;">
        <h3 style="color:#1e3a8a; font-size:1.5rem; margin-bottom:1rem;">Key Features</h3>
        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:1.5rem; margin-bottom:2rem;">
            <div class="feature-card">
                <h3 style="color:#1e3a8a; margin-top:0;">👥 Customer Management</h3>
                <p style="color:#444; line-height:1.6;">
                    Centralize all customer information with detailed profiles, interaction history, 
                    and purchase patterns in one place.
                </p>
            </div>
            <div class="feature-card">
                <h3 style="color:#1e3a8a; margin-top:0;">📈 Lead Tracking</h3>
                <p style="color:#444; line-height:1.6;">
                    Monitor your sales pipeline with visual Kanban boards and automated lead scoring 
                    to prioritize opportunities.
                </p>
            </div>
            <div class="feature-card">
                <h3 style="color:#1e3a8a; margin-top:0;">📊 Sales Analytics</h3>
                <p style="color:#444; line-height:1.6;">
                    Real-time performance dashboards and reports with AI-powered insights to drive 
                    data-driven decisions.
                </p>
            </div>
            <div class="feature-card">
                <h3 style="color:#1e3a8a; margin-top:0;">🔔 Notifications</h3>
                <p style="color:#444; line-height:1.6;">
                    Get timely alerts for follow-ups, meetings, and important customer interactions 
                    to never miss an opportunity.
                </p>
            </div>
            <div class="feature-card">
                <h3 style="color:#1e3a8a; margin-top:0;">🔄 Workflow Automation</h3>
                <p style="color:#444; line-height:1.6;">
                    Automate repetitive tasks and follow-ups to focus on high-value activities and 
                    improve team productivity.
                </p>
            </div>
            <div class="feature-card">
                <h3 style="color:#1e3a8a; margin-top:0;">📱 Mobile Access</h3>
                <p style="color:#444; line-height:1.6;">
                    Access your CRM anywhere, anytime with our fully responsive interface that works 
                    seamlessly on all devices.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Testimonials section
    st.markdown("""
    <div style="max-width:1200px; margin:2rem auto; padding:0 1rem;">
        <h3 style="color:#1e3a8a; font-size:1.5rem; margin-bottom:1rem;">What Our Users Say</h3>
        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:1.5rem; margin-bottom:2rem;">
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; margin-bottom:0.5rem;">"</div>
                <p style="font-style: italic; color:#333; line-height:1.7;">
                    This CRM helped us increase conversion rates by 35% in just 3 months. 
                    The analytics tools are unmatched in the industry.
                </p>
                <p style="font-weight:600; margin-bottom:0; color:#333;">John Davidson</p>
                <p style="color:#3b82f6; margin-top:0;">Marketing Director, FMCG Co.</p>
            </div>
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; margin-bottom:0.5rem;">"</div>
                <p style="font-style: italic; color:#333; line-height:1.7;">
                    The intuitive interface reduced our training time by 60%. Our sales team 
                    adopted it immediately with minimal guidance.
                </p>
                <p style="font-weight:600; margin-bottom:0; color:#333;">Sarah Reynolds</p>
                <p style="color:#3b82f6; margin-top:0;">Sales Manager, Retail Group</p>
            </div>
            <div class="feature-card">
                <div style="font-size:2rem; color:#1e3a8a; margin-bottom:0.5rem;">"</div>
                <p style="font-style: italic; color:#333; line-height:1.7;">
                    Customizable reports give us insights we never had before. We've optimized 
                    our inventory based on predictive analytics.
                </p>
                <p style="font-weight:600; margin-bottom:0; color:#333;">Michael Torres</p>
                <p style="color:#3b82f6; margin-top:0;">CEO, Distribution Network</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA section
    st.markdown("""
    <div style="max-width:1200px; margin:3rem auto; padding:0 1rem; text-align:center;">
        <h3 style="color:#1e3a8a; font-size:1.8rem;">Ready to Transform Your Sales Process?</h3>
        <p style="font-size:1.1rem; margin-bottom:1.5rem; max-width:700px; margin-left:auto; margin-right:auto; color:#333;">
            Join hundreds of FMCG professionals using our CRM solution to streamline their sales operations.
        </p>
        <p style="margin-top:1rem; color:#666;">No credit card required. Free for small teams.</p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <div style="max-width:1200px; margin:0 auto;">
            <h4 style="color:white;">FMCG CRM</h4>
            <p style="color:white;">© 2025 FMCG CRM. All rights reserved.</p>
            <p style="color:white;">Contact: support@fmcgcrm.com | +971 52 272 7760</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Handle button clicks
    if st.button("Get Started Now", key="home_get_started", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

def firebase_login():
    """Firebase login form with styled elements"""
    st.markdown('<h3 class="form-title">Login to Your Account</h3>', unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login", type="primary", use_container_width=True)

        if submit:
            if email and password:
                login_user(email, password)
                st.rerun()
            else:
                st.session_state.auth_message = {'type': 'error', 'text': 'Please enter email and password'}
                st.rerun()

    # Login options
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Forgot Password?", type="secondary", use_container_width=True):
            st.session_state.show_password_reset = True
            st.session_state.auth_message = {'type': None, 'text': None}
            st.rerun()
    with col2:
        if st.button("Back to Home", type="secondary", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.auth_message = {'type': None, 'text': None}
            st.rerun()

    st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#555; margin-bottom:1rem;">Don\'t have an account?</p>',
                unsafe_allow_html=True)

    if st.button("Create Account", type="primary", use_container_width=True):
        st.session_state.show_signup = True
        st.session_state.auth_message = {'type': None, 'text': None}
        st.rerun()

def firebase_signup():
    """Firebase signup form with attractive styling"""
    st.markdown('<h3 class="form-title">Create New Account</h3>', unsafe_allow_html=True)

    with st.form("signup_form"):
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        submit = st.form_submit_button("Sign Up", type="primary", use_container_width=True)

        if submit:
            if new_email and new_password and confirm_password:
                if new_password == confirm_password:
                    signup_user(new_email, new_password)
                    st.rerun()
                else:
                    st.session_state.auth_message = {'type': 'error', 'text': 'Passwords do not match'}
                    st.rerun()
            else:
                st.session_state.auth_message = {'type': 'error', 'text': 'Please fill all fields'}
                st.rerun()

    if st.button("Back to Login", type="secondary", use_container_width=True):
        st.session_state.show_signup = False
        st.session_state.auth_message = {'type': None, 'text': None}
        st.rerun()

def password_reset():
    """Password reset form with attractive styling"""
    st.markdown('<h3 class="form-title">Password Reset</h3>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center; margin-bottom:1.5rem; color:#555;">Enter your email to receive a password reset link</p>',
        unsafe_allow_html=True)

    with st.form("reset_form"):
        email = st.text_input("Enter your email", key="reset_email")
        submit = st.form_submit_button("Send Reset Link", type="primary", use_container_width=True)

        if submit:
            if email:
                reset_password(email)
                st.rerun()
            else:
                st.session_state.auth_message = {'type': 'error', 'text': 'Please enter your email'}
                st.rerun()

    if st.button("Back to Login", type="secondary", use_container_width=True):
        st.session_state.show_password_reset = False
        st.session_state.auth_message = {'type': None, 'text': None}
        st.rerun()

def login_page():
    # Header with same style as home page
    st.markdown("""
    <div class="header" style="padding: 1rem 1rem;">
        <div style="display:flex; align-items:center; justify-content:space-between; max-width:1200px; margin:0 auto;">
            <div>
                <h1 style="font-size:1.8rem; margin-bottom:0.5rem; color:white;">FMCG CRM</h1>
                <p style="font-size:1rem; opacity:0.9; color:white;">Login to Your Account</p>
            </div>
            <div style="font-size: 2rem; color:white;">
                🔒
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered card layout
    st.markdown("""
    <div style="max-width:500px; margin:2rem auto; padding:0 1rem;">
        <div class="login-card">
    """, unsafe_allow_html=True)

    # Show messages if any
    if st.session_state.auth_message['type']:
        if st.session_state.auth_message['type'] == 'error':
            st.markdown(f"<div class='error-message'>{st.session_state.auth_message['text']}</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='success-message'>{st.session_state.auth_message['text']}</div>",
                        unsafe_allow_html=True)

    if st.session_state.show_password_reset:
        password_reset()
    elif st.session_state.show_signup:
        firebase_signup()
    else:
        firebase_login()

    st.markdown("</div></div>", unsafe_allow_html=True)

def app_page():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3144/3144456.png", width=80)
    st.sidebar.title("Sales CRM")

    # Add logout button
    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.page = "login"
        st.rerun()

    menu = st.sidebar.selectbox("Navigation", [
        "Dashboard",
        "Customer Management",
        "Lead Tracking",
        "Interaction Logs",
        "Sales Pipeline",
        "Reporting",
        "Export Data"
    ])

    # Dashboard Tab
    if menu == "Dashboard":
        st.markdown('<p class="app-header">Sales Dashboard</p>', unsafe_allow_html=True)

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric"><div class="metric-value">' +
                        str(len(st.session_state.customers)) +
                        '</div><div class="metric-label">Total Customers</div></div>',
                        unsafe_allow_html=True)
        with col2:
            # Handle case where Status column might be missing
            if not st.session_state.leads.empty and 'Status' in st.session_state.leads.columns:
                active_leads = len(
                    st.session_state.leads[st.session_state.leads['Status'].isin(['New', 'Contacted', 'Quoted'])])
            else:
                active_leads = 0
            st.markdown(
                f'<div class="metric"><div class="metric-value">{active_leads}</div><div class="metric-label">Active Leads</div></div>',
                unsafe_allow_html=True)
        with col3:
            if not st.session_state.leads.empty and 'Status' in st.session_state.leads.columns:
                converted = len(st.session_state.leads[st.session_state.leads['Status'] == 'Converted'])
                conversion_rate = (converted / len(st.session_state.leads)) * 100 if len(st.session_state.leads) > 0 else 0
            else:
                conversion_rate = 0
            st.markdown(
                f'<div class="metric"><div class="metric-value">{conversion_rate:.1f}%</div><div class="metric-label">Conversion Rate</div></div>',
                unsafe_allow_html=True)
        with col4:
            if not st.session_state.leads.empty and 'Value' in st.session_state.leads.columns:
                total_value = st.session_state.leads['Value'].sum()
            else:
                total_value = 0
            st.markdown(
                f'<div class="metric"><div class="metric-value">${total_value:,.0f}</div><div class="metric-label">Pipeline Value</div></div>',
                unsafe_allow_html=True)

        # Charts
        st.markdown('<p class="subheader">Lead Status Distribution</p>', unsafe_allow_html=True)
        if not st.session_state.leads.empty and 'Status' in st.session_state.leads.columns:
            status_counts = st.session_state.leads['Status'].value_counts().reset_index()
            fig = px.pie(status_counts, names='Status', values='count', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No leads data available")

        # Recent Activities
        st.markdown('<p class="subheader">Recent Activities</p>', unsafe_allow_html=True)
        if not st.session_state.interactions.empty and 'Date' in st.session_state.interactions.columns:
            recent_interactions = st.session_state.interactions.sort_values('Date', ascending=False).head(5)
            st.dataframe(recent_interactions, hide_index=True)
        else:
            st.info("No recent activities")

    # Customer Management Tab
    elif menu == "Customer Management":
        st.markdown('<p class="app-header">Customer Management</p>', unsafe_allow_html=True)
        
        with st.expander("Add New Customer", expanded=True):
            with st.form("customer_form"):
                cols = st.columns(2)
                name = cols[0].text_input("Full Name*")
                contact = cols[1].text_input("Phone Number*")
                email = cols[0].text_input("Email*")
                company = cols[1].text_input("Company")
                address = cols[0].text_input("Address")
                category = cols[1].selectbox("Category", ["Retailer", "Distributor", "Wholesaler", "Individual"])

                if st.form_submit_button("Save Customer"):
                    if name and contact and email:
                        new_customer = pd.DataFrame([{
                            'Name': name,
                            'Contact': contact,
                            'Email': email,
                            'Address': address,
                            'Company': company,
                            'Category': category
                        }])
                        st.session_state.customers = pd.concat(
                            [st.session_state.customers, new_customer], 
                            ignore_index=True
                        )
                        
                        # SAVE TO GOOGLE SHEETS
                        if save_sheet_data("Customers", st.session_state.customers):
                            st.success("Customer added and saved to cloud!")
                        else:
                            st.error("Customer added locally but cloud save failed")
                    else:
                        st.error("Please fill required fields")
        
        st.markdown('<p class="subheader">Customer Directory</p>', unsafe_allow_html=True)
        if not st.session_state.customers.empty:
            st.dataframe(st.session_state.customers, use_container_width=True, hide_index=True)

            # Edit/Delete functionality
            st.markdown('<p class="subheader">Manage Customers</p>', unsafe_allow_html=True)
            customer_names = st.session_state.customers['Name'].tolist()
            selected_customer = st.selectbox("Select Customer to Manage", customer_names)

            if selected_customer:
                customer_data = st.session_state.customers[st.session_state.customers['Name'] == selected_customer].iloc[0]

                cols = st.columns(3)
                if cols[0].button("Edit Customer"):
                    st.session_state.edit_customer = customer_data

                if cols[1].button("Delete Customer"):
                    st.session_state.customers = st.session_state.customers[
                        st.session_state.customers['Name'] != selected_customer
                    ]
                    # SAVE TO GOOGLE SHEETS
                    if save_sheet_data("Customers", st.session_state.customers):
                        st.success("Customer deleted and updated in cloud!")
                    else:
                        st.error("Deletion saved locally but cloud update failed")
                    st.rerun()

                if 'edit_customer' in st.session_state:
                    with st.expander("Edit Customer", expanded=True):
                        with st.form("edit_customer_form"):
                            cols = st.columns(2)
                            name = cols[0].text_input("Full Name*", value=st.session_state.edit_customer['Name'])
                            contact = cols[1].text_input("Phone Number*", value=st.session_state.edit_customer['Contact'])
                            email = cols[0].text_input("Email*", value=st.session_state.edit_customer['Email'])
                            company = cols[1].text_input("Company", value=st.session_state.edit_customer['Company'])
                            address = cols[0].text_input("Address", value=st.session_state.edit_customer['Address'])
                            category = cols[1].selectbox("Category",
                                                         ["Retailer", "Distributor", "Wholesaler", "Individual"],
                                                         index=["Retailer", "Distributor", "Wholesaler", "Individual"].index(
                                                             st.session_state.edit_customer['Category']))

                            if st.form_submit_button("Update Customer"):
                                if name and contact and email:
                                    # Update customer
                                    idx = st.session_state.customers[
                                        st.session_state.customers['Name'] == st.session_state.edit_customer['Name']
                                        ].index[0]

                                    st.session_state.customers.at[idx, 'Name'] = name
                                    st.session_state.customers.at[idx, 'Contact'] = contact
                                    st.session_state.customers.at[idx, 'Email'] = email
                                    st.session_state.customers.at[idx, 'Company'] = company
                                    st.session_state.customers.at[idx, 'Address'] = address
                                    st.session_state.customers.at[idx, 'Category'] = category

                                    # SAVE TO GOOGLE SHEETS
                                    if save_sheet_data("Customers", st.session_state.customers):
                                        st.success("Customer updated in cloud!")
                                    else:
                                        st.error("Update saved locally but cloud update failed")
                                    
                                    del st.session_state.edit_customer
                                    st.rerun()
                                else:
                                    st.error("Please fill required fields")
        else:
            st.info("No customers found. Add your first customer using the form above.")

    # Lead Tracking Tab
    elif menu == "Lead Tracking":
        st.markdown('<p class="app-header">Lead Tracking</p>', unsafe_allow_html=True)

        with st.expander("Add New Lead", expanded=True):
            with st.form("lead_form"):
                cols = st.columns(2)
                customer = cols[0].selectbox("Customer*", st.session_state.customers[
                    'Name'].tolist() if not st.session_state.customers.empty else [])
                status = cols[1].selectbox("Status*", ["New", "Contacted", "Quoted", "Converted", "Lost"])
                value = cols[0].number_input("Potential Value ($)", min_value=0, step=100)
                salesperson = cols[1].text_input("Salesperson")
                notes = st.text_area("Notes")
                follow_up = st.date_input("Follow-up Date", min_value=datetime.date.today())

                if st.form_submit_button("Save Lead"):
                    if customer:
                        new_lead = pd.DataFrame([{
                            'Customer': customer,
                            'Status': status,
                            'Value': value,
                            'Salesperson': salesperson,
                            'Notes': notes,
                            'FollowUp': follow_up
                        }])
                        st.session_state.leads = pd.concat([st.session_state.leads, new_lead], ignore_index=True)
                        
                        # SAVE TO GOOGLE SHEETS
                        if save_sheet_data("Leads", st.session_state.leads):
                            st.success("Lead saved to cloud!")
                        else:
                            st.error("Lead saved locally but cloud save failed")
                    else:
                        st.error("Please select a customer")

        st.markdown('<p class="subheader">Active Leads</p>', unsafe_allow_html=True)
        if not st.session_state.leads.empty and 'Status' in st.session_state.leads.columns:
            active_leads = st.session_state.leads[st.session_state.leads['Status'].isin(['New', 'Contacted', 'Quoted'])]
            st.dataframe(active_leads, use_container_width=True, hide_index=True)
        else:
            st.info("No active leads found")

    # Interaction Logs Tab
    elif menu == "Interaction Logs":
        st.markdown('<p class="app-header">Interaction Logs</p>', unsafe_allow_html=True)

        with st.expander("Log New Interaction", expanded=True):
            with st.form("interaction_form"):
                cols = st.columns(2)
                customer = cols[0].selectbox("Customer*", st.session_state.customers[
                    'Name'].tolist() if not st.session_state.customers.empty else [])
                interaction_type = cols[1].selectbox("Type*", ["Call", "Meeting", "Email"])
                date = st.date_input("Date*", datetime.date.today())
                notes = st.text_area("Notes*")

                if st.form_submit_button("Log Interaction"):
                    if customer and notes:
                        new_interaction = pd.DataFrame([{
                            'Customer': customer,
                            'Type': interaction_type,
                            'Date': date,
                            'Notes': notes
                        }])
                        st.session_state.interactions = pd.concat([st.session_state.interactions, new_interaction],
                                                                  ignore_index=True)
                        
                        # SAVE TO GOOGLE SHEETS
                        if save_sheet_data("Interactions", st.session_state.interactions):
                            st.success("Interaction saved to cloud!")
                        else:
                            st.error("Interaction saved locally but cloud save failed")
                    else:
                        st.error("Please fill required fields")

        st.markdown('<p class="subheader">Interaction History</p>', unsafe_allow_html=True)
        if not st.session_state.interactions.empty:
            customer_filter = st.selectbox("Filter by Customer",
                                           ["All"] + st.session_state.customers['Name'].tolist())

            if customer_filter != "All":
                filtered_interactions = st.session_state.interactions[
                    st.session_state.interactions['Customer'] == customer_filter
                    ]
            else:
                filtered_interactions = st.session_state.interactions

            st.dataframe(filtered_interactions.sort_values('Date', ascending=False),
                         use_container_width=True, hide_index=True)
        else:
            st.info("No interactions logged yet")

    # Sales Pipeline Tab
    elif menu == "Sales Pipeline":
        st.markdown('<p class="app-header">Sales Pipeline</p>', unsafe_allow_html=True)

        if not st.session_state.leads.empty:
            # Filters
            cols = st.columns(3)
            status_filter = cols[0].multiselect("Filter by Status",
                                                st.session_state.leads['Status'].unique(),
                                                default=["New", "Contacted", "Quoted"])
            salesperson_filter = cols[1].multiselect("Filter by Salesperson",
                                                     st.session_state.leads['Salesperson'].unique())

            filtered_leads = st.session_state.leads
            if status_filter:
                filtered_leads = filtered_leads[filtered_leads['Status'].isin(status_filter)]
            if salesperson_filter:
                filtered_leads = filtered_leads[filtered_leads['Salesperson'].isin(salesperson_filter)]

            # Pipeline Visualization
            st.markdown('<p class="subheader">Pipeline Value by Status</p>', unsafe_allow_html=True)
            pipeline_value = filtered_leads.groupby('Status')['Value'].sum().reset_index()
            fig = px.bar(pipeline_value, x='Status', y='Value', text='Value',
                         color='Status', template='plotly_white')
            st.plotly_chart(fig, use_container_width=True)

            # Leads Table
            st.markdown('<p class="subheader">Leads</p>', unsafe_allow_html=True)
            st.dataframe(filtered_leads, use_container_width=True, hide_index=True)
        else:
            st.info("No leads data available")

    # Reporting Tab
    elif menu == "Reporting":
        st.markdown('<p class="app-header">Sales Reports</p>', unsafe_allow_html=True)

        if not st.session_state.leads.empty or not st.session_state.interactions.empty:
            cols = st.columns(3)
            with col1:
                st.markdown('<p class="subheader">Lead Conversion Rate</p>', unsafe_allow_html=True)
                total_leads = len(st.session_state.leads)
                if not st.session_state.leads.empty and 'Status' in st.session_state.leads.columns:
                    converted = len(st.session_state.leads[st.session_state.leads['Status'] == 'Converted'])
                else:
                    converted = 0
                conversion_rate = (converted / total_leads) * 100 if total_leads > 0 else 0
                st.metric("Conversion Rate", f"{conversion_rate:.1f}%")

            with col2:
                st.markdown('<p class="subheader">Active Leads</p>', unsafe_allow_html=True)
                if not st.session_state.leads.empty and 'Status' in st.session_state.leads.columns:
                    active_leads = len(st.session_state.leads[st.session_state.leads['Status'].isin(
                        ['New', 'Contacted', 'Quoted'])])
                else:
                    active_leads = 0
                st.metric("Active Leads", active_leads)

            with col3:
                st.markdown('<p class="subheader">Pipeline Value</p>', unsafe_allow_html=True)
                if not st.session_state.leads.empty and 'Value' in st.session_state.leads.columns:
                    total_value = st.session_state.leads['Value'].sum()
                else:
                    total_value = 0
                st.metric("Total Pipeline Value", f"${total_value:,.0f}")

            # Monthly Sales Trend
            st.markdown('<p class="subheader">Monthly Sales Trend</p>', unsafe_allow_html=True)
            if not st.session_state.leads.empty and 'FollowUp' in st.session_state.leads.columns:
                leads = st.session_state.leads.copy()
                leads['Month'] = pd.to_datetime(leads['FollowUp']).dt.to_period('M')
                monthly_sales = leads[leads['Status'] == 'Converted'].groupby('Month')['Value'].sum().reset_index()
                monthly_sales['Month'] = monthly_sales['Month'].dt.strftime('%Y-%m')

                if not monthly_sales.empty:
                    fig = px.line(monthly_sales, x='Month', y='Value', markers=True,
                                  title="Monthly Sales Value", template='plotly_white')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No converted leads for monthly trend")

            # Sales by Salesperson
            if 'Salesperson' in st.session_state.leads.columns and not st.session_state.leads.empty:
                st.markdown('<p class="subheader">Performance by Salesperson</p>', unsafe_allow_html=True)
                sales_by_person = st.session_state.leads[st.session_state.leads['Status'] == 'Converted'].groupby('Salesperson')['Value'].sum().reset_index()

                if not sales_by_person.empty:
                    fig = px.bar(sales_by_person, x='Salesperson', y='Value', text='Value',
                                 title="Sales Value by Salesperson", template='plotly_white')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for reporting")

    # Export Data Tab
    elif menu == "Export Data":
        st.markdown('<p class="app-header">Export Data</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p class="subheader">Export Customers</p>', unsafe_allow_html=True)
            if not st.session_state.customers.empty:
                csv = st.session_state.customers.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download as CSV",
                    csv,
                    "customers.csv",
                    "text/csv"
                )
            else:
                st.info("No customers to export")

        with col2:
            st.markdown('<p class="subheader">Export Leads</p>', unsafe_allow_html=True)
            if not st.session_state.leads.empty:
                csv = st.session_state.leads.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download as CSV",
                    csv,
                    "leads.csv",
                    "text/csv"
                )
            else:
                st.info("No leads to export")

        st.markdown('<p class="subheader">Export Interactions</p>', unsafe_allow_html=True)
        if not st.session_state.interactions.empty:
            csv = st.session_state.interactions.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download as CSV",
                csv,
                "interactions.csv",
                "text/csv"
            )
        else:
            st.info("No interactions to export")

# =====================
# PAGE ROUTING LOGIC
# =====================
def main():
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.authenticated and st.session_state.page == "app":
        app_page()
    else:
        st.warning("Unauthorized access. Redirecting to login...")
        st.session_state.page = "login"
        st.rerun()

if __name__ == "__main__":
    main()
