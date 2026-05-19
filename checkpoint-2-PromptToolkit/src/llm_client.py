import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST  = os.getenv("OLLAMA_HOST",  "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
TIMEOUT      = int(os.getenv("OLLAMA_TIMEOUT", "120"))


class LLMClient:

    def __init__(self, host=OLLAMA_HOST, model=OLLAMA_MODEL):
        self.host  = host.rstrip("/")
        self.model = model
        self.url   = f"{self.host}/api/chat"

    def chat(self, prompt, system="", temp=0.7, max_tokens=1024):
        mensagens = []
        if system:
            mensagens.append({"role": "system", "content": system})
        mensagens.append({"role": "user", "content": prompt})

        payload = {
            "model":   self.model,
            "messages": mensagens,
            "stream":  False,
            "options": {"temperature": temp, "num_predict": max_tokens},
        }

        for tentativa in range(1, 4):
            try:
                inicio = time.time()
                resp   = requests.post(self.url, json=payload, timeout=TIMEOUT)
                resp.raise_for_status()
                fim    = time.time()
                dados  = resp.json()
                msg    = dados.get("message", {})
                return {
                    "resposta":        msg.get("content", "").strip(),
                    "tokens_prompt":   dados.get("prompt_eval_count", 0),
                    "tokens_resposta": dados.get("eval_count", 0),
                    "tempo_ms":        round((fim - inicio) * 1000, 2),
                }
            except requests.exceptions.Timeout:
                print(f"  [LLMClient] Timeout (tentativa {tentativa}/3)...")
                time.sleep(2 ** tentativa)
            except requests.exceptions.ConnectionError:
                raise ConnectionError(f"Não foi possível conectar ao Ollama em {self.host}.\nVerifique se o Ollama está rodando: ollama serve")
            except requests.exceptions.HTTPError as e:
                raise RuntimeError(f"Erro HTTP do Ollama: {e}")

        raise TimeoutError("Ollama não respondeu após 3 tentativas.")