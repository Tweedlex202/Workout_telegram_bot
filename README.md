# Workout Telegram Bot

Telegram-бот для тренировок с программами упражнений по фазам и дням недели.

## Функционал

- 2 фазы тренировок с разными программами
- Выбор дней: Пн/Ср/Пт или Вт/Чт/Сб
- Таймер тренировки
- Режим разработчика для управления ботом
- Логирование активности

## Требования

- Docker
- Docker Compose
- Telegram Bot Token (получить у @BotFather)

## Установка и запуск

### 1. Клонирование проекта

```bash
git clone <repository-url>
cd workout-bot
```

### 2. Настройка переменных окружения

Скопируйте файл с примером и заполните своими данными:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл:

```
BOT_TOKEN=your_bot_token_here
DEVELOPER_ID=your_telegram_id_here
```

**Как получить данные:**
- `BOT_TOKEN` - получите у @BotFather в Telegram
- `DEVELOPER_ID` - ваш Telegram ID (узнать у @userinfobot)

### 3. Запуск с Docker Compose

```bash
# Сборка и запуск контейнера
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart
```

### 4. Проверка работы

После запуска найдите своего бота в Telegram и отправьте команду `/start`.

## Структура проекта

```
workout-bot/
├── tg_bot.py           # Основной код бота
├── Dockerfile          # Конфигурация Docker образа
├── docker-compose.yml  # Конфигурация Docker Compose
├── requirements.txt    # Python зависимости
├── .env               # Переменные окружения (не в git)
├── .env.example       # Пример переменных окружения
├── logs/              # Папка с логами
└── README.md          # Этот файл
```

## Команды Docker

```bash
# Посмотреть статус контейнера
docker-compose ps

# Войти в контейнер
docker-compose exec workout-bot bash

# Посмотреть логи за последние 100 строк
docker-compose logs --tail=100

# Пересобрать образ
docker-compose build --no-cache

# Остановить и удалить контейнер
docker-compose down --volumes
```

## Развертывание на сервере

### 1. Подготовка сервера

```bash
# Установка Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Копирование файлов

```bash
# Скопировать файлы на сервер
scp -r . user@server:/path/to/workout-bot/

# Или клонировать на сервере
ssh user@server
git clone <repository-url>
cd workout-bot
```

### 3. Запуск на сервере

```bash
# Настроить переменные окружения
cp .env.example .env
nano .env  # заполнить данными

# Запустить
docker-compose up -d --build
```

### 4. Автозапуск при перезагрузке

```bash
# Добавить в crontab
crontab -e

# Добавить строку:
@reboot cd /path/to/workout-bot && docker-compose up -d
```

## Мониторинг

```bash
# Просмотр логов в реальном времени
docker-compose logs -f

# Проверка использования ресурсов
docker stats

# Проверка статуса
docker-compose ps
```

## Режим разработчика

В боте доступен специальный режим для администратора:

- Статистика бота
- Список активных пользователей
- Остановка/перезапуск бота

Доступ имеет только пользователь с ID, указанным в `DEVELOPER_ID`.

## Логи

Логи сохраняются в папку `./logs/bot.log` и дублируются в консоль Docker.

## Обновление

```bash
# Получить изменения
git pull

# Пересобрать и перезапустить
docker-compose down
docker-compose up -d --build
```

## Устранение неполадок

### Бот не отвечает
```bash
# Проверить логи
docker-compose logs

# Проверить статус
docker-compose ps

# Перезапустить
docker-compose restart
```

### Ошибки при сборке
```bash
# Очистить кеш Docker
docker system prune -a

# Пересобрать без кеша
docker-compose build --no-cache
```

### Проблемы с правами
```bash
# Дать права на папку логов
sudo chown -R 1000:1000 logs/
```

## Поддержка

При возникновении проблем проверьте:

1. Правильность BOT_TOKEN
2. Доступность интернета на сервере
3. Логи контейнера
4. Статус контейнера Docker

---

**Версия:** 1.3  
**Python:** 3.11  
**Библиотека:** python-telegram-bot 20.7
