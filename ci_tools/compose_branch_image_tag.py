"""
Script: ci_tools/compose_branch_image_tag.py
What: Builds the final branch image tag after the branch-safe prefix is known.
Doing: Appends the Fedora version to the precomputed branch tag prefix and
writes the result to GitHub step outputs.
Why: Keeps branch image tag formatting out of inline workflow shell.
Goal: Provide one stable naming rule for `br-<branch>-<fedora>` tags.
"""

from __future__ import annotations

from ci_tools.common import require_env, write_github_outputs


def build_branch_image_tag(*, branch_tag_prefix: str, fedora_version: str) -> str:
    """Return one branch image tag like `br-my-branch-43`."""

    return f"{branch_tag_prefix}-{fedora_version}"


def main() -> None:
    branch_image_tag = build_branch_image_tag(
        branch_tag_prefix=require_env("BRANCH_TAG_PREFIX"),
        fedora_version=require_env("FEDORA_VERSION"),
    )
    write_github_outputs({"branch_image_tag": branch_image_tag})
    print(f"Branch image tag: {branch_image_tag}")


if __name__ == "__main__":
    main()
