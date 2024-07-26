import streamlit as st
from pages import home, medpali, contact, chatbot, medreco, dashboard, segmentation

pages = {
    "Home": home,
    "Discussion": chatbot,
    "MedPali": medpali,
    "Recommendation": medreco,
    "Detection": segmentation,
    "Dashboard": dashboard,
    "Contact": contact
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", options=list(pages.keys()))

if page in pages:
    pages[page].show()
