# -*- coding: utf-8 -*-
"""Gen AI using LLAMA and HF.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1teka1ZjB9c1AYCLyMnWzy7pJKlcQNQNq

The provided libraries are essential for different aspects of the code you're planning to run:

1. **langchain-huggingface**:
   - This library seems to be a specific package that integrates Hugging Face models with LangChain. It likely provides functionalities and classes to interact with Hugging Face models within the LangChain framework.

2. **huggingface_hub**:
   - This library is used to interact with the Hugging Face Model Hub, a repository of pre-trained models for natural language processing and other tasks. It's commonly used to download, upload, and manage models from Hugging Face.

3. **transformers**:
   - Transformers is a popular library provided by Hugging Face that offers a wide range of pre-trained models for natural language processing tasks like text generation, text classification, question answering, and more. It provides an easy-to-use interface for working with these models.

4. **accelerate**:
   - Accelerate is a library for high-performance deep learning research and development. It's typically used for distributed training, enabling you to train models faster by leveraging multiple GPUs or TPUs.

5. **bitsandbytes**:
   - The purpose of this library is not immediately clear from its name, and it doesn't seem to be a widely known or commonly used library. It's possible that it provides utilities or functionalities related to handling binary data or low-level operations, but without further context, it's challenging to ascertain its exact purpose.

6. **langchain**:
   - LangChain is likely a library or framework for natural language processing tasks. It seems to offer functionalities tailored to language processing pipelines, which may include data preprocessing, model integration, and result interpretation. The exact purpose would depend on its documentation and implementation details.
"""

## Libraries Required
!pip install langchain-huggingface
## For API Calls
!pip install huggingface_hub
!pip install transformers
!pip install accelerate
!pip install  bitsandbytes
!pip install langchain

from langchain_huggingface import HuggingFaceEndpoint

from google.colab import userdata
sec_key=userdata.get("HUGGINGFACEHUB_API_TOKEN")

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key

repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,token=sec_key)

from langchain import PromptTemplate, LLMChain


# Define the prompt template
question = input("Enter your question: ")
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Initialize the LLMChain with your LLM and the prompt template

llm_chain = LLMChain(llm=llm, prompt=prompt)

response_dict = llm_chain.invoke({"question": question})

# Extract the text from the response
response = response_dict['text']

# Split the response into sentences and print each sentence on a new line
for sentence in response.split('. '):
    print(sentence.strip() + '.')

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_id="gpt2"
model=AutoModelForCausalLM.from_pretrained(model_id)
tokenizer=AutoTokenizer.from_pretrained(model_id)

pipe=pipeline("text-generation",model=model,tokenizer=tokenizer,max_new_tokens=100)
hf=HuggingFacePipeline(pipeline=pipe)

hf

## Use HuggingfacePipelines With Gpu
gpu_llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    device=-1,  # replace with device_map="auto" to use the accelerate library.
    pipeline_kwargs={"max_new_tokens": 100},
)

from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

chain=prompt|gpu_llm

question=input("Enter your question: ")
chain.invoke({"question":question})