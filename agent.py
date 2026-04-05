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
    action = None
    action_input = None

    # Case 1: Action: web_search("query")
    func_call_regex = re.compile(r'Action:\s*(\w+)\((.*)\)')
    
    # Case 2: Normal format
    action_regex = re.compile(r'^Action:\s*(.+)$', re.IGNORECASE)
    input_regex = re.compile(r'^Action input:\s*(.+)$', re.IGNORECASE)

    lines = message.split('\n')

    for line in lines:
        func_match = func_call_regex.search(line)
        if func_match:
            action = func_match.group(1)
            action_input = func_match.group(2).strip('"')
            return action, action_input

        action_match = action_regex.match(line)
        input_match = input_regex.match(line)

        if action_match:
            action = action_match.group(1)
        elif input_match:
            action_input = input_match.group(1)

    return action, action_input

def extract_answer(message):
    answer_regex = re.compile(r'^(Final Answer|Answer):\s*(.+)$', re.IGNORECASE)
    lines = message.split('\n')
    answer = None

    for line in lines:
        answer_match = answer_regex.match(line)
        if answer_match:
            answer = answer_match.group(2)

    return answer

def agent_query(user_input):
     agent= Agent()


     while True:
          response= agent.send_message(user_input)
          print(response)

          action, action_input= execute_action(response)
          print("Parsed:", action, action_input)
          if action:
               action = action.lower()

               result= known_actions[action](action_input)
               user_input= str(result)
          else:
               return extract_answer(response)
          
     return


if __name__=="__main__":
    result = agent_query("wwhat is the sum of temperatures in Berlin and Paris right now?")
    print("Final:", result)