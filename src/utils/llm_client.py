import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class OllamaClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """Genera respuesta del LLM"""
        url = f"{self.host}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            logger.error(f"Error en LLM: {e}")
            raise