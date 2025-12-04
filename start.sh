#!/bin/bash
# Скрипт быстрого запуска бота

echo "🚀 Запуск Telegram-бота для расчета АУСН..."
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Ошибка: файл .env не найден!"
    echo ""
    echo "Создайте файл .env и добавьте в него:"
    echo "TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather"
    echo ""
    echo "Инструкция по получению токена: см. SETUP.md"
    exit 1
fi

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен!"
    exit 1
fi

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -q -r requirements.txt

# Запуск бота
echo ""
echo "✅ Запуск бота..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python bot.py

