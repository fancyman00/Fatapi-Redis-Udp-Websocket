# FastAPI + Redis + UDP + WebSocket

Шаблон / исследовательский прототип пайплайна телеметрии:

**UDP → Redis Pub/Sub → WebSocket (FastAPI)**

Сервис слушает UDP-пакеты, публикует их в Redis-канал и раздаёт подключённым клиентам по WebSocket в реальном времени.

> Имя репозитория содержит опечатку (`Fatapi` вместо `Fastapi`) — оставлено как есть.

## Архитектура

```
┌─────────────┐     UDP      ┌──────────────┐   PUBLISH   ┌─────────┐
│  Источник   │ ───────────► │  UdpRedis    │ ──────────► │  Redis  │
│  телеметрии │              │  (worker)    │             │ Pub/Sub │
└─────────────┘              └──────────────┘             └────┬────┘
                                                               │ PSUBSCRIBE
                                                               ▼
                                                         ┌───────────┐
                                                         │ FastAPI   │
                                                         │ /ws/{ch}  │
                                                         └─────┬─────┘
                                                               │ WebSocket
                                                               ▼
                                                         ┌───────────┐
                                                         │ Browser / │
                                                         │ клиент    │
                                                         └───────────┘
```

1. `Udp` / `UdpRedis` биндит UDP-сокет и в фоне читает датаграммы
2. Каждая датаграмма публикуется в Redis-канал (`udp-1`, …)
3. WebSocket-эндпоинт подписывается на канал через `PSUBSCRIBE` и стримит данные клиенту

## Структура

```
FatapiRedisUdpWebsocket/
├── app/
│   ├── main.py              # FastAPI + CORS + старт UDP-воркера
│   ├── config.py            # pydantic-settings из app/.env
│   ├── .env.example
│   ├── api/
│   │   └── websocket.py     # WS /ws/{channel}, тест publish
│   ├── model/
│   │   ├── base.py          # Udp (socket + thread worker)
│   │   ├── redis.py         # UdpRedis → redis.publish
│   │   └── websocket.py     # enum состояний WS
│   ├── schemas/
│   │   ├── packet.py        # Message(channel, event, data)
│   │   └── telemetry.py     # InfraredMatrix
│   └── services/
│       ├── redis.py         # async Redis client
│       └── telemetry.py     # фабрика IR-сервиса
├── tests/
│   └── load_test.py         # Locust + websocket load test
├── docker-compose.yml       # Redis :6380
├── Dockerfile
└── requirements.txt
```

## API

| Тип | Путь | Описание |
|-----|------|----------|
| WebSocket | `/ws/{channel}` | Подписка на Redis-канал (pattern subscribe) |
| GET | `/test/{channel}` | Тестовый `PUBLISH` в канал (`"123"`) |

Пример подключения:

```js
const ws = new WebSocket("ws://localhost:8000/ws/udp-1");
ws.onmessage = (e) => console.log(e.data);
```

## Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/fancyman00/FatapiRedisUdpWebsocket.git
cd FatapiRedisUdpWebsocket
```

### 2. Переменные окружения

```bash
cp app/.env.example app/.env
```

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `WEBSERVER_HOST` | `localhost` | хост приложения |
| `WEBSERVER_PORT` | `8000` | порт приложения |
| `REDIS_HOST` | `localhost` | Redis |
| `REDIS_PORT` | `6380` | порт Redis (mapped из compose) |

### 3. Redis

```bash
docker compose up -d
```

Redis будет на `localhost:6380`.

### 4. Приложение

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Документация: http://127.0.0.1:8000/docs

### 5. Нагрузочный тест (опционально)

```bash
pip install locust websocket-client
locust -f tests/load_test.py
```

Тест открывает `ws://localhost:8000/ws/udp-1` и читает сообщения.

## Стек

- Python 3.12, FastAPI, pydantic-settings
- Redis (async `redis`)
- UDP (`socket` + background thread)
- WebSocket (нативный FastAPI)
- Locust (нагрузочные тесты)
- Docker Compose

## Статус проекта

Это **research / prototype**:

- в `main.py` захардкожен IP/порт UDP-источника (`192.168.41.28:40004`) — замените под свою сеть
- `IrTelemetry` импортируется в `services/telemetry.py`, но файла модели в репозитории нет — нужно дописать класс-наследник `UdpRedis` или поправить импорт
- `Dockerfile` пока только ставит зависимости (без `CMD`); удобнее запускать `uvicorn` локально + Redis в compose
- healthcheck Redis в compose выглядит неполным (`redis-cli -a ping`) — для локалки без пароля лучше `redis-cli ping`

Подходит как заготовка realtime-пайплайна для телеметрии / IoT / демо WebSocket+Redis.

## Лицензия

MIT
