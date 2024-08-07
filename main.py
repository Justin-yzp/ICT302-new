import streamlit as st
from auth.login import login
from pages_app.rag import rag
from pages_app.register import register
from utils.calendar_dashboard import Calendar
from pages_app.style import apply_custom_styles, set_background_image
from pages_app.welcome import welcome
from pages_app.about import about

# Apply custom styles
apply_custom_styles()

# Set background image
set_background_image("https://raw.githubusercontent.com/Justin-yzp/ICT302-new/main/images/background.jpg")

# Initialize session state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state['page'] = 'welcome'

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

# Logout function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['page'] = 'welcome'
    st.session_state['is_admin'] = False

# Function to display the appropriate page based on session state
def display_page():
    pages = {
        'welcome': welcome,
        'login': login,
        'dashboard': lambda: display_calendar('users.db'),
        'rag': rag,
        'register': register,
        'about': about
    }
    page_function = pages.get(st.session_state['page'])
    if page_function:
        if st.session_state['page'] == 'register' and not st.session_state['is_admin']:
            st.error("You do not have permission to access this page.")
        else:
            page_function()

# Function to display calendar page
def display_calendar(db_path):
    cal = Calendar(db_path)
    cal.display_calendar()

# User guide for each page
user_guides = {
    'welcome': "Welcome to our application! Navigate through the sidebar to explore different features.",
    'login': "Please enter your username and password to log in. If you don't have an account, contact an admin.",
    'dashboard': "View and manage your calendar events here. You can add, edit, or delete events as needed.",
    'rag': "Use this feature to chat with and query your documents. Upload files and ask questions to get relevant information.",
    'about': "Learn more about our application, its features, and how to use it effectively.",
    'register': "Admin only: Use this panel to register new users and manage user accounts."
}

# Sidebar navigation items
sidebar_items_logged_out = {
    '🏠 Welcome': 'welcome',
    '🔒 Login': 'login',
    '📘 About': 'about'
}

sidebar_items_logged_in = {
    '🏠 Welcome': 'welcome',
    '📅 Dashboard': 'dashboard',
    '🔍 Chat with documents': 'rag',
    '📘 About': 'about'
}

# Add Register option only for admin users
if st.session_state['is_admin']:
    sidebar_items_logged_in['📝 Admin Panel'] = 'register'

sidebar_items = sidebar_items_logged_out if not st.session_state['logged_in'] else sidebar_items_logged_in

# Display sidebar for navigation with emojis
selected_page = st.sidebar.radio("Navigation", list(sidebar_items.keys()))

# Update session state based on selected page
st.session_state['page'] = sidebar_items[selected_page]

# Display user guide for the current page
st.sidebar.markdown("---")
st.sidebar.subheader("User Guide")
st.sidebar.write(user_guides[st.session_state['page']])

# Display the appropriate page
if st.session_state['logged_in']:
    st.sidebar.write(f"Logged in as {st.session_state['username']}")  # Display login status in the sidebar
    if st.session_state['is_admin']:
        st.sidebar.write("(Admin)")
else:
    st.sidebar.write("Not Logged in")

display_page()

# Add logout button at the bottom of the sidebar
if st.session_state['logged_in']:
    st.sidebar.markdown('---')
    if st.sidebar.button("Logout", key="logout_btn"):
        logout()
        st.rerun()