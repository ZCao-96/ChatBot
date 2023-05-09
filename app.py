import os
import openai
from flask import Flask, jsonify, render_template, request, session
import json


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Opening JSON file
f = open('local.settings.json')

# returns JSON object as
# a dictionary
data = json.load(f)
openai.api_base = data["API_Base"]
openai.api_type = 'azure'
openai.api_version = '2023-03-15-preview'
openai.api_key = data["API_Key"]
deployment_name= data["Deployment_Name"]

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
