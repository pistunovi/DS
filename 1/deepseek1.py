# Доступ до deepseek  здійснюється так
# Простий приклад для студентів
import requests
def simple_chatbot(api_key, question):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
      data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 500
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
# Використання
api_key = "ваш_ключ"
відповідь = simple_chatbot(api_key, "Поясни цикли в Python")
print(відповідь)
