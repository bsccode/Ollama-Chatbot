from openai import OpenAI
import json
import os

client = OpenAI(
    base_url = 'http://10.0.0.32:11434/v1',
    api_key='ollama', # required, but unused
)

context_read = open("context.txt", "r")
context = context_read.read()
context_read.close()

#f = open('history.json',"r")

#history = json.load(f)

class ChatHistoryManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_chat_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def save_chat_history(self, history):
        with open(self.file_path, 'w') as file:
            json.dump(history, file, indent=4)

history_manager = ChatHistoryManager("chat_history.json")  # Initialize ChatHistoryManager
chat_history = history_manager.load_chat_history()  # Load chat history


initial_response = client.chat.completions.create(
  model="llama2",
  messages=[
    {"role": "system", "content": context},
  ]
)

print("\nContext: " + context)
assistant_message = initial_response.choices[0].message.content
print("\nAI: " + assistant_message)

question = input("\nYou: ")

while True:
  response = client.chat.completions.create(
  model="llama2",
  messages=[
    {"role": "user", "content": question},
    {"role": "assistant", "content": question},
  ]
)
  assistant_message = response.choices[0].message.content
  print("\nAI: " + assistant_message)
  question = input("\nYou: ")

  # Update the chat history
  chat_history.append({"role": "assistant", "content": assistant_message})
  chat_history.append({"role": "user", "content": question})

        # Save the updated chat history
  history_manager.save_chat_history(chat_history)