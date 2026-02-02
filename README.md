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

## Конфиг

Если у вас есть локальный клон `GmGnAPI`, можно сохранить конфигурацию
эндпоинта в JSON и передать в `--config`:

```json
{
  "base_url": "https://api.example.com/v1/tokens/{token}/stats",
  "volume_path": "data.volume24h",
  "headers": {
    "Authorization": "Bearer <token>"
  }
}
```

Запуск:

```bash
python monitor_volume.py --token So11111111111111111111111111111111111111112 \
  --config gmgn_config.json
```

## Аргументы

- `--token` — адрес/идентификатор токена.
- `--base-url` — URL эндпоинта. Можно использовать `{token}` для подстановки.
- `--volume-path` — путь к полю объема в JSON-ответе (через точки).
- `--config` — путь к JSON-конфигу с `base_url`/`volume_path`/`headers`.
- `--interval` — интервал в секундах (по умолчанию `1`).
- `--timeout` — таймаут HTTP-запроса (по умолчанию `10`).

## Переменные окружения

- `GMGN_API_URL` — альтернативный способ задать `--base-url`.
- `GMGN_VOLUME_PATH` — альтернативный способ задать `--volume-path`.
- `GMGN_CONFIG` — путь к JSON-конфигу (альтернатива `--config`).

## Пример

```bash
export GMGN_API_URL="https://api.example.com/v1/tokens/{token}/stats"
export GMGN_VOLUME_PATH="data.volume24h"
python monitor_volume.py --token So11111111111111111111111111111111111111112
```

Скрипт будет выводить значение объема каждую секунду.
