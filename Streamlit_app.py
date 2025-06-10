import streamlit as st
import pandas as pd
import datetime
import pyrebase
from io import BytesIO
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize Google Sheets client
def init_gsheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        # Load credentials from Streamlit secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Google Sheets initialization failed: {str(e)}")
        return None

# Load data from Google Sheet
def load_sheet_data(sheet_name):
    try:
        client = init_gsheets()
        spreadsheet = client.open(st.secrets["gsheets"]["spreadsheet_name"])
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
        spreadsheet = client.open(st.secrets["gsheets"]["spreadsheet_name"])
        worksheet = spreadsheet.worksheet(sheet_name)
        
        # Clear existing data and update with new
        worksheet.clear()
        worksheet.append_row(df.columns.tolist())  # Add headers
        for _, row in df.iterrows():
            worksheet.append_row(row.tolist())
        return True
    except Exception as e:
        st.error(f"Error saving {sheet_name} data: {str(e)}")
        return False

# Firebase Configuration (existing code remains the same)
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

# ... (existing CSS and styling remains the same) ...

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.auth_message = {'type': None, 'text': None}
    st.session_state.show_password_reset = False
    st.session_state.show_signup = False
    st.session_state.edit_customer = None
    
    # Initialize empty DataFrames (will be loaded from Google Sheets after login)
    st.session_state.customers = pd.DataFrame(columns=[
        'Name', 'Contact', 'Email', 'Address', 'Company', 'Category'
    ])
    st.session_state.leads = pd.DataFrame(columns=[
        'Customer', 'Status', 'Value', 'Salesperson', 'Notes', 'FollowUp'
    ])
    st.session_state.interactions = pd.DataFrame(columns=[
        'Customer', 'Type', 'Date', 'Notes'
    ])

# =====================
# MODIFIED AUTH FUNCTIONS
# =====================
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
            st.session_state.customers = load_sheet_data("Customers")
            st.session_state.leads = load_sheet_data("Leads")
            st.session_state.interactions = load_sheet_data("Interactions")
            st.session_state.auth_message = {'type': 'success', 'text': 'Login successful! Data loaded.'}
        except Exception as e:
            st.session_state.auth_message = {'type': 'error', 'text': f'Data load error: {str(e)}'}
            
        st.session_state.page = "app"
        return True
    except Exception as e:
        error_message = str(e).split('] ')[-1]
        st.session_state.auth_message = {'type': 'error', 'text': error_message}
        return False

# ... (existing home_page, login_page, etc. functions remain the same) ...

# =====================
# MODIFIED APP PAGE FUNCTIONS
# =====================
def app_page():
    # ... (existing sidebar and menu code) ...
    
    # Customer Management Tab
    if menu == "Customer Management":
        st.markdown('<p class="app-header">Customer Management</p>', unsafe_allow_html=True)
        
        with st.expander("Add New Customer", expanded=True):
            with st.form("customer_form"):
                # ... (existing form fields) ...
                
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
        
        # ... (existing customer management code) ...
        
        # In Edit/Delete sections - add save_sheet_data() after modifications
        if cols[1].button("Delete Customer"):
            st.session_state.customers = st.session_state.customers[
                st.session_state.customers['Name'] != selected_customer
            ]
            if save_sheet_data("Customers", st.session_state.customers):
                st.success("Customer deleted and updated in cloud!")
            else:
                st.error("Deletion saved locally but cloud update failed")
            st.rerun()
        
        if 'edit_customer' in st.session_state:
            # ... (existing edit form) ...
            if st.form_submit_button("Update Customer"):
                # ... (existing update logic) ...
                if save_sheet_data("Customers", st.session_state.customers):
                    st.success("Customer updated in cloud!")
                else:
                    st.error("Update saved locally but cloud update failed")
                del st.session_state.edit_customer
                st.rerun()
    
    # Lead Tracking Tab
    elif menu == "Lead Tracking":
        # ... (existing lead form) ...
        if st.form_submit_button("Save Lead"):
            if customer:
                # ... (existing lead creation) ...
                if save_sheet_data("Leads", st.session_state.leads):
                    st.success("Lead saved to cloud!")
                else:
                    st.error("Lead saved locally but cloud save failed")
        
    # Interaction Logs Tab
    elif menu == "Interaction Logs":
        # ... (existing interaction form) ...
        if st.form_submit_button("Log Interaction"):
            if customer and notes:
                # ... (existing interaction creation) ...
                if save_sheet_data("Interactions", st.session_state.interactions):
                    st.success("Interaction saved to cloud!")
                else:
                    st.error("Interaction saved locally but cloud save failed")
    
    # ... (other tabs remain the same) ...

# ... (rest of the code remains the same) ...
