# FullStack веб-розробка на Python — ДЗ 3

Простий веб-додаток на `http.server` (stdlib) з маршрутизацією, обробкою форм,
рендером через Jinja2 та збереженням повідомлень у JSON-файл.

## Функціонал

- `GET /` — головна сторінка `index.html`
- `GET /message` — сторінка з формою `message.html`
- `POST /message` — приймає `username` + `message`, дописує у `storage/data.json` з ключем `datetime.now()`
- `GET /read` — шаблон Jinja2 `read.html` зі списком усіх повідомлень
- Статика: `/style.css`, `/logo.png` (MIME визначається через `mimetypes`)
- 404 → `error.html`
- Порт: `3000`

## Структура

```
homework_3/
├── main.py            # HTTP-сервер + HttpHandler
├── index.html         # Головна
├── message.html       # Форма
├── read.html          # Jinja2-шаблон зі списком повідомлень
├── error.html         # 404
├── style.css          # Статика
├── logo.png           # Статика
├── storage/
│   └── data.json      # Створюється автоматично після першого POST
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Запуск локально

Через `uv`:

```bash
uv sync
uv run main.py
```

Відкрити в браузері: http://localhost:3000

## Формат storage/data.json

```json
{
  "2022-10-29 20:20:58.020261": {
    "username": "krabaton",
    "message": "First message"
  }
}
```

## Docker

Збірка образу:

```bash
docker build -t homework3 .
```

Запуск з volume (дані `data.json` зберігаються поза контейнером у локальній теці `./storage`):

```bash
docker run --name homework3 -d -p 3000:3000 -v $(pwd)/storage:/app/storage homework3
```

Логи:

```bash
docker logs -f homework3
```

Зупинка / видалення:

```bash
docker stop homework3 && docker rm homework3
```

## Залежності

- Python 3.14+
- `jinja2`
