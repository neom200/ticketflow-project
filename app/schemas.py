from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class Category(str, Enum):
    ACCESS = "access"
    AVAILABILITY = "availability"
    PERFORMANCE = "performance"
    DATA_QUALITY = "data_quality"
    OTHER = "other"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Team(str, Enum):
    IDENTITY = "identity"
    INFRASTRUCTURE = "infrastructure"
    DATA = "data"
    GENERAL = "general"

class TriageAction(str, Enum):
    ROUTE = "route"
    REQUEST_CLARIFICATION = "request_clarification"


class TicketInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=2000)


class TicketClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Category
    priority: Priority
    team: Team
    system: str | None
    location: str | None
    summary: str = Field(min_length=1, max_length=500)
    action: TriageAction
    missing_information: list[str] = Field(default_factory=list)
    clarification_question: str | None = None