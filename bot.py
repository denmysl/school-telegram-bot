#!/usr/bin/env python3
# school-telegram-bot for Render.com

import os
import sys
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    logger.error("❌ BOT_TOKEN не найден!")
    logger.info("Добавьте BOT_TOKEN в Environment Variables на Render")
    sys.exit(1)

print("=" * 60)
print("🏫 ШКОЛЬНЫЙ ТЕЛЕГРАМ БОТ - RENDER.COM")
print("=" * 60)
print(f"✅ Токен: {TOKEN[:10]}...")

# Устанавливаем библиотеки если нужно
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
    print("✅ Библиотеки загружены")
except ImportError:
    print("📦 Устанавливаю библиотеки...")
    os.system("pip install python-telegram-bot==20.7 > /dev/null 2>&1")
    from telegram import Update
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== КОМАНДЫ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"🎉 *Привет, {user.first_name}!*\n\n"
        f"🏫 *Школьный бот работает на Render!*\n"
        f"✅ 24/7 без перебоев\n\n"
        f"📚 *Команды:*\n"
        f"/school - Создать школу (в группе)\n"
        f"/lesson - Провести урок (5 минут)\n"
        f"/shop - Магазин улучшений\n"
        f"/profile - Мой профиль\n"
        f"/games - Мои игры на Scratch\n"
        f"/help - Помощь\n\n"
        f"💰 *Валюта:* Знания 📚",
        parse_mode='Markdown'
    )

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /games"""
    if update.message.chat.type != 'private':
        return
    
    await update.message.reply_text(
        "🎮 *Мои игры на Scratch:*\n\n"
        "1️⃣ *PolstudyIO:*\n"
        "https://scratch.mit.edu/users/PolstudyIO/\n\n"
        "2️⃣ *PolstudyStudio:*\n"
        "https://scratch.mit.edu/users/PolstudyStudio/\n\n"
        "🌟 Заходите, играйте, оставляйте комментарии!",
        parse_mode='Markdown'
    )

async def school(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /school - создание школы в группе"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("🏫 *Создавайте школу в группе!*", parse_mode='Markdown')
        return
    
    user = update.effective_user
    school_name = " ".join(context.args) if context.args else f"Школа {user.first_name}"
    
    await update.message.reply_text(
        f"🎉 *ШКОЛА СОЗДАНА!*\n\n"
        f"🏫 *Название:* {school_name}\n"
        f"👑 *Директор:* {user.first_name}\n"
        f"💰 *Стартовый капитал:* 500 Знаний 📚\n"
        f"📅 *Основана:* {datetime.now().strftime('%d.%m.%Y')}\n\n"
        f"Теперь используйте /lesson для проведения уроков!",
        parse_mode='Markdown'
    )

async def lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /lesson"""
    if update.message.chat.type == 'private':
        await update.message.reply_text("👨‍🏫 *Проводите уроки в группе!*", parse_mode='Markdown')
        return
    
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("📐 Математика", callback_data="math"),
         InlineKeyboardButton("📚 Русский", callback_data="russian")],
        [InlineKeyboardButton("🌍 География", callback_data="geo"),
         InlineKeyboardButton("💻 Информатика", callback_data="it")]
    ]
    
    await update.message.reply_text(
        "👨‍🏫 *ПРОВЕДЕНИЕ УРОКА*\n\n"
        "⏱️ *Длительность:* 5 минут\n"
        "💰 *Награда:* 20-50 Знаний 📚\n"
        "🎮 *Мини-игра:* Викторина\n\n"
        "*Выберите предмет:*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /shop"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = [
        [InlineKeyboardButton("🦊 Аватары", callback_data="avatars"),
         InlineKeyboardButton("🎨 Цвета", callback_data="colors")],
        [InlineKeyboardButton("🏅 Титулы", callback_data="titles"),
         InlineKeyboardButton("💰 Баланс", callback_data="balance")]
    ]
    
    await update.message.reply_text(
        "🛒 *МАГАЗИН УЛУЧШЕНИЙ*\n\n"
        "💰 *Валюта:* Знания 📚\n\n"
        "*Категории:*\n"
        "🦊 *Аватары* - иконки профиля\n"
        "🎨 *Цвета* - цвет имени\n"
        "🏅 *Титулы* - особые звания\n\n"
        "💡 *Зарабатывайте проводя уроки!*",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /profile"""
    user = update.effective_user
    await update.message.reply_text(
        f"👤 *Профиль: {user.first_name}*\n\n"
        f"💰 *Баланс:* 100 Знаний 📚\n"
        f"📊 *Уровень:* 1\n"
        f"🏫 *Школа:* не состоит\n\n"
        f"💡 Присоединяйтесь к школе (/school в группе)!",
        parse_mode='Markdown'
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        "📚 *ПОМОЩЬ ПО КОМАНДАМ*\n\n"
        "🎮 *Основные:*\n"
        "/start - начало работы\n"
        "/games - мои игры на Scratch\n"
        "/profile - мой профиль\n\n"
        "🏫 *В группах:*\n"
        "/school [название] - создать школу\n"
        "/lesson - провести урок (5 минут)\n"
        "/shop - магазин улучшений\n\n"
        "✅ *Бот работает 24/7 на Render.com!*",
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "math":
        await query.edit_message_text("📐 *Урок математики начат!* Ученики пишут /join", parse_mode='Markdown')
    elif query.data == "balance":
        await query.edit_message_text("💰 *Ваш баланс:* 100 Знаний 📚", parse_mode='Markdown')

# ========== ЗАПУСК ==========
def main():
    """Запуск бота"""
    print("🤖 Создаю приложение бота...")
    
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("games", games))
    application.add_handler(CommandHandler("school", school))
    application.add_handler(CommandHandler("lesson", lesson))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("help", help_cmd))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Бот настроен!")
    print("📱 Напишите /start в Telegram")
    print("🌐 Хостинг: Render.com")
    print("💰 Валюта: Знания 📚")
    print("⏱️ Уроки: 5 минут")
    
    # Запускаем
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"💥 Ошибка: {e}")
        print("🔄 Перезапуск через 10 секунд...")
        import time
        time.sleep(10)
        main()
