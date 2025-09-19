import tempfile
import unittest
from pathlib import Path

from glossary_utils import safe_load, safe_load_path


class YamlParsingTestCase(unittest.TestCase):
    def test_colon_in_plain_string_round_trips(self) -> None:
        content = (
            "examples:\n"
            "  do:\n"
            "    - Run quarterly tabletop drills\n"
            "  dont:\n"
            "    - \"Silence alerts: skip postmortems once the incident is closed\"\n"
        )

        expected = "Silence alerts: skip postmortems once the incident is closed"

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "term.yml"
            file_path.write_text(content, encoding="utf-8")

            for payload in (safe_load(content), safe_load_path(file_path)):
                dont_examples = payload["examples"]["dont"]
                self.assertEqual(dont_examples, [expected])


if __name__ == "__main__":
    unittest.main()
