# GMGN Volume Monitor

Скрипт для мониторинга объема торгов по токену через API из репозитория
`ChipaDevTeam/GmGnAPI` и вывода результата каждую секунду.

> ⚠️ В среде выполнения отсутствует доступ к GitHub (403), поэтому точные URL
> эндпоинтов из репозитория не были получены автоматически. Скрипт поддерживает
> настройку базового URL и JSON-пути к полю объема через аргументы/переменные
> окружения, чтобы легко подстроить под актуальные эндпоинты из `GmGnAPI`.

## Быстрый старт

```bash
python monitor_volume.py \
  --token YOUR_TOKEN_ADDRESS \
  --base-url "https://api.example.com/v1/tokens/{token}/volume" \
  --volume-path "data.volume"
```

По умолчанию запрос выполняется каждую секунду.

## Аргументы

- `--token` — адрес/идентификатор токена.
- `--base-url` — URL эндпоинта. Можно использовать `{token}` для подстановки.
- `--volume-path` — путь к полю объема в JSON-ответе (через точки).
- `--interval` — интервал в секундах (по умолчанию `1`).
- `--timeout` — таймаут HTTP-запроса (по умолчанию `10`).

## Переменные окружения

- `GMGN_API_URL` — альтернативный способ задать `--base-url`.
- `GMGN_VOLUME_PATH` — альтернативный способ задать `--volume-path`.

## Пример

```bash
export GMGN_API_URL="https://api.example.com/v1/tokens/{token}/stats"
export GMGN_VOLUME_PATH="data.volume24h"
python monitor_volume.py --token So11111111111111111111111111111111111111112
```

Скрипт будет выводить значение объема каждую секунду.
