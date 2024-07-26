import streamlit as st
from PIL import Image
from transformers import PaliGemmaForConditionalGeneration, AutoProcessor
import torch

@st.cache_resource
def load_model():
    model_id = "mockingmonkey/MedPali"
    model = PaliGemmaForConditionalGeneration.from_pretrained(model_id)
    processor = AutoProcessor.from_pretrained(model_id)
    return model, processor

model, processor = load_model()

def model_predict(image, prompt):
    try:
        if image.mode != "RGB":
            image = image.convert("RGB")

        model_inputs = processor(text=prompt, images=image, return_tensors="pt")
        input_len = model_inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
            generation = generation[0][input_len:]
            decoded = processor.decode(generation, skip_special_tokens=True)

        return decoded
    except Exception as e:
        st.error(f"Error during model prediction: {e}")
        return ""

def show():
    st.title("MedPali - Medical Image Analysis")

    st.markdown("""
    **Welcome to MedPali!**

    This AI Assistant allows you to upload medical images for analysis. Follow these steps to use the tool:
    
    1. Click on the "Choose an image..." button below to upload a medical image.
    2. Ensure the image is in JPG, JPEG, or PNG format.
    3. After uploading, the image will be displayed below.
    4. Type your prompt in the text box. For a quick description, try "caption en"!
    5. The analysis results will be shown below the prompt.
    6. You can ask further questions about the same image.
    """)

    # Apply custom CSS for input boxes
    st.markdown(
        """
        <style>
        .stTextInput > div > input {
            border: 2px solid black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "image" not in st.session_state:
        st.session_state.image = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.session_state.image = Image.open(uploaded_file)
        st.image(st.session_state.image, caption='Uploaded Image.', use_column_width=True)
    
    if st.session_state.image is not None:
        prompt = st.text_input("Enter your prompt", "")

        if st.button("Analyze"):
            if not prompt:
                st.warning("Please enter a prompt before analyzing.")
            else:
                with st.spinner('MedPali is analyzing the image for you...'):
                    prediction = model_predict(st.session_state.image, prompt)
                    st.session_state.conversation.append((prompt, prediction))
                    st.experimental_rerun()

        if st.session_state.conversation:
            st.markdown("## Conversation")
            for i, (user_input, response) in enumerate(st.session_state.conversation):
                st.markdown(f"**User:** {user_input}")
                st.markdown(f"**MedPali:** {response}")

        prompt = st.text_input("Ask another question about the same image", "")

        if st.button("Ask"):
            if not prompt:
                st.warning("Please enter a prompt before asking.")
            else:
                with st.spinner('MedPali is analyzing the image for you...'):
                    prediction = model_predict(st.session_state.image, prompt)
                    st.session_state.conversation.append((prompt, prediction))
                    st.experimental_rerun()

if __name__ == "__main__":
    show()
