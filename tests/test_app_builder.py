import unittest
from pathlib import Path

from adaptable.app_builder import AppBuilder
from adaptable.blocks import default_library


class AppBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = AppBuilder(name="Demo")

    def test_add_block_requires_fields(self) -> None:
        with self.assertRaises(ValueError):
            self.builder.add_block("page", key="start", config={})

        block = self.builder.add_block("page", key="start", config={"title": "Start"})
        self.assertEqual(block.key, "start")
        self.assertEqual(block.schema.type, "page")

    def test_build_and_reload_blueprint(self) -> None:
        self.builder.add_block("page", key="start", config={"title": "Start"})
        self.builder.add_block(
            "api-request",
            key="hämta",
            config={"url": "https://api.exempel.se", "method": "GET"},
        )
        self.builder.connect("hämta", "start", purpose="provides-data")

        tmp_path = Path("/tmp/blueprint-test.json")
        self.builder.save(tmp_path)

        loaded = AppBuilder.load(tmp_path)
        self.assertEqual(loaded.name, "Demo")
        self.assertIn("start", loaded.blocks)
        self.assertEqual(len(loaded.connections), 1)

    def test_list_library_contains_defaults(self) -> None:
        library = default_library()
        self.assertIn("page", library)
        self.assertIn("form", library)


if __name__ == "__main__":
    unittest.main()
