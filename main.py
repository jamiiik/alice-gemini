import os
from fastapi import FastAPI, Request
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@app.post("/webhook")
async def handle_alice_request(request: Request):
    data = await request.json()
    user_question = data.get("request", {}).get("original_utterance", "")

    if not user_question:
        return {
            "response": {
                "text": "Я не расслышала вопрос. Повторите, пожалуйста.",
                "tts": "Я не расслышала вопрос. Повторите, пожалуйста.",
                "end_session": False
            },
            "version": "1.0"
        }

    try:
        response = client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=[
                {"role": "system", "content": "Ты — полезный ассистент. Отвечай кратко и по делу."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=500
        )

        ai_answer = response.choices[0].message.content

        return {
            "response": {
                "text": ai_answer,
                "tts": ai_answer,
                "end_session": False
            },
            "version": "1.0"
        }

    except Exception as e:
        print(f"Ошибка при обращении к Gemini: {e}")
        return {
            "response": {
                "text": "Произошла ошибка при обращении к ИИ. Попробуйте позже.",
                "tts": "Произошла ошибка при обращении к ИИ. Попробуйте позже.",
                "end_session": False
            },
            "version": "1.0"
        }
