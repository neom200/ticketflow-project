import pytest

from app.schemas import TicketClassification
from app.validation import validate_triage


def make_ticket(**overrides):
    data = {
        "category": "availability",
        "priority": "medium",
        "team": "infrastructure",
        "system": "faturamento",
        "location": None,
        "summary": "Problema no sistema de faturamento.",
        "action": "route",
        "missing_information": [],
        "clarification_question": None,
    }

    data.update(overrides)
    return TicketClassification(**data)


def test_valid_route():
    validate_triage(make_ticket())


def test_valid_clarification():
    ticket = make_ticket(
        action="request_clarification",
        missing_information=["problem_description"],
        clarification_question="O que acontece ao utilizar o sistema?",
    )

    validate_triage(ticket)


def test_clarification_without_missing_information():
    ticket = make_ticket(
        action="request_clarification",
        missing_information=[],
        clarification_question="Qual é o problema?",
    )

    with pytest.raises(ValueError):
        validate_triage(ticket)


def test_clarification_without_question():
    ticket = make_ticket(
        action="request_clarification",
        missing_information=["problem_description"],
        clarification_question=None,
    )

    with pytest.raises(ValueError):
        validate_triage(ticket)


def test_route_with_clarification_question():
    ticket = make_ticket(
        action="route",
        clarification_question="Qual é o problema?",
    )

    with pytest.raises(ValueError):
        validate_triage(ticket)


def test_critical_ticket_cannot_wait_for_clarification():
    ticket = make_ticket(
        priority="critical",
        action="request_clarification",
        missing_information=["location"],
        clarification_question="Qual é a localização?",
    )

    with pytest.raises(ValueError):
        validate_triage(ticket)