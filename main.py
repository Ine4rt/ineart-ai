from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# 🧠 OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎯 Comportement de ton agent
SYSTEM_PROMPT = """
Tu es un agent commercial pour Ineart, une entreprise d'impression textile.

Ton rôle :
- comprendre la demande client
- poser des questions simples
- collecter les infos pour faire un devis

Toujours demander :
- type de produit (t-shirt, hoodie, etc.)
- quantité
- délai
- fichier prêt ou non
- nom et email

Tu es rapide, simple et professionnel.
"""

# 📩 Structure des requêtes
class ChatRequest(BaseModel):
    message: str


# 🌍 Test serveur
@app.get("/")
def home():
    return {"message": "IA Ineart active"}


# 🤖 Endpoint IA
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_message = request.message

        if not user_message:
            return {"error": "message vide"}

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }
