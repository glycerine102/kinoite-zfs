"""
Script: tests/test_compose_branch_image_tag.py
What: Tests for final branch-image tag composition.
Doing: Verifies that the precomputed branch-safe prefix is combined with the Fedora version in one stable format.
Why: Branch image publishing should use one predictable naming rule that matches workflow expectations.
Goal: Keep `br-<branch>-<fedora>` naming logic out of workflow shell and under test.
"""

from __future__ import annotations

import unittest

from ci_tools.compose_branch_image_tag import build_branch_image_tag


class ComposeBranchImageTagTests(unittest.TestCase):
    def test_builds_branch_image_tag(self) -> None:
        self.assertEqual(
            build_branch_image_tag(
                branch_tag_prefix="br-my-branch",
                fedora_version="43",
            ),
            "br-my-branch-43",
        )


if __name__ == "__main__":
    unittest.main()
