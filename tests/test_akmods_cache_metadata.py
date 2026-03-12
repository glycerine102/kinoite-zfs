"""
Script: tests/test_akmods_cache_metadata.py
What: Tests for shared akmods cache metadata helpers.
Doing: Verifies label generation/parsing and the tiny metadata-image publish command sequence.
Why: The metadata sidecar is the new fast path for cache reuse checks.
Goal: Keep cache metadata explicit, parseable, and cheap to publish.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch

from ci_tools.akmods_cache_metadata import (
    AKMODS_CACHE_KERNEL_RELEASES_LABEL,
    metadata_labels,
    parse_kernel_releases_from_labels,
    publish_shared_cache_metadata,
    shared_cache_metadata_tag,
)


class AkmodsCacheMetadataTests(unittest.TestCase):
    def test_metadata_labels_sort_and_deduplicate_kernel_releases(self) -> None:
        labels = metadata_labels(
            kernel_flavor="main",
            akmods_version="43",
            kernel_releases=[
                "6.18.16-200.fc43.x86_64",
                "6.18.13-200.fc43.x86_64",
                "6.18.16-200.fc43.x86_64",
            ],
        )
        self.assertEqual(
            labels[AKMODS_CACHE_KERNEL_RELEASES_LABEL],
            "6.18.13-200.fc43.x86_64 6.18.16-200.fc43.x86_64",
        )

    def test_parse_kernel_releases_from_labels_requires_expected_key(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "missing required key"):
            parse_kernel_releases_from_labels({})

    def test_publish_shared_cache_metadata_builds_and_pushes_sidecar_image(self) -> None:
        with patch("ci_tools.akmods_cache_metadata.run_cmd") as run_cmd:
            publish_shared_cache_metadata(
                image_org="danathar",
                akmods_repo="zfs-kinoite-containerfile-akmods",
                kernel_flavor="main",
                akmods_version="43",
                kernel_releases=[
                    "6.18.13-200.fc43.x86_64",
                    "6.18.16-200.fc43.x86_64",
                ],
            )

        build_call = run_cmd.call_args_list[0]
        self.assertEqual(build_call.args[0][:4], ["podman", "build", "-f", build_call.args[0][3]])
        self.assertIn(
            f"localhost/zfs-kinoite-containerfile-akmods:{shared_cache_metadata_tag(kernel_flavor='main', akmods_version='43')}",
            build_call.args[0],
        )
        self.assertIn("--label", build_call.args[0])
        self.assertEqual(
            run_cmd.call_args_list[1],
            call(
                [
                    "podman",
                    "push",
                    "localhost/zfs-kinoite-containerfile-akmods:main-43-metadata",
                    "docker://ghcr.io/danathar/zfs-kinoite-containerfile-akmods:main-43-metadata",
                ],
                capture_output=False,
            ),
        )


if __name__ == "__main__":
    unittest.main()
