#!/usr/bin/env python3
import argparse
import os
import sys
import time

from gmgn_client import GmGnConfig, build_url, extract_path, fetch_json, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor trading volume for a token and print it every second."
    )
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
        "--config",
        default=os.getenv("GMGN_CONFIG"),
        help="Path to JSON config with base_url/volume_path/headers",
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


def resolve_config(args: argparse.Namespace) -> GmGnConfig:
    config = load_config(args.config)
    if config:
        return config

    if not args.base_url:
        raise SystemExit("--base-url or GMGN_API_URL is required")

    return GmGnConfig(base_url=args.base_url, volume_path=args.volume_path, headers={})


def main() -> int:
    args = parse_args()
    config = resolve_config(args)
    url = build_url(config.base_url, args.token)

    while True:
        try:
            payload = fetch_json(url, timeout=args.timeout, headers=config.headers)
            volume = extract_path(payload, config.volume_path)
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} volume: {volume}", flush=True)
        except (ValueError, KeyError, IndexError) as exc:
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} error: {exc}",
                file=sys.stderr,
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} error: {exc}",
                file=sys.stderr,
                flush=True,
            )
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
