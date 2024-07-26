import streamlit as st
from PIL import Image
import os

def show():
    st.title("Welcome to Anima.org")

    # Introduction
    st.markdown("""
    **ANIMA - AI Powered Medical Solutions**

    Welcome to ANIMA. Our ambition is to enhance decision-making in the healthcare industry. Our tools allows you to get insightful analysis powered by AI.

    ### Features:
    - **Discussion**: An AI chatbot to answer your medical queries and help you with diagnosis or prevention strategies.
    - **MedPali**: Upload your image, enter a custom prompt, and get instant analysis results from the AI.
    - **Dashboard**: Review AI analysis and add your comments, or even edit AI results if necessary. 

    ### How to Use:
    1. Navigate to the desired section from the sidebar.
    2. Enter a prompt for analysis.
    3. View the results.

    Feel free to explore and make use of the features offered by ANIMA!
    """)

    local_image_path = os.path.join(os.path.dirname(__file__), "../images/random_doctor_image.jpg")
    image = Image.open(local_image_path)
    st.image(image, caption="ANIMA, your AI Assistant", use_column_width=True)

    st.markdown("""
    If you have any questions or feedback, please reach out to us using the contact form.
    """)

if __name__ == "__main__":
    show()