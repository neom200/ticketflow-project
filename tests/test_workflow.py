from unittest.mock import MagicMock, patch

import pytest

from app.schemas import TicketInput
from app.workflow import classify_ticket


@patch("app.workflow.get_client")
def test_classify_ticket_success(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(
            message=MagicMock(
                content="""{
                    "category": "availability",
                    "priority": "critical",
                    "team": "infrastructure",
                    "system": "faturamento",
                    "location": "Curitiba",
                    "summary": "Sistema indisponível.",
                    "action": "route",
                    "missing_information": [],
                    "clarification_question": null
                }"""
            )
        )
    ]

    result = classify_ticket(
        TicketInput(text="Sistema de faturamento fora do ar em Curitiba.")
    )

    assert result.category.value == "availability"
    assert result.action.value == "route"
    mock_client.chat.completions.create.assert_called_once()


@patch("app.workflow.get_client")
def test_classify_ticket_invalid_json(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="isto não é JSON"))
    ]

    with pytest.raises(ValueError, match="invalid JSON"):
        classify_ticket(TicketInput(text="Sistema lento."))


@patch("app.workflow.get_client")
def test_classify_ticket_invalid_triage(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(
            message=MagicMock(
                content="""{
                    "category": "availability",
                    "priority": "critical",
                    "team": "infrastructure",
                    "system": null,
                    "location": null,
                    "summary": "Sistema indisponível.",
                    "action": "request_clarification",
                    "missing_information": ["system"],
                    "clarification_question": "Qual sistema?"
                }"""
            )
        )
    ]

    with pytest.raises(ValueError, match="Critical tickets"):
        classify_ticket(TicketInput(text="Todos os sistemas estão fora do ar."))