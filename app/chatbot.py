import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# print(os.environ.get("GOOGLE_API_KEY"))
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack. give answer in 5 words only")
# print(response.text)
print(response.usage_metadata.total_token_count)