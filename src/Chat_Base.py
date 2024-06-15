from groq import Groq 
from typing import List, Any 
from pydantic import BaseModel, Field
import instructor
import os
import time
from colorama import Fore, Style
from transformers import AutoTokenizer

#Colors 
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

# Tokenizer 
COUNT = 0
TOKENS = 0
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")

class ChatBase:
    def __init__(self, api_key : str):
        self.api_key = api_key
        self.summarizer_client = None 
        self.chat_client = None 
        if self.api_key:
            self.summarizer_client = Groq(api_key=self.api_key)
            self.chat_client = Groq(api_key=self.api_key)
        else:
            print("GROQ_API_KEY environment variable not found.")            

    def summarizer(self, text : str):
        try:
            chat_completion = self.summarizer_client.chat.completions.create(
                model="llama3-70b-8192",
                messages= [
                    {"role" : "system", "content" : "You are an helpful assistant that summarizes conversations between a user and an intelligent ai"},
                    {"role" : "user", "content" : text}                    
                ]
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print("Error: ", e)

    def chat(self, context : List):
        global COUNT
        global TOKENS

        user_input = input(Fore.BLUE + "User: " + Style.RESET_ALL)

        context.append({
            "role" : "user",
            "content" : user_input
        })
        try:
            chat_completion = self.chat_client.chat.completions.create(
                model="llama3-70b-8192",
                messages= [
                    {
                        "role" : "user",
                        "content" : "You are a helpful assistant, you will be provided with conversation history so that you can have conversations with the user"
                    },
                    {
                        "role" : "user",
                        "content" : f"Conversation History {context}"
                    }
                ]
            )
            t0 = time.time()
            response = chat_completion.choices[0].message.content
            t1 = time.time()
            context.append({
                "role" : "assistant",
                "content" : response,
            })
            COUNT += 1 
            if COUNT == 10:
                TOKENS += len(tokenizer.encode(str(context)))
                COUNT = 0

            if TOKENS >= 8000:
                summary = self.summarizer(str(context))
                TOKENS = 0
                context = [
                    {
                        "role" : "Past_Conversation_Summary",
                        "content" : summary
                    }
                ]
            
            print("Tokens :", TOKENS)
            print("Message Count :", COUNT)
            print("Elapsed Time", t1 - t0)
            return response
        
        except Exception as e:
            print("Error", e)

    
            
        