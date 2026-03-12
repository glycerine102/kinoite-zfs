"""
Script: tests/test_export_registry_context.py
What: Tests for registry-context export helper logic.
Doing: Verifies lowercase registry-path generation, bot detection, and GitHub output/env writes.
Why: Branch, pull request, and main workflows all rely on one shared registry-context action.
Goal: Keep registry-path and bot-account handling stable across every workflow path.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ci_tools.export_registry_context import actor_is_bot, main


class ExportRegistryContextTests(unittest.TestCase):
    def test_actor_is_bot_matches_github_bot_suffix(self) -> None:
        self.assertTrue(actor_is_bot("dependabot[bot]"))
        self.assertFalse(actor_is_bot("dbaggett"))

    def test_main_writes_outputs_and_env(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "github-output.txt"
            env_path = Path(temp_dir) / "github-env.txt"
            with patch.dict(
                os.environ,
                {
                    "GITHUB_REPOSITORY_OWNER": "Danathar",
                    "GITHUB_ACTOR": "dependabot[bot]",
                    "GITHUB_OUTPUT": str(output_path),
                    "GITHUB_ENV": str(env_path),
                },
                clear=False,
            ):
                main()

            self.assertIn("image_org=danathar", output_path.read_text(encoding="utf-8"))
            self.assertIn("actor_is_bot=true", output_path.read_text(encoding="utf-8"))
            self.assertIn("IMAGE_REGISTRY=ghcr.io/danathar", env_path.read_text(encoding="utf-8"))
            self.assertIn("ACTOR_IS_BOT=true", env_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
