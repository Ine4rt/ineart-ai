from fastapi import FastAPI
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Tu es un agent commercial pour Ineart (impression textile).
Tu aides à créer des devis.
"""

@app.get("/")
def home():
    return {"message": "IA Ineart active"}

@app.post("/chat")
async def chat(data: dict):
    try:
        user_message = data.get("message", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        return {"reply": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}
