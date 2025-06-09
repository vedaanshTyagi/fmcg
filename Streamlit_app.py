pip install pyrebase4
import streamlit as st
import pandas as pd
import os
import pyrebase
from datetime import datetime

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
    page_title="FMCG CRM Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with enhanced form styling
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


# =====================
# FIREBASE AUTH FUNCTIONS
# =====================
def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # Check if email is verified
        user_info = auth.get_account_info(user['idToken'])
        if not user_info['users'][0]['emailVerified']:
            st.session_state.auth_message = {
                'type': 'error',
                'text': 'Please verify your email before logging in. Check your inbox for verification link.'
            }
            return False

        st.session_state.authenticated = True
        st.session_state.user = email
        st.session_state.page = "app"
        st.session_state.auth_message = {'type': 'success', 'text': 'Login successful!'}
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False


def signup_user(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        # Send verification email
        auth.send_email_verification(user['idToken'])
        st.session_state.auth_message = {
            'type': 'success',
            'text': 'Account created! Please check your email to verify your account.'
        }
        st.session_state.show_signup = False
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False


def reset_password(email):
    try:
        auth.send_password_reset_email(email)
        st.session_state.auth_message = {'type': 'success', 'text': 'Password reset email sent!'}
        st.session_state.show_password_reset = False
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False


# =====================
# ATTRACTIVE HOME PAGE
# =====================
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


# =====================
# ATTRACTIVE LOGIN PAGE
# =====================
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


# =====================
# APP PAGE
# =====================
def app_page():
    st.title("FMCG CRM Dashboard")
    st.success(f"Welcome, {st.session_state.user}!")

    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", "245", "↑ 12%")
    with col2:
        st.metric("Active Leads", "89", "↑ 8%")
    with col3:
        st.metric("Conversion Rate", "23%", "↑ 3%")
    with col4:
        st.metric("Monthly Revenue", "$189K", "↑ 15%")

    # Main content columns
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Recent Leads")
        # Sample leads data
        leads_data = pd.DataFrame({
            'Company': ['ABC Distributors', 'XYZ Retail', 'Global Foods', 'Premium Goods'],
            'Contact': ['John Smith', 'Sarah Johnson', 'Mike Thompson', 'Emily Davis'],
            'Value': ['$12,500', '$8,200', '$24,000', '$5,400'],
            'Status': ['Proposal Sent', 'Meeting Scheduled', 'Negotiation', 'New Lead'],
            'Follow-up': ['Tomorrow', 'In 2 days', 'Next week', 'Today']
        })
        st.dataframe(leads_data, hide_index=True)

    with col2:
        st.subheader("Upcoming Activities")
        # Sample activities
        activities = [
            {"title": "Call with ABC Distributors", "time": "10:00 AM"},
            {"title": "Product Demo - XYZ Retail", "time": "2:30 PM"},
            {"title": "Contract Review Meeting", "time": "Tomorrow, 11:00 AM"},
            {"title": "Quarterly Sales Review", "time": "Jun 15, 3:00 PM"}
        ]

        for activity in activities:
            with st.container(border=True):
                st.markdown(f"**{activity['title']}**")
                st.caption(f"⏰ {activity['time']}")

    # Add a logout button
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.page = "home"
        st.session_state.auth_message = {'type': None, 'text': None}
        st.rerun()


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
