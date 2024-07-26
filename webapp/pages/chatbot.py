import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("mockingmonkey/MedGemma2")
    model = AutoModelForCausalLM.from_pretrained("mockingmonkey/MedGemma2")
    return tokenizer, model

tokenizer, model = load_model()

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []

    if "generated" not in st.session_state:
        st.session_state["generated"] = ["Hello! 👋 Feel free to ask me any questions about medical issues."]

    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey! 👋"]

    if "initial_query" not in st.session_state:
        st.session_state["initial_query"] = ""

def conversation_chat(query):
    input_ids = tokenizer.encode(query, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if '.' in response:
        last_period_index = response.rfind('.')
        response = response[:last_period_index + 1]

    st.session_state["history"].append((query, response))
    return response

def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_input("Ask the Medical Assistant:", placeholder="Ask your medical question here", key="input")
            submit_button = st.form_submit_button(label="Send")

            if submit_button and user_input:
                with st.spinner("Generating response..."):
                    output = conversation_chat(query=user_input)

                    if st.session_state["initial_query"] == "":
                        st.session_state["initial_query"] = user_input

                st.session_state["past"].append(user_input)
                st.session_state["generated"].append(output)

    if st.session_state["generated"]:
        with reply_container:
            for i in range(len(st.session_state["generated"])):
                st.write(f"**You:** {st.session_state['past'][i]}")
                st.write(f"**Assistant:** {st.session_state['generated'][i]}")

def show():
    initialize_session_state()
    st.title("👩‍⚕️ Medical ChatBot")
    st.sidebar.title("📂 Information")
    st.sidebar.info("This chatbot provides medical advice for simple queries. Please consult a professional for serious conditions.")

    display_chat_history()

    st.header("🔍 Compare with Google Search")
    google_query = st.text_input("Enter your query:", placeholder="Enter a query to search on Google", value=st.session_state["initial_query"])

    if st.button("Search"):
        if google_query:
            google_search_link = f"https://www.google.com/search?q={google_query.replace(' ', '+')}"
            st.markdown(f"[Compare with Google Search]({google_search_link})")
