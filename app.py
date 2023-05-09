import os
import openai
from flask import Flask, jsonify, render_template, request, session


app = Flask(__name__)
app.secret_key = os.urandom(24)

openai.api_base = os.environ['api_base']
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'
openai.api_key = os.environ['api_key']
deployment_name= os.environ['deployment_name']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    history = data["history"]

    messages = [{"role": msg["role"], "content": msg["content"]} for msg in history]

    response = openai.ChatCompletion.create(
        engine = deployment_name, 
        messages = messages
    )

    # Extract the generated AI message from the response
    ai_message = response.choices[0].message["content"].strip()

    # Return the AI message as a JSON response
    return jsonify(ai_message)

if __name__ == "__main__":
    app.run()
