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

<img width="983" alt="chatbot" src="https://github.com/user-attachments/assets/fddc669a-628f-4298-aa26-d48e7f8f0f17">

And then AI will reply to you:

<img width="983" alt="chatbot" src="https://github.com/user-attachments/assets/49817e44-c2b9-4b13-b5b3-79b941c30cc9">

Finally, you can also compare the answer you got with a Google search:

<img width="983" alt="search" src="https://github.com/user-attachments/assets/3824c50a-8975-4674-ab27-17adf2be13d2">

### 2. MedPali

MedPali is an AI model capable to comprehend medical images and answer questions you may have regarding that image. 

MedPali is easy and straight forward to use:

<img width="983" alt="medpali_intro" src="https://github.com/user-attachments/assets/34b7bb49-d2f0-443c-b451-30f1ab52e7db">

You can prompt the model by following the below template:
- For a quick description of the image, ask the model for "caption en".
- Or simply ask a straight to the point question of your choice.

<img width="983" alt="medpali_prompt" src="https://github.com/user-attachments/assets/36e363b8-cf7e-43e3-a9fa-1797212fb06e">

If you wish to get more information, you can prompt again the model:

<img width="983" alt="medpali_conv" src="https://github.com/user-attachments/assets/f553cf3f-5bd4-484f-ad06-e63015f3bc9f">


### 3. Medical Recommendations

ANIMA is also capable of providing recommendations using medical record from your patient. 

You can either fill in the form or upload your own csv:

<img width="983" alt="reco_form" src="https://github.com/user-attachments/assets/6c7dab6b-1a83-4c39-bcb9-460bf54110d3">

This will output informations alongside recommendations:

<img width="983" alt="reco_answer" src="https://github.com/user-attachments/assets/54bf426f-1dd1-4787-b585-f0b1a111ea59">

### 4. Image Segmentation

On this page, you can upload any medical image. Best performances are observed with MRI scans. 

Model will return all objects detected on the image:

<img width="367" alt="segmentation" src="https://github.com/user-attachments/assets/4bac6fea-e87c-450f-b2f4-325013f153ec">
