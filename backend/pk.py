import google.generativeai as genai

genai.configure(api_key="AIzaSyAgqCqG7Par8LMorgSgJMiB2ABV-13Vrzk")

 for model in genai.list_models():
    print(model.name)