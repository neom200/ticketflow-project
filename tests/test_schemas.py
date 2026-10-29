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
        )


def test_missing_optional_information():
    result = TicketClassification(
        category="access",
        priority="low",
        team="identity",
        system=None,
        location=None,
        summary="Usuário não consegue acessar sua conta.",
    )

    assert result.system is None
    assert result.location is None