import asyncio
import json
import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List, Set
from dotenv import load_dotenv

from agents import Runner, set_default_openai_key
from agent import generator_agent, BatchOutput

load_dotenv()

set_default_openai_key(os.getenv("OPENAI_API_KEY"))

OUTPUT_PATH = Path("dataset.jsonl")

NUM_SAMPLES = 3000
BATCH_SIZE = 50
PARALLEL_CALLS = 15

def hash_email(text: str) -> str:
    """Stable dedup key for an email body."""
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()


def load_existing_hashes() -> Set[str]:
    """Read existing file to avoid adding duplicates."""
    if not OUTPUT_PATH.exists():
        return set()
    hashes = set()
    with OUTPUT_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                hashes.add(hash_email(obj["email"]))
            except Exception:
                continue
    return hashes


def append_samples(samples: List[Dict[str, Any]]) -> None:
    """Append new samples to JSONL file."""
    with OUTPUT_PATH.open("a", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

async def generate_one_batch(existing_hashes: Set[str]) -> List[Dict[str, Any]]:
    msg = f"Generate one BATCH of {BATCH_SIZE} original, non-duplicate emails."
    result = await Runner.run(generator_agent, input=msg)
    if not result.final_output or not isinstance(result.final_output, BatchOutput):
        print("[WARN] Agent did not return a valid BatchOutput.")
        return []

    cleaned = []
    for item in result.final_output.emails:
        email = item.email.strip()
        label = item.label.strip().lower()
        
        if not email:
            continue
            
        h = hash_email(email)
        if h not in existing_hashes:
            existing_hashes.add(h)
            cleaned.append({
                "email": email,
                "label": label
            })

    print(f"[BATCH] generated: {len(cleaned)} new emails")
    return cleaned


async def main():
    if OUTPUT_PATH.exists():
        print(f"Removing previous dataset: {OUTPUT_PATH}")
        OUTPUT_PATH.unlink()

    print("Loading existing hashes...")
    existing_hashes = load_existing_hashes()
    print(f"→ {len(existing_hashes)} hashes loaded.")

    generated_total = len(existing_hashes)

    print(f"Target: {NUM_SAMPLES} samples")
    print("Generating...\n")

    while generated_total < NUM_SAMPLES:
        remaining = NUM_SAMPLES - generated_total
        batches_needed = (remaining + BATCH_SIZE - 1) // BATCH_SIZE
        parallel = min(PARALLEL_CALLS, batches_needed)

        if parallel == 0:
            break
        tasks = [
            asyncio.create_task(generate_one_batch(existing_hashes))
            for _ in range(parallel)
        ]

        results = await asyncio.gather(*tasks)
        batch_samples = [x for batch in results for x in batch]
        if batch_samples:
            append_samples(batch_samples)
            generated_total += len(batch_samples)
            print(f"Accumulated: {generated_total}/{NUM_SAMPLES}\n")
        else:
            print("[WARN] No new samples this cycle (duplicates or errors).\n")

    print("✓ Dataset complete.")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
