import streamlit as st
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import io

@st.cache_resource
def load_gemma_model():
    model_id = "mockingmonkey/MedGemma"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return model, tokenizer

def model_predict(model, tokenizer, input_text):
    try:
        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        outputs = model.generate(input_ids, max_new_tokens=300)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if '.' in response:
            last_period_index = response.rfind('.')
            response = response[:last_period_index + 1]
        
        return response
    
    except Exception as e:
        st.error(f"Error during model prediction: {e}")
        return ""

def format_prompt_from_csv(df):
    # Assuming the CSV columns match the form fields
    prompts = []
    for _, row in df.iterrows():
        prompt = (
            f"Age: {row['Age']}\n"
            f"Gender: {row['Gender']}\n"
            f"Primary Symptom: {row['Symptom']}\n"
            f"Symptom Duration: {row['Duration']}\n"
            f"Symptom Severity: {row['Severity']}\n"
            f"Past Surgeries: {row['Past Surgeries']}\n"
            f"Current Medications: {row['Current Medications']}\n"
            f"Allergies: {row['Allergies']}\n"
            "Based on this information, provide medical recommendations and suggest next steps for the patient's care."
        )
        prompts.append(prompt)
    return prompts

def show():
    st.markdown("""
    **Welcome to the Medical Recommendations Assistant!**

    This tool allows you to:
    1. Upload a patient's medical records (CSV format) or complete the form with patient information.
    2. Receive AI-generated medical recommendations.
    
    Please follow the steps below to use the tool.
    """)

    st.title("Medical Recommendations Assistant")

    # Provide a CSV template for users to download
    st.markdown("### Download CSV Template")
    csv_template = pd.DataFrame({
        'Age': [35],
        'Gender': ['Male'],
        'Symptom': ['Headache'],
        'Duration': ['3 days'],
        'Severity': ['Mild'],
        'Past Surgeries': ['None'],
        'Current Medications': ['None'],
        'Allergies': ['Penicillin']
    })

    csv_buffer = io.StringIO()
    csv_template.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download CSV Template",
        data=csv_buffer.getvalue(),
        file_name="patient_records_template.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader("Upload patient records (CSV)", type="csv")

    with st.form("patient_form"):
        st.header("Patient Information")
        age = st.number_input("Age", min_value=0, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        st.header("Symptoms")
        primary_symptom = st.text_input("Primary Symptom")
        duration = st.text_input("Duration")
        severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe"])
        
        st.header("Medical History")
        past_surgeries = st.text_area("Past Surgeries")
        medications = st.text_area("Current Medications")
        allergies = st.text_input("Allergies")
        
        submit_button = st.form_submit_button(label="Get Recommendations")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded patient records:")
        st.write(df)
        
        input_texts = format_prompt_from_csv(df)

        with st.spinner("Loading GEMMA model... This may take a few minutes."):
            model, tokenizer = load_gemma_model()

        for input_text in input_texts:
            with st.spinner('Generating recommendations...'):
                first_output = model_predict(model, tokenizer, input_text)
                st.subheader("GEMMA Model Recommendations")
                st.write(first_output)

        st.subheader("Disclaimer")
        st.write("These recommendations are generated by an AI model based on the provided patient information. They should be reviewed by a qualified healthcare professional before making any medical decisions.")

    if submit_button:
        if not primary_symptom and not medications:
            st.error("Please fill in the required fields.")
        else:
            input_text = (
                f"Age: {age}\n"
                f"Gender: {gender}\n"
                f"Primary Symptom: {primary_symptom}\n"
                f"Symptom Duration: {duration}\n"
                f"Symptom Severity: {severity}\n"
                f"Past Surgeries: {past_surgeries}\n"
                f"Current Medications: {medications}\n"
                f"Allergies: {allergies}\n"
                "Based on this information, provide medical recommendations and suggest next steps for the patient's care."
            )

            with st.spinner("Loading GEMMA model... This may take a few minutes."):
                model, tokenizer = load_gemma_model()

            with st.spinner('Generating recommendations...'):
                first_output = model_predict(model, tokenizer, input_text)
                st.subheader("GEMMA Model Recommendations")
                st.write(first_output)

            st.subheader("Disclaimer")
            st.write("These recommendations are generated by an AI model based on the provided patient information. They should be reviewed by a qualified healthcare professional before making any medical decisions.")

if __name__ == "__main__":
    show()
