# from dotenv import load_dotenv
# from openai import OpenAI
# import os

# load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     raise ValueError("GROQ_API_KEY was not found")

# client = OpenAI(
#     api_key=api_key,
#     base_url="https://api.groq.com/openai/v1"
# )

# messages = [
#     {
#         "role": "system",
#         "content": "You are a helpful AI assistant."
#     }
# ]

# while True:
#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         print("AI: Goodbye!")
#         break

#     messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=messages,
#         temperature=1.8
#     )

#     assistant_response = response.choices[0].message.content

#     messages.append({
#         "role": "assistant",
#         "content": assistant_response
#     })=

#     print("AI:", assistant_response)

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__)

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"]

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.7
    )

    assistant_response = response.choices[0].message.content

    messages.append({
        "role": "assistant",
        "content": assistant_response
    })

    return jsonify({
        "response": assistant_response,
        "message_history": messages
    })


if __name__ == "__main__":
    app.run(debug=True)