# 🤖 Telegram Psychology Bot

Этот бот — твой персональный психологический ассистент в Telegram. Он помогает пользователям справляться с трудностями, поддерживает в сложных ситуациях и вдохновляет на личностный рост.

## ✨ Функции бота
- 🔹 Ответы с эмпатией и пониманием
- 🔹 Генерация ответов с помощью OpenAI API
- 🔹 Логирование запросов в Telegram-чат
- 🔹 Полная автономность и простота в использовании

---

## 🚀 Развертывание на Render

### 1️⃣ **Создание и настройка проекта**
1. **Клонируй репозиторий:**
   ```bash
   git clone https://github.com/sergvor727223/telegram-psychology-newbot.git
   cd telegram-psychology-newbot

Установи зависимости:

pip install -r requirements.txt

Создай .env файл и добавь в него переменные:

TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
LOG_BOT_TOKEN=your_log_bot_token
LOG_CHAT_ID=your_log_chat_id

2  ️⃣ Разворачивание на Render
1.Перейди в Render и создай новый веб-сервис.

2.Подключи репозиторий (telegram-psychology-newbot).

3.Укажи настройки:

- Build Command: pip install -r requirements.txt
- Start Command: python main.py
- Environment Variables: добавь вручную все переменные из .env.
4.Нажми "Deploy" и жди завершения процесса. 🚀