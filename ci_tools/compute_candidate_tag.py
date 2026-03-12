"""
Script: ci_tools/compute_candidate_tag.py
What: Builds the candidate image tag for one `main` workflow run.
Doing: Combines the current commit prefix with the Fedora version and writes the
result to GitHub step outputs.
Why: Keeps candidate-tag formatting out of inline workflow shell.
Goal: Provide one stable naming rule for `candidate-<sha>-<fedora>` tags.
"""

from __future__ import annotations

from ci_tools.common import require_env, write_github_outputs


def build_candidate_tag(*, github_sha: str, fedora_version: str) -> str:
    """Return one candidate tag like `candidate-deadbee-43`."""

    return f"candidate-{github_sha[:7]}-{fedora_version}"


def main() -> None:
    candidate_tag = build_candidate_tag(
        github_sha=require_env("GITHUB_SHA"),
        fedora_version=require_env("FEDORA_VERSION"),
    )
    write_github_outputs({"candidate_tag": candidate_tag})
    print(f"Candidate image tag: {candidate_tag}")


if __name__ == "__main__":
    main()
