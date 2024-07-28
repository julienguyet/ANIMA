# Enhancing Healthcare Solutions with AI :woman_health_worker: :man_health_worker:

---

## Introduction :open_book:

**ANIMA** is a powered AI application tailored to a medical usage. It has LLAMA3 and PaliGemma at its core, and both models were fine-tuned on medical datasets. 

To use this application, you can follow the below steps:

1. Clone the repository on your machine.
2. Install all requirements with:

```bash
pip install -r requirements.txt
```

3. In your terminal, at the root of the directory run in order:

```bash
cd webapp
streamlit run app.py
```

<img width="983" alt="anima_home" src="https://github.com/user-attachments/assets/3e166979-9fb1-4659-b887-8ab94469e951">


4. The application will open in your browser, feel free to explore and to use either the chat or the image assistant. 

Note: 
- if you would like to reproduce fine-tuning of the models, feel free to reach out and we will share the code on request.
- by default the application runs with MedGemma, a light fine-tuned Gemma model that can run on CPU. 
- If you possess a powerful set up, you can edit the model in Discussion and Recommendations python scripts with:
```python
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM

config = PeftConfig.from_pretrained("mockingmonkey/MedLLAMA")
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
model = PeftModel.from_pretrained(base_model, "mockingmonkey/MedLLAMA")
```

---

## How can ANIMA help me as a student or professional? :robot:

ANIMA has been designed to solve medical query. A few options are available to you:

### 1. Discussion

Discussion is our AI chatbot where you get answers to any question you might have. Simply enter your question like below:

<img width="983" alt="chatbot" src="https://github.com/user-attachments/assets/25d31947-745f-46f9-a564-9cdf55dee886">

A Google Search link is also available at the bottom of the page if you would like to cross validate results.

### 2. MedPali

MedPali is an AI model capable to comprehend medical images and answer questions you may have regarding that image. 

MedPali is easy and straight forward to use. You can prompt the model by following the below template:
- For a quick description of the image, ask the model for "caption en".
- Or simply ask a straight to the point question of your choice.

<img width="983" alt="[medpali_prompt" src="https://github.com/user-attachments/assets/fc62cd2e-6e40-42eb-bb7b-58ee2d8b639a">

### 3. Medical Recommendations

ANIMA is also capable of providing recommendations using medical record from your patient. 

You can either fill in the form or upload your own csv:

<img width="983" alt="reco_form" src="https://github.com/user-attachments/assets/0a3098c8-c69b-4999-9126-aa1f1e3c7b2d">

This will output informations alongside recommendations:

<img width="983" alt="reco_answer" src="https://github.com/user-attachments/assets/52d83c03-15e9-46d6-b304-c5a65e737080">

### 4. Image Segmentation

On this page, you can upload any medical image. Best performances are observed with MRI scans. 

Model will return all objects detected on the image:

<img width="367" alt="segmentation" src="https://github.com/user-attachments/assets/fc7ed936-2b22-4897-8cb5-dc73ed8a5c65">

<img width="367" alt="segmentation_label" src="https://github.com/user-attachments/assets/302fb32b-85dc-4f4a-9119-8580dbfe5e47">
