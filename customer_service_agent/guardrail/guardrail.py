import os
import re
import requests
import time
from dotenv import load_dotenv

load_dotenv()

NER_SERVICE_URL = os.getenv("NER_SERVICE_URL")


REGEX_PATTERNS = {
    "PHONE": r"\b08\d{8,11}\b",
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "NIK": r"\b\d{16}\b",
    "CREDIT_CARD": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"
}

# =============================
# REGEX ENTITY EXTRACTION
# =============================
def extract_regex_entities(text: str):
    entities = []

    for label, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            entities.append({
                "start": match.start(),
                "end": match.end(),
                "label": label
            })

    return entities


# =============================
# NER ENTITY EXTRACTION
# =============================
def extract_ner_entities(text: str):
    start = time.perf_counter()

    response = requests.post(
        NER_SERVICE_URL,
        json={"text": text},
        timeout=5
    )
    response.raise_for_status()

    latency_ms = (time.perf_counter() - start) * 1000

    return response.json().get("entities", []), latency_ms


# =============================
# MASKING FUNCTION
# =============================
def mask_text(text: str, entities: list):
    """
    Mask text using entity offsets
    Format: [REDACTED_{LABEL}]
    """
    masked_text = text

    # IMPORTANT: reverse sort to keep offsets valid
    for ent in sorted(entities, key=lambda x: x["start"], reverse=True):
        label = ent["label"]
        masked_text = (
            masked_text[:ent["start"]]
            + f"[REDACTED_{label}]"
            + masked_text[ent["end"]:]
        )

    return masked_text


# =============================
# MAIN GUARDRAIL PIPELINE
# =============================
def apply_guardrail(text: str):
    """
    Returns:
    {
        allowed: bool,
        safe_text: str,
        entities: list,
        reason: str | None
    }
    """

    # 1️⃣ REGEX ENTITIES
    regex_entities = extract_regex_entities(text)

    # 2️⃣ NER ENTITIES
    ner_entities, ner_latency = extract_ner_entities(text)

    # 3️⃣ MERGE ENTITIES
    all_entities = regex_entities + ner_entities
    
    print(f"NER latency: {ner_latency:.2f} ms")

    if all_entities:
        masked_text = mask_text(text, all_entities)
        labels = sorted({e["label"] for e in all_entities})

        return {
            "allowed": False,
            "safe_text": masked_text,
            "entities": all_entities,
            "reason": f"PII detected: {', '.join(labels)}"
        }

    # 4️⃣ SAFE
    return {
        "allowed": True,
        "safe_text": text,
        "entities": [],
        "reason": None
    }
