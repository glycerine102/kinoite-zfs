"""
Script: tests/test_compute_candidate_tag.py
What: Tests for candidate-tag helper logic.
Doing: Verifies the naming rule used by the `main` workflow when it creates a candidate image tag.
Why: Candidate and stable promotion depend on a stable, predictable candidate-tag format.
Goal: Keep `candidate-<sha>-<fedora>` naming simple and consistent.
"""

from __future__ import annotations

import unittest

from ci_tools.compute_candidate_tag import build_candidate_tag


class ComputeCandidateTagTests(unittest.TestCase):
    def test_builds_candidate_tag_from_sha_and_fedora_version(self) -> None:
        self.assertEqual(
            build_candidate_tag(
                github_sha="deadbeefcafebabefeedface1234567890abcdef",
                fedora_version="43",
            ),
            "candidate-deadbee-43",
        )


if __name__ == "__main__":
    unittest.main()
