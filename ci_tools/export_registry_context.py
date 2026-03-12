"""
Script: ci_tools/export_registry_context.py
What: Writes normalized registry context for later workflow steps.
Doing: Computes lowercase image-owner text, the full registry path, and whether
the triggering account is an automation bot, then writes those values to step
outputs and later-step environment variables.
Why: Keeps small but important workflow data-shaping logic out of inline shell.
Goal: Provide one reusable source of truth for registry-path and bot-detection logic.
"""

from __future__ import annotations

from ci_tools.common import normalize_owner, require_env, write_github_env, write_github_outputs


def actor_is_bot(actor_name: str) -> bool:
    """True when the current GitHub account name follows the bot naming pattern."""

    return "[bot]" in actor_name


def main() -> None:
    image_org = normalize_owner(require_env("GITHUB_REPOSITORY_OWNER"))
    image_registry = f"ghcr.io/{image_org}"
    is_bot = "true" if actor_is_bot(require_env("GITHUB_ACTOR")) else "false"

    write_github_env(
        {
            "IMAGE_ORG": image_org,
            "IMAGE_REGISTRY": image_registry,
            "ACTOR_IS_BOT": is_bot,
        }
    )
    write_github_outputs(
        {
            "image_org": image_org,
            "image_registry": image_registry,
            "actor_is_bot": is_bot,
        }
    )

    print(
        "Prepared registry context: "
        f"image_org={image_org} image_registry={image_registry} actor_is_bot={is_bot}"
    )


if __name__ == "__main__":
    main()
