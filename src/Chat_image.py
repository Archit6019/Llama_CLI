from openai import OpenAI 
from typing import List, Any
from colorama import Fore , Style
import time
import base64

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

class Image_chat:
    def __init__(self, api_key : str, image_url : str):
        self.api_key = api_key
        self.image_url = image_url
        if self.image_url.startswith("http"):
            image_url = image_url
        else:
            encoded_image = encode_image(self.image_url)
            self.image_url = f"data:image/jpeg;base64,{encoded_image}"
        self.client = None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            print("OPENAI_API_KEY environment variable not found.") 

    def chat_with_image(self, query : str):
        t0 = time.time()
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                        {
                        "role": "user",
                        "content": [
                            {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{self.image_url}"
                            }
                            },
                            {
                            "type": "text",
                            "text": f"{query}"
                            }
                        ]
                        }
                    ],
                    max_tokens=500
        )
        print("Message Generated")
        response_str = response.choices[0].message.content
        t1 = time.time()
        print(f"Elapsed time for AI Response:  {t1 - t0} seconds")
        return response_str
    