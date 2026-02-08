# Доступ до Gemini
import google.generativeai as genai
# Налаштування API-ключа
genai.configure(api_key="ВАШ_API_KEY")
# Вибір моделі (наприклад, gemini-1.5-flash)
model = genai.GenerativeModel('gemini-1.5-flash')
# Генерація відповіді
response = model.generate_content("Привіт! Як справи?")
print(response.text)
