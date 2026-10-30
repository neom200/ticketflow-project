import pytest
from pydantic import ValidationError
from app.schemas import TicketInput, TicketClassification


def test_valid_ticket_input():
    ticket = TicketInput(text="Não consigo acessar o sistema.")

    assert ticket.text == "Não consigo acessar o sistema."


def test_empty_ticket_rejected():
    with pytest.raises(ValidationError):
        TicketInput(text="")


def test_ticket_too_long_rejected():
    with pytest.raises(ValidationError):
        TicketInput(text="A" * 2001)


def test_valid_classification():
    result = TicketClassification(
        category="availability",
        priority="critical",
        team="infrastructure",
        system="faturamento",
        location="Curitiba",
        summary="Sistema de faturamento indisponível.",
        action="route",
    )

    assert result.category.value == "availability"
    assert result.priority.value == "critical"


def test_invalid_category_rejected():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="finance",
            priority="high",
            team="general",
            system=None,
            location=None,
            summary="Problema financeiro.",
            action="route",
        )


def test_missing_optional_information():
    result = TicketClassification(
        category="access",
        priority="low",
        team="identity",
        system=None,
        location=None,
        summary="Usuário não consegue acessar sua conta.",
        action="route",
    )

    assert result.system is None
    assert result.location is None

def test_route_action():
    result = TicketClassification(
        category="availability",
        priority="critical",
        team="infrastructure",
        system="faturamento",
        location="Curitiba",
        summary="Sistema de faturamento indisponível.",
        action="route",
    )

    assert result.action.value == "route"
    assert result.missing_information == []
    assert result.clarification_question is None


def test_request_clarification():
    result = TicketClassification(
        category="other",
        priority="low",
        team="general",
        system=None,
        location=None,
        summary="Cliente relata um problema não especificado.",
        action="request_clarification",
        missing_information=["system", "problem_description"],
        clarification_question=(
            "Qual sistema apresenta problemas e o que acontece ao utilizá-lo?"
        ),
    )

    assert result.action.value == "request_clarification"
    assert "system" in result.missing_information
    assert result.clarification_question is not None


def test_invalid_triage_action():
    with pytest.raises(ValidationError):
        TicketClassification(
            category="access",
            priority="medium",
            team="identity",
            system=None,
            location=None,
            summary="Usuário relata dificuldade de acesso.",
            action="solve_problem",
        )