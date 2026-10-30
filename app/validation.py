from app.schemas import TicketClassification, TriageAction, Priority


def validate_triage(result: TicketClassification) -> None:
    if result.priority == Priority.CRITICAL:
        if result.action != TriageAction.ROUTE:
            raise ValueError(
                "Critical tickets must be routed immediately."
            )

    if result.action == TriageAction.REQUEST_CLARIFICATION:
        if not result.missing_information:
            raise ValueError(
                "Clarification requires missing information."
            )

        if not result.clarification_question:
            raise ValueError(
                "Clarification requires a question."
            )

    if result.action == TriageAction.ROUTE:
        if result.clarification_question is not None:
            raise ValueError(
                "Routed tickets cannot have a clarification question."
            )