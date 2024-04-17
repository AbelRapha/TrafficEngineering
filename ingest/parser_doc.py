import google.generativeai as genai
import os
import glob
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=api_key)

filepath = 'ingest/docs/pages-to-jpg/'  # Replace with the path of your file
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

model = genai.GenerativeModel('gemini-pro-vision', safety_settings=safety_settings)
question = """Describe to me all text information in this image in markdown format"""

list_text_to_input_doc = list()

list_name_images = os.listdir(filepath)
list_name_images = sorted(list_name_images)

for image_file in list_name_images:
    print(image_file)
    img = Image.open(f'{filepath}/{image_file}')
    response = model.generate_content([img, question])
    list_text_to_input_doc.append(response.text)


with open('ingest/docs/doc.md', 'w') as f:
    f.write('\n'.join(list_text_to_input_doc))
    f.close()