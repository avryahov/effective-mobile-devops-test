# Effective Mobile DevOps Test Task

Проект поднимает два контейнера:

- `backend` с простым HTTP-сервером на Python
- `nginx` как reverse proxy

## Структура

```text
.
├── backend
│   ├── .dockerignore
│   ├── app.py
│   └── Dockerfile
├── nginx
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Запуск

1. Убедитесь, что установлены Docker и Docker Compose.
2. Запустите проект:

```bash
docker compose up --build -d
```

## Проверка

После запуска выполните:

```bash
curl http://localhost
```

Ожидаемый ответ:

```text
Hello from Effective Mobile!
```

## Как это работает

1. `backend` слушает порт `8080` только внутри docker-сети.
2. `nginx` слушает порт `80` на хосте.
3. `nginx` проксирует запросы на сервис `backend` по имени сервиса Docker Compose.

Схема взаимодействия:

```text
client -> localhost:80 -> nginx -> backend:8080
```

## Использованные технологии

- Docker
- Docker Compose
- Nginx
- Python 3.12

## Замечания по реализации

- Базовый образ backend: `python:3.12-alpine`
- Процесс backend запускается от непривилегированного пользователя
- В build context backend исключены служебные Python-файлы через `.dockerignore`
