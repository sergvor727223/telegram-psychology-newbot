import telebot
from openai import OpenAI
import logging
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Импорт конфигураций из отдельных файлов
from config import TELEGRAM_TOKEN, OPENAI_API_KEY, LOG_BOT_TOKEN, LOG_CHAT_ID
from system_prompt import SYSTEM_PROMPT

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def send_log_to_telegram(user, user_message, bot_response):
    """
    Отправка лога активности в отдельный Telegram-бот
    """
    try:
        log_bot = telebot.TeleBot(LOG_BOT_TOKEN)
        log_message = (
            f"Пользователь: {user}\n"
            f"Время: {datetime.now()}\n\n"
            f"Запрос:\n{user_message}\n\n"
            f"Ответ:\n{bot_response}"
        )
        log_bot.send_message(LOG_CHAT_ID, log_message)
        logger.info(f"Лог для пользователя {user} отправлен")
    
    except Exception as e:
        logger.error(f"Ошибка отправки лога: {e}")

# Инициализация бота и OpenAI
try:
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logger.error(f"Ошибка инициализации: {e}")
    sys.exit(1)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Обработчик команды /start - первое приветствие пользователя
    """
    try:
        welcome_text = (
            "Привет! Я твой психологический ассистент и друг. "
            "Готов поддержать, выслушать и помочь разобраться в себе. "
            "Чем могу помочь?"
        )
        bot.reply_to(message, welcome_text)
        logger.info(f"Пользователь {message.from_user.username} запустил бота")
    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Основной обработчик входящих сообщений
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content.strip()
        
        # Отправка лога в Telegram
        send_log_to_telegram(
            message.from_user.username, 
            message.text, 
            bot_response
        )
        
        bot.reply_to(message, bot_response)
        logger.info(f"Обработано сообщение от {message.from_user.username}")

    except Exception as e:
        error_message = "Извините, возникли проблемы с обработкой вашего запроса. Пожалуйста, попробуйте позже."
        bot.reply_to(message, error_message)
        logger.error(f"Ошибка при работе с OpenAI API: {e}")

# Бесконечный запуск бота с обработкой ошибок
def main():
    try:
        logger.info("Бот психологической поддержки запущен")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.critical(f"Критическая ошибка при работе бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
