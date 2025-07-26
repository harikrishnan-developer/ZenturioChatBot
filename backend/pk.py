import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyAgqCqG7Par8LMorgSgJMiB2ABV-13Vrzk"))

for model in genai.list_models():
   print(model.name)