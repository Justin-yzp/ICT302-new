import streamlit as st

def welcome():
    st.markdown('<h1 class="title">University Document Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">Your Intelligent Guide for University Documents</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="content card">
        <p>Welcome to the University Document Assistant! Our AI-driven system simplifies your document management:</p>
        <ul>
            <li>Get quick answers to your questions</li>
            <li>Navigate complex university documents effortlessly</li>
            <li>Download source PDFs directly</li>
            <li>Stay organized with an interactive calendar</li>
        </ul>
        <p>Log in to access all features and start your efficient document journey!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Go to Login"):
            st.session_state['page'] = 'login'
            st.rerun()
    with col2:
        if st.button("About"):
            st.session_state['page'] = 'about'
            st.rerun()

if __name__ == "__main__":
    welcome()
