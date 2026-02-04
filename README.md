# 🏋️ Workout Telegram Bot

> Telegram-бот для персональных тренировок с программами упражнений, таймером и отслеживанием прогресса

## ✨ Возможности

- 📅 2 фазы тренировок с разными программами
- 🗓️ Выбор дней: Пн/Ср/Пт или Вт/Чт/Сб
- ⏱️ Встроенный таймер тренировки
- 👨‍💻 Режим разработчика для управления
- 📊 Логирование активности

## 🚀 Быстрый старт

### 1️⃣ Клонирование проекта

```bash
git clone <repository-url>
cd workout-bot
```

### 2️⃣ Настройка переменных

```bash
cp .env.example .env
nano .env
```

Заполните данные:
```env
BOT_TOKEN=your_bot_token_here    # от @BotFather
DEVELOPER_ID=your_telegram_id    # от @userinfobot
```

### 3️⃣ Запуск

```bash
docker-compose up -d --build
```

✅ **Готово!** Найдите бота в Telegram и отправьте `/start`

## 📋 Основные команды

```bash
# 🔍 Просмотр логов
docker-compose logs -f

# 🔄 Перезапуск
docker-compose restart

# ⛔ Остановка
docker-compose down

# 🔧 Обновление
git pull && docker-compose up -d --build
```

## 📁 Структура

```
workout-bot/
├── 🐍 tg_bot.py
├── 🐳 Dockerfile
├── ⚙️ docker-compose.yml
├── 📦 requirements.txt
├── 🔐 .env
└── 📝 logs/
```

## 🖥️ Развертывание на сервере

### Ubuntu/Debian

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Клонирование и запуск
git clone <repository-url>
cd workout-bot
cp .env.example .env
nano .env  # заполнить данными
docker-compose up -d --build
```

### Автозапуск

```bash
crontab -e
# Добавить:
@reboot cd /path/to/workout-bot && docker-compose up -d
```

## 🔧 Устранение неполадок

| Проблема | Решение |
|----------|---------|
| 🔴 Бот не отвечает | `docker-compose logs` → `docker-compose restart` |
| 🔴 Ошибки сборки | `docker system prune -a` → `docker-compose build --no-cache` |
| 🔴 Проблемы с правами | `sudo chown -R 1000:1000 logs/` |

## 📊 Мониторинг

```bash
docker-compose ps          # Статус
docker stats              # Ресурсы
docker-compose logs -f    # Логи в реальном времени
```

## 👨‍💼 Режим разработчика

Доступен только для `DEVELOPER_ID`:
- 📈 Статистика бота
- 👥 Список пользователей
- 🔄 Управление ботом

---

**⚡ Стек:** Python 3.11 • python-telegram-bot 20.7 • Docker  
**📄 Версия:** 1.3
