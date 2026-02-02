import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional

import requests


@dataclass(frozen=True)
class GmGnConfig:
    base_url: str
    volume_path: str
    headers: Mapping[str, str]


def load_config(path: Optional[str]) -> Optional[GmGnConfig]:
    if not path:
        return None

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    base_url = data.get("base_url")
    volume_path = data.get("volume_path", "data.volume")
    headers = data.get("headers", {})
    if not base_url:
        raise ValueError("config file must include 'base_url'")
    return GmGnConfig(base_url=base_url, volume_path=volume_path, headers=headers)


def build_url(base_url: str, token: str) -> str:
    if "{token}" in base_url:
        return base_url.format(token=token)
    separator = "" if base_url.endswith("/") else "/"
    return f"{base_url}{separator}{token}"


def fetch_json(url: str, timeout: float, headers: Optional[Mapping[str, str]] = None) -> Any:
    response = requests.get(url, timeout=timeout, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_path(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if part == "":
            continue
        if isinstance(current, list):
            try:
                index = int(part)
            except ValueError as exc:
                raise KeyError(
                    f"Expected numeric index for list access, got '{part}'"
                ) from exc
            current = current[index]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(f"Path '{path}' not found (stuck at '{part}')")
    return current
