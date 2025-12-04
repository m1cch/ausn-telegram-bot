#!/usr/bin/env python3
"""
Telegram-бот для расчета налогов по АУСН (Автоматизированная упрощенная система налогообложения)
"""

import os
import logging
from typing import Dict
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
INCOME, EXPENSES = range(2)


class AUSNCalculator:
    """Калькулятор налогов АУСН"""
    
    @staticmethod
    def calculate_income_only(income: float) -> Dict[str, float]:
        """
        Расчет по схеме 'доходы' (8%)
        
        Args:
            income: Сумма дохода
            
        Returns:
            Словарь с результатами расчета
        """
        tax = income * 0.08
        return {
            'tax': tax,
            'rate': 0.08,
            'rate_percent': 8
        }
    
    @staticmethod
    def calculate_income_minus_expenses(income: float, expenses: float) -> Dict[str, float]:
        """
        Расчет по схеме 'доходы минус расходы' (20%, но не менее 3% от дохода)
        
        Args:
            income: Сумма дохода
            expenses: Сумма расходов
            
        Returns:
            Словарь с результатами расчета
        """
        profit = income - expenses
        tax_20_percent = profit * 0.2
        min_tax = income * 0.03
        
        # Налог не может быть меньше 3% от дохода
        tax = max(tax_20_percent, min_tax)
        
        return {
            'tax': tax,
            'profit': profit,
            'tax_20_percent': tax_20_percent,
            'min_tax': min_tax,
            'used_minimum': tax == min_tax
        }
    
    @staticmethod
    def format_money(amount: float) -> str:
        """Форматирование суммы в рубли"""
        return f"{amount:,.2f}".replace(',', ' ').replace('.', ',') + " ₽"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога с пользователем"""
    welcome_text = (
        "👋 <b>Привет! Я помогу рассчитать налоги по АУСН</b>\n\n"
        "📊 АУСН — автоматизированная упрощённая система налогообложения\n\n"
        "<b>Два варианта налогообложения:</b>\n"
        "🔹 <b>Доходы</b> — 8% от всех доходов\n"
        "🔹 <b>Доходы минус расходы</b> — 20% от разницы (но не менее 3% от дохода)\n\n"
        "⚠️ <b>Важно!</b> До 31 декабря 2025 года нужно перейти на АУСН\n\n"
        "📍 <b>Ограничения АУСН:</b>\n"
        "• Годовой доход до 60 млн ₽\n"
        "• Не более 5 сотрудников\n"
        "• Работа в Москве, СПб или МО\n"
        "• Наличие счета в уполномоченном банке\n\n"
        "Для расчета отправьте сумму <b>годового дохода</b> в рублях:"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='HTML'
    )
    
    return INCOME


async def income_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка введенного дохода"""
    try:
        income = float(update.message.text.replace(' ', '').replace(',', '.'))
        
        if income <= 0:
            await update.message.reply_text(
                "❌ Доход должен быть положительным числом. Попробуйте еще раз:"
            )
            return INCOME
        
        if income > 60_000_000:
            await update.message.reply_text(
                "⚠️ <b>Внимание!</b> Годовой доход превышает лимит АУСН (60 млн ₽)\n"
                "При таком доходе АУСН недоступна.\n\n"
                "Продолжить расчет для ознакомления?",
                parse_mode='HTML'
            )
        
        context.user_data['income'] = income
        
        await update.message.reply_text(
            f"✅ Доход: <b>{AUSNCalculator.format_money(income)}</b>\n\n"
            f"Теперь введите сумму <b>годовых расходов</b> в рублях:\n"
            f"(Если расходов нет, введите 0)",
            parse_mode='HTML'
        )
        
        return EXPENSES
        
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректное число (например: 1000000 или 1 000 000)"
        )
        return INCOME


