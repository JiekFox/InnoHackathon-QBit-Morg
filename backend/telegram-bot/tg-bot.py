from fastapi import FastAPI, Request
from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from dotenv import load_dotenv
import os
import logging
import requests
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения
load_dotenv()

# Создание FastAPI приложения
app = FastAPI()

# Инициализация Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")
if not BOT_TOKEN:
    raise ValueError("Не указан токен бота в переменных окружения!")
if not BACKEND_URL:
    raise ValueError("Не указан BACKEND_URL в переменных окружения!")
bot = Bot(token=BOT_TOKEN)


@app.post(f"/webhook/{BOT_TOKEN}")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot)
        logging.info(f"Обновление: {update}")

        if update.message:
            text = update.message.text
            user_id = update.message.from_user.id
            username = update.message.from_user.username or "Unknown"

            # Обработка команды /start
            if text == "/start":
                keyboard = ReplyKeyboardMarkup(
                    [["🔍 Поиск", "Все митапы"], ["Мои митапы (созданные)", "Мои митапы (подписки)"]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text="👋 Добро пожаловать! Вы можете:\n- 📜 Посмотреть список митапов.\n- 🎯 Управлять своими митапами.\n- 🔍 Использовать поиск.",
                    reply_markup=keyboard
                )

            # Обработка команды /help
            elif text == "/help":
                await bot.send_message(
                    chat_id=update.message.chat.id,
                    text=(
                        "Вот что я могу сделать:\n"
                        "- Команда 'Все митапы': отображает список доступных митапов.\n"
                        "- Команда 'Мои митапы (созданные)': показывает митапы, которые вы создали.\n"
                        "- Команда 'Мои митапы (подписки)': показывает митапы, на которые вы подписаны.\n"
                        "- Команда 'Поиск': позволяет найти митап по ID или названию.\n"
                        "- Команды /subscribe [ID] и /unsubscribe [ID]: подписка/отписка от митапа."
                    )
                )

            # Команда "Все митапы"
            elif text == "Все митапы" or text == "/meetups":
                try:
                    response = requests.get(f"{BACKEND_URL}/meetings/")
                    response.raise_for_status()
                    meetings = response.json()
                    message = "*Список митапов:*\n" + "\n".join(
                        [
                            f'• ({meeting["id"]}) *{meeting["title"]}* '
                            f'(Дата: {datetime.fromisoformat(meeting["datetime_beg"]).strftime("%d.%m.%Y %H:%M")})'
                            for meeting in meetings[:5]
                        ]
                    )
                    # Добавление кнопки "Выбрать"
                    keyboard = InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Выбрать", callback_data="choose_meetup")]
                        ]
                    )
                    await bot.send_message(chat_id=update.message.chat.id, text=message, parse_mode="Markdown", reply_markup=keyboard)
                except Exception as e:
                    await bot.send_message(chat_id=update.message.chat.id, text=f"❌ Ошибка при получении митапов: {e}")

            # Обработка CallbackQuery для кнопки "Выбрать"
            elif update.callback_query and update.callback_query.data == "choose_meetup":
                await bot.send_message(chat_id=update.callback_query.message.chat.id, text="Введите ID или название митапа для поиска.")

            # Обработка поиска митапа
            elif text.isdigit() or text.isalnum():
                query = text
                try:
                    response = requests.get(f"{BACKEND_URL}/meetings/")
                    response.raise_for_status()
                    meetings = response.json()
                    meeting = next(
                        (m for m in meetings if str(m["id"]) == query or m["title"].lower() == query.lower()),
                        None
                    )
                    if not meeting:
                        await bot.send_message(chat_id=update.message.chat.id, text="❌ Митап не найден.")
                        return

                    # Формирование сообщения с кнопкой и изображением
                    formatted_date = datetime.fromisoformat(meeting["datetime_beg"]).strftime("%d.%m.%Y %H:%M")
                    caption = (
                        f"Информация о митапе:\n"
                        f"Название: *{meeting['title']}*\n"
                        f"Описание: _{meeting['description']}_\n"
                        f"Дата: {formatted_date}"
                    )
                    website_link = f"https://qbit-meetup.web.app/meetup-details/{meeting['id']}"
                    keyboard = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Перейти на сайт", url=website_link)]]
                    )

                    if "image" in meeting and meeting["image"]:
                        await bot.send_photo(
                            chat_id=update.message.chat.id,
                            photo=meeting["image"],
                            caption=caption,
                            reply_markup=keyboard,
                            parse_mode="Markdown"
                        )
                    else:
                        await bot.send_message(
                            chat_id=update.message.chat.id,
                            text=caption,
                            reply_markup=keyboard,
                            parse_mode="Markdown"
                        )
                except Exception as e:
                    await bot.send_message(chat_id=update.message.chat.id, text=f"❌ Ошибка при поиске митапа: {e}")

        return {"ok": True}
    except Exception as e:
        logging.error(f"❌ Ошибка обработки: {e}")
        return {"ok": False, "error": str(e)}
