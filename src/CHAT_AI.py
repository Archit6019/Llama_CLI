from groq import Groq
from typing import List, Any
from pydantic import BaseModel, Field
from ast import literal_eval
import instructor
import argparse
from transformers import AutoTokenizer

COUNT = 0
TOKENS = 0
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")

# class LLMOutput(BaseModel):
#     llm_response : str = Field(..., description="AI Response")

def summarizer(text : str, api_key : str):
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            model='llama3-70b-8192',
            messages = [
                {"role" : "system","content" : "You are a helpful assistant that summarizes conversations between a user and an intelligent ai"},
                {"role" : "user", "content" : text}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Error", e)

def ask_ai(context : List, api_key : str):
    global COUNT
    global TOKENS
    
    context.append({
        "role" : "user",
        "content" : input("User:  \n")
    })
    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            model='llama3-70b-8192',
            messages= [
                {
                    "role" : "system",
                    "content" : "You are a helpful assistant, you will be provided with conversation history so that you can have conversations with the user."
                },
                {
                    "role" : "user",
                    "content" : f"{context}"
                }
            ]
        )
        response =  chat_completion.choices[0].message.content
        context.append({
                    "role" : "assistant",
                    "content" : response,
                })
        COUNT += 1
        if COUNT == 10:
            TOKENS += len(tokenizer.encode(str(context)))
            COUNT = 0

        if TOKENS >= 6000:
            summary = summarizer(str(context) , api_key)
            TOKENS = 0
            context = [{
                "role" : "Past_Conversation_Summary",
                "content" : summary
            }]
        
        print("Tokens :", TOKENS)
        print("Message Count :", COUNT)
        return response
    
    except Exception as e:
        print("Error", e)