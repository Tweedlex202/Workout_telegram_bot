import asyncio
import logging
import os
import sys
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота (получите у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN', "")

# ID разработчика (замените на ваш Telegram ID)
DEVELOPER_ID = int(os.getenv('DEVELOPER_ID', #766824340))

# Отключаем предупреждения httpx
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Словарь для хранения данных пользователей
user_data = {}

class WorkoutBot:
    def __init__(self):
        self.application = None
        self.training_programs = {
            "phase_1": {
                "monday_wednesday_friday": {
                    "muscle_group_1": {
                        "title": "Фаза-1 Понедельник",
                        "program": """
💪 Группа мышц: Грудь/Трицепс

• [жим гант. на накл. скамье - 4х8]
• [Жим на тренажере узк.хват - 4х10]
• [Жим штанги на накл. скамье - 3х10]
• [Разводка на тренажере - 4х12]
• [Жим на гориз. скамье - 3х10]
• [Геркулес снизу - 3х10]
• [Пуловер - 2х10]
• [Трицепс в наклоне с гантелями - 4х8]
• [Трицепс с канатом на трен. - 4х10]
• [Франц.жим лежа - 3х10]
• [Трицепс на тренажере обр хват - 4х10]
                        """
                    },
                    "muscle_group_2": {
                        "title": "Фаза-1 Среда",
                        "program": """
💪 Группа мышц: Спина/Бицепс

• [Турник - 2х10]
• [Пул даун к груди - 3х10]
• [Пул даун узк.хват - 3х10]
• [Тяга Т грифа уз.хват - 4х8]
• [Тяга ниж.блока шир.хват - 4х10]
• [Тяга гантели в наклоне - 4х8]
• [Жим п.грифа на скамье Л.Скотта - 4х10]
• [Молот на скамье Л.Скотта - 3х10]
• [Бицепс на верх.блоке - 4х10]
• [Бицепс на трен. обр. хватом - 4х10]
                        """
                    },
                    "muscle_group_3": {
                        "title": "Фаза-1 Пятница",
                        "program": """
💪 Группа мышц: Плечи/Ноги

• [Турник (узк. хват) - 2х10]
• [Арм. жим на прям. скамье - 4х10]
• [Разводка блинами - 4х10]
• [Жим Арнольда - 4х10]
• [Поднятие блина - 4х10]
• [Задняя бабочка (брать свер.)- 4х10]
• [Ноги задняя часть - 4х10]
• [Ноги передняя часть - 4х10]
• [Присед с весом - 4х10]
• [Приседания с гантелей - 4х10]
                        """
                    }
                },
                "tuesday_thursday_saturday": {
                    "muscle_group_1": {
                        "title": "Фаза-1 Вторник",
                        "program": """
💪 Группа мышц: Грудь/Трицепс

• [жим гант. на накл. скамье - 4х8]
• [Жим на тренажере узк.хват - 4х10]
• [Жим штанги на накл. скамье - 3х10]
• [Разводка на тренажере - 4х12]
• [Жим на гориз. скамье - 3х10]
• [Геркулес снизу - 3х10]
• [Пуловер - 2х10]
• [Трицепс в наклоне с гантелями - 4х8]
• [Трицепс с канатом на трен. - 4х10]
• [Франц.жим лежа - 3х10]
• [Трицепс на тренажере обр хват - 4х10]
                        """
                    },
                    "muscle_group_2": {
                        "title": "Фаза-1 - Четверг",
                        "program": """
💪 Группа мышц: Спина/Бицепс

• [Турник - 2х10]
• [Пул даун к груди - 3х10]
• [Пул даун узк.хват - 3х10]
• [Тяга Т грифа уз.хват - 4х8]
• [Тяга ниж.блока шир.хват - 4х10]
• [Тяга гантели в наклоне - 4х8]
• [Жим п.грифа на скамье Л.Скотта - 4х10]
• [Молот на скамье Л.Скотта - 3х10]
• [Бицепс на верх.блоке - 4х10]
• [Бицепс на трен. обр. хватом - 4х10]
                        """
                    },
                    "muscle_group_3": {
                        "title": "Фаза-1 Суббота",
                        "program": """
💪 Группа мышц: Плечи/Ноги

• [Турник (узк. хват) - 2х10]
• [Арм. жим на прям. скамье - 4х10]
• [Разводка блинами - 4х10]
• [Жим Арнольда - 4х10]
• [Поднятие блина - 4х10]
• [Задняя бабочка (брать свер.)- 4х10]
• [Ноги задняя часть - 4х10]
• [Ноги передняя часть - 4х10]
• [Присед с весом - 4х10]
• [Приседания с гантелей - 4х10]
                        """
                    }
                }
            },
            "phase_2": {
                "monday_wednesday_friday": {
                    "muscle_group_1": {
                        "title": "Фаза-2 Понедельник",
                        "program": """
💪 Группа мышц: Спина/Плечи

• [Тяга узк.хватом штанги - 3х10]
• [Тяга на пул.дауне к груди - 4х10]
• [Тяга гантели в наклоне - 3х10]
• [Тяга ниж.блока шир.хватом - 4х10]
• [Тяга ниж.бл с канатом на задн D-ты - 4х12]
• [Жим штанги передний сидя - 3х8]
• [Жим штанги задний сидя - 3х8]
• [Гриф"вертолет" узким хватом - 4х10]
• [жим Арнольда - 3х10]
• [поднятие блина вперед - 4х10]
                        """
                    },
                    "muscle_group_2": {
                        "title": "Фаза-2 Среда",
                        "program": """
💪 Группа мышц: Грудь/Трицепс

• [Разводка на шир. бабочке - 4х10]
• [Жим штанги на горизонт.скамье - 3х10]
• [Трен. "Хамер" узк. хват - 4х10]
• [Жим гантелей на накл.скамье - 3х10]
• [Бабочка средняя (обычная) - 3х12]
• [Пуловер с гантелью - 3х12]
• [Тяга верх.блока с канатом - 3х12]
• [Тяга гантели в наклоне - 3х8]
• [тяга верх.блока обрат. хватом - 3х12]
• [Отжимание на брусьях - 3х10]
                        """
                    },
                    "muscle_group_3": {
                        "title": "Фаза-2 Пятница",
                        "program": """
💪 Группа мышц: Бицепс/Ноги

• [Турник на бицепс - 4х10]
• [Тяга гантелей на "Л.Скотта" - 4х10]
• [Тяга обр. хватом на "Л.Скотта" - 3х12]
• [Тяга штанги шир.хватом - 4х10]
• [Велосипед - 10 мин]
• [Полуприседы - 3х10 (без веса)]
• [Сгибание и разгибания на трен. - 3х10]
• [Приседания со штангой - 4х10]
• [Выпады с гантелями - 3х12]
• [Приседания на тренажере - 3х10]
• [Приседания "сумо" с гантелью - 4х10]
                        """
                    }
                },
                "tuesday_thursday_saturday": {
                    "muscle_group_1": {
                        "title": "Фаза-2 Вторник",
                        "program": """
💪 Группа мышц: Спина/Плечи

• [Тяга узк.хватом штанги - 3х10]
• [Тяга на пул.дауне к груди - 4х10]
• [Тяга гантели в наклоне - 3х10]
• [Тяга ниж.блока шир.хватом - 4х10]
• [Тяга ниж.бл с канатом на задн D-ты - 4х12]
• [Жим штанги передний сидя - 3х8]
• [Жим штанги задний сидя - 3х8]
• [Гриф"вертолет" узким хватом - 4х10]
• [жим Арнольда - 3х10]
• [поднятие блина вперед - 4х10]
                        """
                    },
                    "muscle_group_2": {
                        "title": "Фаза-2 Четверг",
                        "program": """
💪 Группа мышц: Грудь/Трицепс

• [Разводка на шир. бабочке - 4х10]
• [Жим штанги на горизонт.скамье - 3х10]
• [Трен. "Хамер" узк. хват - 4х10]
• [Жим гантелей на накл.скамье - 3х10]
• [Бабочка средняя (обычная) - 3х12]
• [Пуловер с гантелью - 3х12]
• [Тяга верх.блока с канатом - 3х12]
• [Тяга гантели в наклоне - 3х8]
• [тяга верх.блока обрат. хватом - 3х12]
• [Отжимание на брусьях - 3х10]
                        """
                    },
                    "muscle_group_3": {
                        "title": "Фаза-2 Суббота",
                        "program": """
💪 Группа мышц: Бицепс/Ноги

• [Турник на бицепс - 4х10]
• [Тяга гантелей на "Л.Скотта" - 4х10]
• [Тяга обр. хватом на "Л.Скотта" - 3х12]
• [Тяга штанги шир.хватом - 4х10]
• [Велосипед - 10 мин]
• [Полуприседы - 3х10 (без веса)]
• [Сгибание и разгибания на трен. - 3х10]
• [Приседания со штангой - 4х10]
• [Выпады с гантелями - 3х12]
• [Приседания на тренажере - 3х10]
• [Приседания "сумо" с гантелью - 4х10]
                        """
                    }
                }
            }
        }

    def is_developer(self, user_id):
        """Проверка, является ли пользователь разработчиком"""
        return user_id == DEVELOPER_ID

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        user_data[user_id] = {}
        
        keyboard = [
            [InlineKeyboardButton("📊 Фаза 1", callback_data="phase_1")],
            [InlineKeyboardButton("📊 Фаза 2", callback_data="phase_2")]
        ]
        
        # Добавляем кнопки разработчика
        if self.is_developer(user_id):
            keyboard.append([
                InlineKeyboardButton("🔧 Dev Mode", callback_data="dev_mode")
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🏋️‍♂️ Добро пожаловать в фитнес-бот!\n\n"
            "Сначала Выбери фазу тренировки:",
            reply_markup=reply_markup
        )

    async def select_phase(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора фазы"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        phase = query.data  # "phase_1" или "phase_2"
        user_data[user_id]['phase'] = phase
        
        phase_name = "Фаза 1" if phase == "phase_1" else "Фаза 2"
        
        keyboard = [
            [InlineKeyboardButton("🗓️ Пн, Ср, Пт", callback_data="days_mwf")],
            [InlineKeyboardButton("🗓️ Вт, Чт, Сб", callback_data="days_tts")],
            [InlineKeyboardButton("⬅️ Назад к фазам", callback_data="back_to_phases")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # РЕДАКТИРУЕМ существующее сообщение
        await query.edit_message_text(
            text=f"✅ Выбрана: **{phase_name}**\n\n"
                 "Теперь выберите дни тренировок:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def select_days(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора дней тренировок"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if query.data == "days_mwf":
            user_data[user_id]['days'] = 'monday_wednesday_friday'
            days_text = "Понедельник, Среда, Пятница"
        else:
            user_data[user_id]['days'] = 'tuesday_thursday_saturday'
            days_text = "Вторник, Четверг, Суббота"
        
        phase = user_data[user_id]['phase']
        phase_name = "Фаза 1" if phase == "phase_1" else "Фаза 2"
        
        # Разные группы мышц для разных фаз
        if phase == "phase_1":
            keyboard = [
                [InlineKeyboardButton("💪 Грудь/Трицепс", callback_data="muscle_group_1")],
                [InlineKeyboardButton("🦵 Спина/Бицепс", callback_data="muscle_group_2")],
                [InlineKeyboardButton("💪 Плечи/Ноги", callback_data="muscle_group_3")],
                [InlineKeyboardButton("⬅️ Назад к дням", callback_data="back_to_days")]
            ]
        else:  # phase_2
            keyboard = [
                [InlineKeyboardButton("💪 Спина/Плечи", callback_data="muscle_group_1")],
                [InlineKeyboardButton("🦵 Грудь/Трицепс", callback_data="muscle_group_2")],
                [InlineKeyboardButton("💪 Бицепс/Ноги", callback_data="muscle_group_3")],
                [InlineKeyboardButton("⬅️ Назад к дням", callback_data="back_to_days")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # РЕДАКТИРУЕМ существующее сообщение
        await query.edit_message_text(
            text=f"✅ **{phase_name}** - **{days_text}**\n\n"
                 "Выберите группу мышц:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def select_muscle_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора группы мышц"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        muscle_group = query.data  # "muscle_group_1", "muscle_group_2", "muscle_group_3"
        user_data[user_id]['muscle_group'] = muscle_group
        
        phase = user_data[user_id]['phase']
        
        # Проверяем, выбраны ли дни - если нет, ставим по умолчанию
        if 'days' not in user_data[user_id]:
            user_data[user_id]['days'] = 'monday_wednesday_friday'  # По умолчанию Пн/Ср/Пт
        
        days = user_data[user_id]['days']
        program = self.training_programs[phase][days][muscle_group]
        
        # ОТПРАВЛЯЕМ НОВОЕ СООБЩЕНИЕ с программой тренировки
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎯 **{program['title']}**\n\n"
                 f"{program['program']}",
            parse_mode='Markdown'
        )
        
        # ОТПРАВЛЯЕМ НОВОЕ СООБЩЕНИЕ с кнопками управления тренировкой
        keyboard = [
            [InlineKeyboardButton("▶️ Старт тренировки", callback_data="start_workout")],
            [InlineKeyboardButton("🔄 Выбрать др. программу", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=user_id,
            text="Готов к тренировке?\n\n"
                 "💧 **Не забывай пить воду 2-3л!** 💦",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def back_to_days(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат к выбору дней"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        phase = user_data[user_id]['phase']
        phase_name = "Фаза 1" if phase == "phase_1" else "Фаза 2"
        
        keyboard = [
            [InlineKeyboardButton("🗓️ Пн, Ср, Пт", callback_data="days_mwf")],
            [InlineKeyboardButton("🗓️ Вт, Чт, Сб", callback_data="days_tts")],
            [InlineKeyboardButton("⬅️ Назад к фазам", callback_data="back_to_phases")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # РЕДАКТИРУЕМ существующее сообщение
        await query.edit_message_text(
            text=f"✅ Выбрана: **{phase_name}**\n\n"
                 "Теперь выберите дни тренировок:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def back_to_phases(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат к выбору фаз"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user_data[user_id] = {}
        
        keyboard = [
            [InlineKeyboardButton("📊 Фаза 1", callback_data="phase_1")],
            [InlineKeyboardButton("📊 Фаза 2", callback_data="phase_2")]
        ]
        
        if self.is_developer(user_id):
            keyboard.append([
                InlineKeyboardButton("🔧 Dev Mode", callback_data="dev_mode")
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # РЕДАКТИРУЕМ существующее сообщение
        await query.edit_message_text(
            text="🏋️‍♂️ Выберите фазу тренировки:",
            reply_markup=reply_markup
        )

    async def back_to_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат к началу"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user_data[user_id] = {}
        
        keyboard = [
            [InlineKeyboardButton("📊 Фаза 1", callback_data="phase_1")],
            [InlineKeyboardButton("📊 Фаза 2", callback_data="phase_2")]
        ]
        
        if self.is_developer(user_id):
            keyboard.append([
                InlineKeyboardButton("🔧 Dev Mode", callback_data="dev_mode")
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # ОТПРАВЛЯЕМ НОВОЕ СООБЩЕНИЕ для нового старта
        await context.bot.send_message(
            chat_id=user_id,
            text="🏋️‍♂️ Выберите фазу тренировки:",
            reply_markup=reply_markup
        )

    async def dev_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Режим разработчика"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_developer(user_id):
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Доступ запрещен!"
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("🛑 Stop Bot", callback_data="stop_bot")],
            [InlineKeyboardButton("🔄 Restart Bot", callback_data="restart_bot")],
            [InlineKeyboardButton("📊 Bot Stats", callback_data="bot_stats")],
            [InlineKeyboardButton("👥 Active Users", callback_data="active_users")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Если это callback_query, редактируем сообщение
        if hasattr(update, 'callback_query') and update.callback_query:
            await query.edit_message_text(
                text="🔧 **РЕЖИМ РАЗРАБОТЧИКА**\n\n"
                     "Выберите действие:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            # Если это обычное сообщение, отправляем новое
            await context.bot.send_message(
                chat_id=user_id,
                text="🔧 **РЕЖИМ РАЗРАБОТЧИКА**\n\n"
                     "Выберите действие:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )

    async def stop_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Остановка бота"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_developer(user_id):
            await query.edit_message_text("❌ Доступ запрещен!")
            return
        
        await query.edit_message_text(
            text="🛑 **БОТ ОСТАНАВЛИВАЕТСЯ...**\n\n"
                 "Завершение работы через 3 секунды...",
            parse_mode='Markdown'
        )
        
        # Ждем 3 секунды и останавливаем
        await asyncio.sleep(3)
        
        if self.application:
            await self.application.stop()
        
        sys.exit(0)

    async def restart_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Перезапуск бота"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_developer(user_id):
            await query.edit_message_text("❌ Доступ запрещен!")
            return
        
        await query.edit_message_text(
            text="🔄 **БОТ ПЕРЕЗАПУСКАЕТСЯ...**\n\n"
                 "Перезапуск через 3 секунды...",
            parse_mode='Markdown'
        )
        
        # Ждем 3 секунды
        await asyncio.sleep(3)
        
        # Перезапускаем Python скрипт
        os.execv(sys.executable, ['python'] + sys.argv)

    async def bot_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Статистика бота"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_developer(user_id):
            await query.edit_message_text("❌ Доступ запрещен!")
            return
        
        stats_text = f"""
📊 **СТАТИСТИКА БОТА**

👥 Активных пользователей: {len(user_data)}
🤖 Версия бота: 1.3
⏰ Время работы: {datetime.now().strftime('%H:%M:%S')}
📅 Дата: {datetime.now().strftime('%d.%m.%Y')}

🔧 Dev ID: {DEVELOPER_ID}
        """
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="bot_stats")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="dev_mode")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=stats_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def active_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Список активных пользователей"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if not self.is_developer(user_id):
            await query.edit_message_text("❌ Доступ запрещен!")
            return
        
        if not user_data:
            users_text = "👥 **АКТИВНЫЕ ПОЛЬЗОВАТЕЛИ**\n\n📭 Нет активных пользователей"
        else:
            users_text = "👥 **АКТИВНЫЕ ПОЛЬЗОВАТЕЛИ**\n\n"
            for i, (uid, data) in enumerate(user_data.items(), 1):
                phase = data.get('phase', 'Не выбрано')
                days = data.get('days', 'Не выбрано')
                muscle_group = data.get('muscle_group', 'Не выбрано')
                
                phase_name = "Фаза 1" if phase == "phase_1" else "Фаза 2" if phase == "phase_2" else phase
                days_name = "Пн/Ср/Пт" if days == "monday_wednesday_friday" else "Вт/Чт/Сб" if days == "tuesday_thursday_saturday" else days
                
                # Разные группы мышц для разных фаз
                if phase == "phase_1":
                    muscle_name = "Грудь/Трицепс" if muscle_group == "muscle_group_1" else "Спина/Бицепс" if muscle_group == "muscle_group_2" else "Плечи/Ноги" if muscle_group == "muscle_group_3" else muscle_group
                elif phase == "phase_2":
                    muscle_name = "Спина/Плечи" if muscle_group == "muscle_group_1" else "Грудь/Трицепс" if muscle_group == "muscle_group_2" else "Бицепс/Ноги" if muscle_group == "muscle_group_3" else muscle_group
                else:
                    muscle_name = muscle_group
                
                users_text += f"{i}. ID: `{uid}`\n   {phase_name} - {days_name} - {muscle_name}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="active_users")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="dev_mode")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=users_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def start_workout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало тренировки"""
        query = update.callback_query
        user_id = query.from_user.id
        
        logger.info(f"Пользователь {user_id} начал тренировку")
        
        try:
            await query.answer()
            user_data[user_id]['start_time'] = datetime.now()
            
            keyboard = [
                [InlineKeyboardButton("⏹️ Окончить тренировку", callback_data="end_workout")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Удаляем предыдущее сообщение
            try:
                await query.delete_message()
            except Exception as e:
                logger.warning(f"Не удалось удалить сообщение: {e}")
            
            await context.bot.send_message(
                chat_id=user_id,
                text="⏱️ **Тренировка началась!**\n\n"
                     "⏰ Таймер запущен...\n"
                     "💪 Удачной тренировки!\n\n"
                     "Нажми кнопку ниже, когда закончишь:",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            logger.info(f"Сообщение о начале тренировки отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка в start_workout для пользователя {user_id}: {e}")
            # Отправляем сообщение об ошибке
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Произошла ошибка при запуске тренировки. Попробуйте еще раз."
            )

    async def end_workout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Окончание тренировки"""
        query = update.callback_query
        user_id = query.from_user.id
        
        logger.info(f"Пользователь {user_id} закончил тренировку")
        
        try:
            await query.answer()
            
            end_time = datetime.now()
            start_time = user_data[user_id].get('start_time')
            
            if start_time:
                duration = end_time - start_time
                hours, remainder = divmod(duration.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                
                duration_text = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            else:
                duration_text = "Не удалось определить"
            
            keyboard = [
                [InlineKeyboardButton("🔄 Новая тренировка", callback_data="back_to_start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Удаляем предыдущее сообщение
            try:
                await query.delete_message()
            except Exception as e:
                logger.warning(f"Не удалось удалить сообщение: {e}")
            
            await context.bot.send_message(
                chat_id=user_id,
                text="🎉 **Тренировка завершена!**\n\n"
                     f"⏱️ Время тренировки: **{duration_text}**\n"
                     f"🏁 Закончено в: {end_time.strftime('%H:%M:%S')}\n\n"
                     "💪 Отличная работа! Отдохни и восстанавливайся! 🎯",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            logger.info(f"Сообщение о завершении тренировки отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка в end_workout для пользователя {user_id}: {e}")
            # Отправляем сообщение об ошибке
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Произошла ошибка при завершении тренировки."
            )

    async def show_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать историю тренировок (заглушка для будущего функционала)"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("🔄 Новая тренировка", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="📊 **История тренировок**\n\n"
                 "Функционал в разработке...\n"
                 "Здесь будет отображаться ваша статистика! 📈",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Общий обработчик всех кнопок"""
        query = update.callback_query
        logger.info(f"Получен callback: {query.data} от пользователя {query.from_user.id}")
        
        if query.data in ["phase_1", "phase_2"]:
            await self.select_phase(update, context)
        elif query.data in ["days_mwf", "days_tts"]:
            await self.select_days(update, context)
        elif query.data in ["muscle_group_1", "muscle_group_2", "muscle_group_3"]:
            await self.select_muscle_group(update, context)
        elif query.data == "back_to_days":
            await self.back_to_days(update, context)
        elif query.data == "back_to_phases":
            await self.back_to_phases(update, context)
        elif query.data == "start_workout":
            await self.start_workout(update, context)
        elif query.data == "end_workout":
            await self.end_workout(update, context)
        elif query.data == "back_to_start":
            await self.back_to_start(update, context)
        elif query.data == "history":
            await self.show_history(update, context)
        elif query.data == "dev_mode":
            await self.dev_mode(update, context)
        elif query.data == "stop_bot":
            await self.stop_bot(update, context)
        elif query.data == "restart_bot":
            await self.restart_bot(update, context)
        elif query.data == "bot_stats":
            await self.bot_stats(update, context)
        elif query.data == "active_users":
            await self.active_users(update, context)

def main():
    """Запуск бота"""
    bot = WorkoutBot()
    
    try:
        # Создание приложения с дополнительными настройками
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .build()
        )
        
        # Сохраняем ссылку на приложение в боте
        bot.application = application
        
        # Добавление обработчиков
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CallbackQueryHandler(bot.button_handler))
        
        print("🤖 Бот запущен!")
        print(f"🔧 Режим разработчика доступен для ID: {DEVELOPER_ID}")
        print("ℹ️  Узнать свой ID можно у @userinfobot")
        
        # Запуск бота
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        print("🔧 Попробуйте обновить библиотеки командой:")
        print("python -m pip install --upgrade python-telegram-bot httpx")

if __name__ == '__main__':

    main()

