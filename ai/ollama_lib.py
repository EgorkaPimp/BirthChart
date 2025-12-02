import ollama
import yaml


def chat_with_ollama():
    # Простой запрос
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": "Привет! Расскажи о себе"}]
    )
    return response['message']['content']


# Или с использованием stream (потоковый ответ)
def stream_chat(mes):
    stream = ollama.chat(
        model="llama3.1:8b",
        messages=[mes],
        stream=True
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

with open('../yaml/config_Penza_1481996_1530.yaml', 'r', encoding="utf-8") as f:
    templates = yaml.safe_load(f)
    print(templates)
    stream_chat(templates)