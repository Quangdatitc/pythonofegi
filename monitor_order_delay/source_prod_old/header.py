#header.py
import streamlit as st

def hide_header():
    hide_streamlit_style = """
                <style> 
                .stDeployButton {visibility:hidden;}
                .st-emotion-cache-4z1n4l {display:none;}
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    

    #メニューボタンhide
    st.markdown(hide_streamlit_style,unsafe_allow_html=True)