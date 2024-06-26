# pages_app/style.py

import streamlit as st


def apply_custom_styles():
    # Custom CSS
    st.markdown("""
        <style>
        .custom-title {
            font-size: 24px;
            color: #ff6347;
            text-align: center;
        }
        .custom-button {
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .custom-container {
            background-color: #f2f2f2;
            padding: 20px;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Background image
    page_bg_img = '''
    <style>
    body {
        background-image: url("https://raw.githubusercontent.com/Justin-yzp/ICT302-new/main/elements/background.jpg");
        background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
