import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY tidak ditemukan di file .env")


# Create OpenAI client
client = OpenAI(api_key=api_key)


# Send a simple request
response = client.responses.create(
    model="gpt-6-luna",
    input="Say hello and explain what an AI agent is in one sentence. Gunakan bahasa indonesia yah "
)


# Display response
print(response.output_text)