import re

from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import web_search, calculator


class Agent:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_msg = "you are a helpful assistant."
        self.messages=[]
        self.messages.append({"role": "system", "content": self.system_msg})    
    
    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create( model="gpt-4o", messages=self.messages )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    

if __name__=="__main__":
        agent = Agent()
        message= "what is the latest AI news in 2026?"
        response=agent.send_message(message)
        print(response)