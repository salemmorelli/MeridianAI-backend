from __future__ import annotations

import json
import logging
import os
from urllib import error, request

from catalog import load_catalog

logger = logging.getLogger(__name__)


def _point_catalog_for_triage() -> list[dict]:
    out: list[dict] = []
    for p in load_catalog()["points"]:
        out.append(
            {
                "code": p["id"],
                "who_code": p.get("whoCode", p["id"]),
                "name": p["name"],
                "meridian": p["meridian"],
            }
        )
    return out


POINT_CATALOG = _point_catalog_for_triage()
ALLOWED_POINT_CODES = ", ".join(p["code"] for p in POINT_CATALOG)

KEYWORD_RULES = [
    {
        "keywords": ["stress", "irritability", "anger", "cramps", "period", "menstrual"],
        "meridians": ["liver", "pericardium"],
        "points": ["LV3", "PC6"],
        "why": "Stress and irritability patterns are commonly associated with Liver flow and chest regulation.",
    },
    {
        "keywords": ["nausea", "motion sickness", "anxiety", "palpitations", "chest tight"],
        "meridians": ["pericardium", "stomach"],
        "points": ["PC6", "ST36"],
        "why": "Nausea/anxiety often respond to Pericardium and Stomach balancing points.",
    },
    {
        "keywords": ["headache", "migraine", "neck", "stiffness", "eye strain"],
        "meridians": ["gallbladder", "large-intestine", "governing-vessel"],
        "points": ["GB20", "LI4", "YINTANG"],
        "why": "Head-neck discomfort frequently tracks Gallbladder/LI pathways and calming midline points.",
    },
    {
        "keywords": ["fatigue", "bloating", "digestion", "swelling", "heavy legs"],
        "meridians": ["stomach", "liver"],
        "points": ["ST36", "LV3"],
        "why": "Digestive and heaviness symptoms are often addressed via Stomach and Liver support.",
    },
]


def _catalog_keyword_hits(symptom_text: str) -> list[tuple[int, str, str]]:
    text = symptom_text.lower()
    scored: list[tuple[int, str, str]] = []
    for p in load_catalog()["points"]:
        pid = p["id"]
        mer = p["meridian"]
        score = 0
        for term in p.get("benefits", []) + p.get("matchKeywords", []):
            t = str(term).lower().strip()
            if not t:
                continue
            if t in text:
                score += 3
                continue
            for word in t.split():
                if len(word) > 3 and word in text:
                    score += 1
        if score > 0:
            scored.append((score, pid, mer))
    scored.sort(key=lambda x: -x[0])
    return scored


def _heuristic_triage(symptom_text: str) -> dict:
    text = symptom_text.lower()
    cat_hits = _catalog_keyword_hits(text)
    if cat_hits:
        meridians: list[str] = []
        point_codes: list[str] = []
        for _score, pid, mer in cat_hits:
            if pid not in point_codes:
                point_codes.append(pid)
            if mer not in meridians:
                meridians.append(mer)
            if len(point_codes) >= 6:
                break
        point_objects = []
        for code in point_codes[:4]:
            match = next((p for p in POINT_CATALOG if p["code"] == code), None)
            if match:
                point_objects.append(match)
        return {
            "probable_meridians": meridians[:4],
            "suggested_points": point_objects,
            "rationale": (
                "Matched your wording to curated benefit and keyword tags on each point "
                "(educational heuristic, not a diagnosis)."
            ),
            "source": "heuristic",
        }

    meridians: list[str] = []
    points: list[str] = []
    rationale_parts: list[str] = []

    for rule in KEYWORD_RULES:
        if any(k in text for k in rule["keywords"]):
            for m in rule["meridians"]:
                if m not in meridians:
                    meridians.append(m)
            for p in rule["points"]:
                if p not in points:
                    points.append(p)
            rationale_parts.append(rule["why"])

    if not meridians:
        meridians = ["stomach", "liver"]
    if not points:
        points = ["ST36", "LV3", "PC6"]
    if not rationale_parts:
        rationale_parts = [
            "General balancing suggestion based on common stress/digestion presentations."
        ]

    point_objects = []
    for code in points[:4]:
        match = next((p for p in POINT_CATALOG if p["code"] == code), None)
        if match:
            point_objects.append(match)

    return {
        "probable_meridians": meridians[:4],
        "suggested_points": point_objects,
        "rationale": " ".join(rationale_parts),
        "source": "heuristic",
    }


def _openai_triage(symptom_text: str) -> dict | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set; falling back to heuristic triage")
        return None

    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a MeridianAI triage assistant. "
                    "Return strict JSON with keys: probable_meridians (array of strings), "
                    f"suggested_points (array of point codes from: {ALLOWED_POINT_CODES}), "
                    "rationale (short string)."
                ),
            },
            {
                "role": "user",
                "content": f"User symptom text: {symptom_text}",
            },
        ],
        "temperature": 0.2,
    }

    req = request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        probable_meridians = parsed.get("probable_meridians", [])
        point_codes = parsed.get("suggested_points", [])
        rationale = parsed.get("rationale", "LLM suggestion.")
        points = [p for p in POINT_CATALOG if p["code"] in point_codes][:4]
        if not points:
            return None
        return {
            "probable_meridians": probable_meridians[:4],
            "suggested_points": points,
            "rationale": rationale,
            "source": "llm",
        }
    except (error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as exc:
        logger.error("OpenAI triage failed: %s", exc, exc_info=True)
        return None


def triage_symptom_text(symptom_text: str) -> dict:
    llm = _openai_triage(symptom_text)
    if llm:
        return llm
    return _heuristic_triage(symptom_text)
