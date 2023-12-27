from flask import Flask, render_template, request
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv() 
import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


app = Flask(__name__)

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.read()

        image_parts = [
            {
                "mime_type": uploaded_file.mimetype,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input = request.form['input']
        uploaded_file = request.files['image']
        image = Image.open(uploaded_file)

        input_prompt = """
                   You are an expert in understanding invoices.
                   You will receive input images as invoices &
                   you will have to answer questions based on the input image
                   """

        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input)

        return render_template('index.html', input=input, image=image, response=response)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()