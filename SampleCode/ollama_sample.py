# OLLAMA allows for running LLMs on your local device. It offloads larger models to OLLAMA cloud.
# Look for possible model names available on https://ollama.com/search and select a model you would like to work with.
# Install Ollama by following steps from here: https://ollama.com/download
# Please note that larger the model, more inference time it will take. For our use case I am using the Ministral 3B model (which is 3.0GB)
# Get a model by making a ollama pull. Run this command in your terminal: ollama pull ministral-3

# Import these models and functions from Ollama
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='ministral-3:3b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)