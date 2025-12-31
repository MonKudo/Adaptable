from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .app_builder import AppBuilder, list_library
from .blocks import default_library


def _load_or_exit(blueprint_path: Path) -> AppBuilder:
    if not blueprint_path.exists():
        raise SystemExit(f"Hittar ingen blåkopia på {blueprint_path}.")
    data = json.loads(blueprint_path.read_text())
    return AppBuilder.from_blueprint(data)


def _save(builder: AppBuilder, blueprint_path: Path) -> None:
    builder.save(blueprint_path)
    print(f"✅ Sparade blåkopia till {blueprint_path}")


def cmd_init(args: argparse.Namespace) -> None:
    blueprint_path = Path(args.output)
    builder = AppBuilder(name=args.name)
    _save(builder, blueprint_path)


def cmd_add(args: argparse.Namespace) -> None:
    blueprint_path = Path(args.blueprint)
    builder = _load_or_exit(blueprint_path)
    config: Dict[str, Any] = {}
    for item in args.config or []:
        if "=" not in item:
            raise SystemExit("Använd --config key=value för att ange konfiguration.")
        key, value = item.split("=", 1)
        config[key] = value

    builder.add_block(args.type, key=args.key, config=config)
    _save(builder, blueprint_path)


def cmd_connect(args: argparse.Namespace) -> None:
    blueprint_path = Path(args.blueprint)
    builder = _load_or_exit(blueprint_path)
    builder.connect(args.source, args.target, purpose=args.purpose or "")
    _save(builder, blueprint_path)


def cmd_preview(args: argparse.Namespace) -> None:
    blueprint_path = Path(args.blueprint)
    builder = _load_or_exit(blueprint_path)
    print(builder.to_markdown())


def cmd_library(_: argparse.Namespace) -> None:
    library = list_library(default_library())
    for schema in library:
        print(f"- {schema['type']} ({schema['category']}): {schema['description']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bygg appar med block utan att skriva kod.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="Skapa en ny blåkopia")
    init_parser.add_argument("--name", required=True, help="Appens namn")
    init_parser.add_argument("--output", default="blueprint.json", help="Sökväg att spara blåkopia")
    init_parser.set_defaults(func=cmd_init)

    add_parser = sub.add_parser("add", help="Lägg till ett block")
    add_parser.add_argument("--blueprint", default="blueprint.json", help="Befintlig blåkopia att uppdatera")
    add_parser.add_argument("--type", required=True, help="Blocktyp, t.ex. page eller form")
    add_parser.add_argument("--key", required=True, help="Unik nyckel för blocket")
    add_parser.add_argument("--config", nargs="*", help="Blockkonfiguration som key=value par")
    add_parser.set_defaults(func=cmd_add)

    connect_parser = sub.add_parser("connect", help="Koppla ihop två block")
    connect_parser.add_argument("--blueprint", default="blueprint.json", help="Blåkopia att läsa och uppdatera")
    connect_parser.add_argument("--source", required=True, help="Nyckel för källblocket")
    connect_parser.add_argument("--target", required=True, help="Nyckel för målblocket")
    connect_parser.add_argument("--purpose", help="Beskrivning av kopplingen, t.ex. navigates")
    connect_parser.set_defaults(func=cmd_connect)

    preview_parser = sub.add_parser("preview", help="Rendera en enkel översikt")
    preview_parser.add_argument("--blueprint", default="blueprint.json", help="Blåkopia att läsa")
    preview_parser.set_defaults(func=cmd_preview)

    library_parser = sub.add_parser("library", help="Visa tillgängliga blocktyper")
    library_parser.set_defaults(func=cmd_library)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
