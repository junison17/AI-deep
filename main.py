from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY 환경 변수를 설정해주세요.")

openai.api_key = api_key

@app.route("/translater", methods=["post"])
def translater():
    data = request.json
    language = data["language"]
    text = data["text"]

    prompt = f"{text}\n\nYou are a globally capable English teacher. You made and published TOEIC workbooks for middle school, high school, and college students in Korea.Make an English question, make a split line at the bottom, Write down the correct answer in the beginning of the explanation.translate the explanation into Korean and write it in detail.Write down in detail why the correct answer is correct and why the wrong part is wrong {language}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "you are a English teacher"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000,
    )
    return response["choices"][0]["message"]["content"]


@app.route("/web")
def web():
    return render_template("index.html")


@app.route("/")
def index():
    return "<a href='/web'>안녕하세요. 이곳은 영어 문제를 쓰는 사이트입니다. 클릭하면 사이트에 들어갑니다.</a>"
     
app.run(host="0.0.0.0", debug=True, port=80)
