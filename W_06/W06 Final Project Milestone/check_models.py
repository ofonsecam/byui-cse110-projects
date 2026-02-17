"""Script de diagnóstico: lista los modelos Gemini disponibles con tu API Key (SDK google-genai v1+)."""

from pathlib import Path

from dotenv import load_dotenv
from google import genai
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- Modelos Generativos Disponibles (SDK v1+) ---")
try:
    for model in client.models.list():
        print(f"Modelo: {model.name} - Soporta: {model.supported_actions}")
except Exception as e:
    print(f"Error: {e}")