async def expenses_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка введенных расходов и расчет налогов"""
    try:
        expenses = float(update.message.text.replace(' ', '').replace(',', '.'))
        
        if expenses < 0:
            await update.message.reply_text(
                "❌ Расходы не могут быть отрицательными. Попробуйте еще раз:"
            )
            return EXPENSES
        
        income = context.user_data['income']
        
        if expenses > income:
            await update.message.reply_text(
                "⚠️ <b>Внимание!</b> Расходы превышают доходы!\n"
                "Продолжить расчет?",
                parse_mode='HTML'
            )
        
        # Расчет обоих вариантов
        variant1 = AUSNCalculator.calculate_income_only(income)
        variant2 = AUSNCalculator.calculate_income_minus_expenses(income, expenses)
        
        # Остаток после налогов
        net_profit_v1 = income - variant1['tax'] - expenses
        net_profit_v2 = income - variant2['tax'] - expenses
        
        # Определяем, какой вариант выгоднее
        best_variant = 1 if variant1['tax'] < variant2['tax'] else 2
        
        # Формируем ответ
        result_text = (
            "📊 <b>РЕЗУЛЬТАТЫ РАСЧЕТА</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💰 Доход: <b>{AUSNCalculator.format_money(income)}</b>\n"
            f"💸 Расходы: <b>{AUSNCalculator.format_money(expenses)}</b>\n"
            f"📈 Прибыль: <b>{AUSNCalculator.format_money(income - expenses)}</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        
        # Вариант 1: Доходы
        result_text += (
            f"{'🏆 ' if best_variant == 1 else ''}🔹 <b>ВАРИАНТ 1: ДОХОДЫ (8%)</b>\n"
            f"└ Налог: <b>{AUSNCalculator.format_money(variant1['tax'])}</b>\n"
            f"└ Остаток чистыми: <b>{AUSNCalculator.format_money(net_profit_v1)}</b>\n\n"
        )
        
        # Вариант 2: Доходы минус расходы
        result_text += (
            f"{'🏆 ' if best_variant == 2 else ''}🔹 <b>ВАРИАНТ 2: ДОХОДЫ - РАСХОДЫ (20%)</b>\n"
        )
        
        if variant2['used_minimum']:
            result_text += (
                f"└ Налог 20%: {AUSNCalculator.format_money(variant2['tax_20_percent'])}\n"
                f"└ <b>Применен минимум (3% от дохода)</b>\n"
                f"└ Налог к уплате: <b>{AUSNCalculator.format_money(variant2['tax'])}</b>\n"
            )
        else:
            result_text += (
                f"└ Налог: <b>{AUSNCalculator.format_money(variant2['tax'])}</b>\n"
            )
        
        result_text += f"└ Остаток чистыми: <b>{AUSNCalculator.format_money(net_profit_v2)}</b>\n\n"
        
        # Итоговая рекомендация
        result_text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if best_variant == 1:
            saving = variant2['tax'] - variant1['tax']
            result_text += (
                f"✅ <b>РЕКОМЕНДАЦИЯ:</b> ДОХОДЫ (8%)\n"
                f"💡 Экономия: <b>{AUSNCalculator.format_money(saving)}</b>"
            )
        else:
            saving = variant1['tax'] - variant2['tax']
            result_text += (
                f"✅ <b>РЕКОМЕНДАЦИЯ:</b> ДОХОДЫ - РАСХОДЫ (20%)\n"
                f"💡 Экономия: <b>{AUSNCalculator.format_money(saving)}</b>"
            )
        
        result_text += (
            "\n\n━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔄 Для нового расчета используйте /start"
        )
        
        await update.message.reply_text(result_text, parse_mode='HTML')
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            "❌ Пожалуйста, введите корректное число (например: 500000 или 500 000)"
        )
        return EXPENSES


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена операции"""
    await update.message.reply_text(
        "❌ Расчет отменен. Для нового расчета используйте /start",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показ справки"""
    help_text = (
        "📖 <b>СПРАВКА ПО БОТУ</b>\n\n"
        "Этот бот помогает рассчитать налоги по АУСН и выбрать оптимальный вариант налогообложения.\n\n"
        "<b>Доступные команды:</b>\n"
        "/start - Начать новый расчет\n"
        "/help - Показать эту справку\n"
        "/cancel - Отменить текущий расчет\n\n"
        "<b>Как пользоваться:</b>\n"
        "1️⃣ Введите годовой доход\n"
        "2️⃣ Введите годовые расходы\n"
        "3️⃣ Получите расчет по обоим вариантам\n\n"
        "<b>О системе АУСН:</b>\n"
        "• Действует в Москве, СПб и МО\n"
        "• Лимит дохода: 60 млн ₽/год\n"
        "• Максимум 5 сотрудников\n"
        "• Переход до 31.12.2025\n\n"
        "📞 Подробности на сайте ФНС: nalog.ru"
    )
    
    await update.message.reply_text(help_text, parse_mode='HTML')


def main() -> None:
    """Запуск бота"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не найден в переменных окружения!")
        logger.error("Создайте файл .env и добавьте туда токен бота")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Настраиваем обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, income_received)],
            EXPENSES: [MessageHandler(filters.TEXT & ~filters.COMMAND, expenses_received)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Регистрируем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

