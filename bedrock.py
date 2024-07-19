import boto3
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import BedrockChat
import streamlit as st
import os

from botocore.config import Config
retry_config = Config(
        region_name = 'us-east-1',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
)

def bedrock_chain():
    #ACCESS_KEY = st.secrets["ACCESS_KEY"]
    #SECRET_KEY = st.secrets["SECRET_KEY"]

    ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    SECRET_KEY = os.environ['AWS_SECRET_KEY']
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    
    bedrock_runtime = session.client("bedrock-runtime", config=retry_config)
       
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    model_kwargs =  { 
        "max_tokens": 2048,  # Claude-3 use “max_tokens” However Claud-2 requires “max_tokens_to_sample”.
        "temperature": 0.0,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman"],
    }
    model = BedrockChat(
        client=bedrock_runtime,
        model_id=model_id,
        model_kwargs=model_kwargs,
    )
    
    prompt_template = """System: TThe following is a video transcript. I want you to provide a comprehensive summary of this text and then list the key points. The entire summary should be around 400 word. 

    Current conversation:
    {history}

    User: {input}
    Bot:"""
    prompt = PromptTemplate(
        input_variables=["history", "input"], template=prompt_template
    )

    memory = ConversationBufferMemory(human_prefix="User", ai_prefix="Bot")
    conversation = ConversationChain(
        prompt=prompt,
        llm=model,
        verbose=True,
        memory=memory,
    )
    return conversation
