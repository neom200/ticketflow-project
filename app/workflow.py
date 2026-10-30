import json
import os
from pathlib import Path

from pydantic import ValidationError

from app.llm_client import get_client
from app.schemas import TicketInput, TicketClassification
from app.validation import validate_triage


PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "v1.txt"

def classify_ticket(ticket: TicketInput) -> TicketClassification:
    prompt = PROMPT_PATH.read_text(encoding="utf-8")

    client = get_client()

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": ticket.text},
        ],
        response_format={"type": "json_object"},
        temperature=0,
        max_tokens=400,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("LLM returned an empty response.")

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM returned invalid JSON.") from exc

    try:
        result = TicketClassification.model_validate(data)
    except ValidationError as exc:
        raise ValueError("LLM returned an invalid classification.") from exc

    validate_triage(result)

    return result