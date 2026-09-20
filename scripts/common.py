#!/usr/bin/env python3
"""Fonctions communes aux scripts Cisco Legacy."""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import yaml
from netmiko import ConnectHandler

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs"
LOGS = ROOT / "logs"


def setup(name: str) -> logging.Logger:
    OUTPUT.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(LOGS / f"{name}.log"), logging.StreamHandler()])
    return logging.getLogger(name)


def parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("-i", "--inventory", default="inventory.yml")
    p.add_argument("-w", "--workers", type=int, default=10)
    return p


def devices(path: str) -> list[dict[str, Any]]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    user, password, secret = (os.getenv("CISCO_USERNAME"), os.getenv("CISCO_PASSWORD"), os.getenv("CISCO_SECRET", ""))
    if not user or not password:
        raise SystemExit("Définir CISCO_USERNAME et CISCO_PASSWORD.")
    result = []
    for item in data.get("devices", []):
        d = dict(item); d.setdefault("device_type", "cisco_ios")
        d.update(username=user, password=password, secret=secret)
        result.append(d)
    return result


def run(device: dict[str, Any], command: str, structured: bool = False) -> Any:
    params = {k: v for k, v in device.items() if k != "name"}
    with ConnectHandler(**params) as conn:
        if device.get("secret"): conn.enable()
        return conn.send_command(command, use_textfsm=structured)


def parallel(items: list[dict[str, Any]], fn: Callable, workers: int) -> list[Any]:
    out = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fn, d): d for d in items}
        for future in as_completed(futures):
            d = futures[future]
            try: out.append(future.result())
            except Exception as exc: out.append({"device": d.get("name", d["host"]), "error": str(exc)})
    return out


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def write_json(name: str, data: Any) -> Path:
    path = OUTPUT / f"{name}_{stamp()}.json"; path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"); return path


def write_csv(name: str, rows: list[dict[str, Any]]) -> Path:
    path = OUTPUT / f"{name}_{stamp()}.csv"
    fields = sorted({k for row in rows for k in row}) or ["result"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return path


def flatten(device: str, value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list): return [dict(device=device, **x) if isinstance(x, dict) else {"device": device, "value": x} for x in value]
    return [{"device": device, "raw": str(value)}]

