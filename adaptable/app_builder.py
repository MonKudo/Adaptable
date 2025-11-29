from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .blocks import BlockInstance, BlockSchema, default_library


@dataclass
class Connection:
    """Kopplar ihop två block för att signalera ett flöde."""

    source: str
    target: str
    purpose: str = ""  # ex. "navigates", "provides-data"

    def to_dict(self) -> Dict[str, str]:
        return {"source": self.source, "target": self.target, "purpose": self.purpose}


@dataclass
class AppBuilder:
    """Samlar block och relationer till en app-blåkopior."""

    name: str
    library: Dict[str, BlockSchema] = field(default_factory=default_library)
    blocks: Dict[str, BlockInstance] = field(default_factory=dict)
    connections: List[Connection] = field(default_factory=list)

    def add_block(self, block_type: str, key: str, config: Optional[Dict[str, object]] = None) -> BlockInstance:
        if block_type not in self.library:
            raise KeyError(f"Blocktypen '{block_type}' finns inte i biblioteket.")

        if key in self.blocks:
            raise ValueError(f"Ett block med nyckeln '{key}' finns redan.")

        config = config or {}
        schema = self.library[block_type]
        missing = [field for field in schema.required_fields if field not in config]
        if missing:
            raise ValueError(f"Saknade obligatoriska fält för '{block_type}': {', '.join(missing)}")

        instance = BlockInstance(key=key, schema=schema, config=config)
        self.blocks[key] = instance
        return instance

    def connect(self, source: str, target: str, purpose: str = "") -> Connection:
        if source not in self.blocks:
            raise ValueError(f"Källblocket '{source}' saknas.")

        if target not in self.blocks:
            raise ValueError(f"Målblocket '{target}' saknas.")

        connection = Connection(source=source, target=target, purpose=purpose)
        self.connections.append(connection)
        return connection

    def blueprint(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "blocks": [block.to_dict() for block in self.blocks.values()],
            "connections": [connection.to_dict() for connection in self.connections],
        }

    def save(self, destination: Path | str) -> Path:
        path = Path(destination)
        data = self.blueprint()
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return path

    @classmethod
    def from_blueprint(cls, blueprint: Dict[str, object]) -> "AppBuilder":
        name = blueprint.get("name", "Namnlös app")
        builder = cls(name=name)
        blocks = blueprint.get("blocks", [])
        for block in blocks:
            block_type = block["type"]
            key = block["key"]
            config = block.get("config", {})
            builder.add_block(block_type=block_type, key=key, config=config)

        for connection in blueprint.get("connections", []):
            builder.connect(
                source=connection.get("source", ""),
                target=connection.get("target", ""),
                purpose=connection.get("purpose", ""),
            )

        return builder

    @classmethod
    def load(cls, blueprint_path: Path | str) -> "AppBuilder":
        path = Path(blueprint_path)
        if not path.exists():
            raise FileNotFoundError(f"Hittar ingen blåkopia på {path}.")

        blueprint = json.loads(path.read_text())
        return cls.from_blueprint(blueprint)

    def to_markdown(self) -> str:
        """Genererar en textuell översikt som är enkel att dela inom organisationen."""

        lines = [f"# {self.name}", "", "## Block", ""]
        for block in self.blocks.values():
            lines.append(f"- **{block.key}** ({block.schema.type}) - {block.schema.description}")
            for field, value in block.config.items():
                lines.append(f"  - {field}: {value}")
            lines.append("")

        if self.connections:
            lines.extend(["## Kopplingar", ""])
            for connection in self.connections:
                arrow = "➡" if connection.purpose == "" else f"➡ ({connection.purpose})"
                lines.append(f"- {connection.source} {arrow} {connection.target}")

        return "\n".join(lines).strip() + "\n"


def list_library(library: Optional[Dict[str, BlockSchema]] = None) -> List[Dict[str, str]]:
    """Returnerar en lättläst lista av blocktyper och beskrivningar."""

    schema_library = library or default_library()
    return [asdict(schema) for schema in schema_library.values()]
