from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
CATALOG_PATH = ROOT_DIR / "data" / "points-catalog.json"


@lru_cache(maxsize=1)
def load_catalog() -> dict:
    if not CATALOG_PATH.is_file():
        raise FileNotFoundError(f"Missing points catalog: {CATALOG_PATH}")
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def clear_catalog_cache() -> None:
    load_catalog.cache_clear()
