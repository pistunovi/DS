# Доступ до Grok
# Спосіб 1: через офіційний xAI SDK
# pip install xai-sdk
import os
from xai_sdk import Client
from xai_sdk.chat import user, system
# Бери ключ з https://console.x.ai/team/default/api-keys
client = Client(api_key=os.getenv("XAI_API_KEY"))
response = client.chat.completions.create(
    model="grok-4",               # або grok-4-1-fast, grok-3 тощо
    messages=[
        system("Ти корисний український AI-помічник"),
        user("Привіт! Напиши короткий жарт про Python")
    ],
    temperature=0.7,
    max_tokens=200
)
print(response.choices[0].message.content)
```
Або через OpenAI-стиль (багато хто так робить):
```python
# pip install openai
from openai import OpenAI
import os
client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)
response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "system", "content": "Ти крутий AI з почуттям гумору"},
        {"role": "user", "content": "Розкажи анекдот про програмістів"}
    ]
)
print(response.choices[0].message.content)
``
