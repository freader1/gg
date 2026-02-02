#!/usr/bin/env python3
import argparse
import os
import sys
import time
from typing import Any

import requests


def extract_path(payload: Any, path: str) -> Any:
    current = payload
    for part in path.split("."):
        if part == "":
            continue
        if isinstance(current, list):
            index = int(part)
            current = current[index]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(f"Path '{path}' not found (stuck at '{part}')")
    return current


def build_url(base_url: str, token: str) -> str:
    if "{token}" in base_url:
        return base_url.format(token=token)
    separator = "" if base_url.endswith("/") else "/"
    return f"{base_url}{separator}{token}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor trading volume for a token and print it every second.")
    parser.add_argument("--token", required=True, help="Token address or symbol")
    parser.add_argument(
        "--base-url",
        default=os.getenv("GMGN_API_URL"),
        help="API endpoint base URL (can include {token})",
    )
    parser.add_argument(
        "--volume-path",
        default=os.getenv("GMGN_VOLUME_PATH", "data.volume"),
        help="Dot-separated JSON path to the volume value",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Polling interval in seconds",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP request timeout in seconds",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.base_url:
        raise SystemExit("--base-url or GMGN_API_URL is required")

    url = build_url(args.base_url, args.token)

    while True:
        try:
            response = requests.get(url, timeout=args.timeout)
            response.raise_for_status()
            payload = response.json()
            volume = extract_path(payload, args.volume_path)
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} volume: {volume}", flush=True)
        except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} error: {exc}",
                file=sys.stderr,
                flush=True,
            )
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
