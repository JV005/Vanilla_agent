import re

from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import web_search, calculator


class Agent:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_msg = open("system_prompt.txt").read()
        self.messages=[]
        self.messages.append({"role": "system", "content": self.system_msg})    
    
    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content
    
known_actions = {
    "web_search": web_search,
    "calculator": calculator
}

def execute_action(message):
     #match either "Action: <action>" or "Action input: <input>"
     action_regex= re.compile('^Action: (.+)$')
     input_regex= re.compile('^Action input: (.+)$')

     lines = message.split('\n')
     action= None
     action_input= None

     for line in lines:
          action_match = action_regex.match(line)
          input_match= input_regex.match(line)

          if action_match:
               action= action_match.group(1)
          elif input_match:
               action_input= input_match.group(1)

     return action, action_input

def extract_answer(message):
     answer_regex= re.compile('^Answer: (.+)$')
     lines = message.split('\n')
     answer= None
     for line in lines:
          answer_match = answer_regex.match(line)
          if answer_match:
               answer= answer_match.group(1)
               
     return answer


if __name__=="__main__":
        agent = Agent()
        message= "what is the latest AI news in 2026?"
        response=agent.send_message(message)
        print(response)