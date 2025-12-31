from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

BlockCategory = Literal["layout", "data", "interaction"]


@dataclass
class BlockSchema:
    """Beskriver en blocktyp som finns i blockbiblioteket."""

    type: str
    category: BlockCategory
    description: str
    required_fields: List[str] = field(default_factory=list)
    optional_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "required_fields": list(self.required_fields),
            "optional_fields": dict(self.optional_fields),
        }


@dataclass
class BlockInstance:
    """En instans av ett block i en app."""

    key: str
    schema: BlockSchema
    config: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "type": self.schema.type,
            "category": self.schema.category,
            "config": self.config,
        }


def _layout_blocks() -> Dict[str, BlockSchema]:
    return {
        "page": BlockSchema(
            type="page",
            category="layout",
            description="Grundlayout för en sida som kan innehålla komponenter och navigering.",
            required_fields=["title"],
            optional_fields={"navigation": []},
        ),
        "card": BlockSchema(
            type="card",
            category="layout",
            description="Kortliknande yta för att gruppera information eller formulär.",
            optional_fields={"icon": None},
        ),
    }


def _data_blocks() -> Dict[str, BlockSchema]:
    return {
        "data-list": BlockSchema(
            type="data-list",
            category="data",
            description="Visar en lista med poster från ett datakälla- eller API-anrop.",
            required_fields=["source"],
            optional_fields={"fields": []},
        ),
        "form": BlockSchema(
            type="form",
            category="data",
            description="Formulär som kan skapa eller uppdatera data.",
            required_fields=["fields"],
            optional_fields={"submit_action": ""},
        ),
    }


def _interaction_blocks() -> Dict[str, BlockSchema]:
    return {
        "action-button": BlockSchema(
            type="action-button",
            category="interaction",
            description="Knapp som kan kopplas till en åtgärd eller ett API-anrop.",
            required_fields=["label"],
            optional_fields={"action": ""},
        ),
        "api-request": BlockSchema(
            type="api-request",
            category="interaction",
            description="Utför ett HTTP-anrop och exponerar resultatet som data för andra block.",
            required_fields=["url", "method"],
            optional_fields={"headers": {}, "body": {}},
        ),
    }


def default_library() -> Dict[str, BlockSchema]:
    """Returnerar ett sammanslaget blockbibliotek för appbyggaren."""

    library: Dict[str, BlockSchema] = {}
    for source in (_layout_blocks(), _data_blocks(), _interaction_blocks()):
        library.update(source)
    return library
