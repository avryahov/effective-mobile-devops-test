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
│   ├── Dockerfile
│   └── start.sh
├── keys
│   └── .gitkeep
├── nginx
│   └── nginx.conf
├── secrets
│   └── backend_response.txt.example
├── .env.example
├── docker-compose.yml
└── README.md
```

## Запуск

1. Убедитесь, что установлены Docker и Docker Compose.
2. При необходимости создайте локальные файлы конфигурации:

```bash
cp .env.example .env
cp secrets/backend_response.txt.example secrets/backend_response.txt
```

3. Запустите проект:

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
4. Для обоих сервисов настроены healthcheck, а `nginx` стартует после готовности `backend`.
5. Текст ответа backend может безопасно читаться из файла `secrets/backend_response.txt`, который не коммитится в git.

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
- Параметры compose вынесены в `.env`
- Локальные секреты и ключи не хранятся в git: используются `secrets/*.example` и каталог `keys/`
- Для контейнеров включены `read_only`, `tmpfs`, `cap_drop` и `no-new-privileges`
- Для сервисов заданы явные resource limits: `cpus`, `mem_limit`, `pids_limit`, `ulimits`

## Работа с секретами и ключами

- `.env.example` содержит только шаблон переменных окружения без чувствительных данных
- реальный `.env` добавлен в `.gitignore`
- файл `secrets/backend_response.txt` читается контейнером как секрет и не попадает в репозиторий
- каталог `keys/` зарезервирован под локальные сертификаты или ключи и также игнорируется git
