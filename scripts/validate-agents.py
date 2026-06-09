#!/usr/bin/env python3
"""
Validate the universal-ai-agents monorepo conventions.

Checks, for every agent under agents/<name>/:
  - Required files exist: AGENTS.md (canonical), CLAUDE.md & GEMINI.md (adapters),
    config/config.example.yaml, config/profiles/example.yaml, output/.gitkeep
  - Adapters actually import the canonical manual (contain "@AGENTS.md")
  - config.example.yaml parses and has the expected top-level keys

Repo-wide checks:
  - Every tracked *.yaml / *.yml parses
  - No personal data is tracked (a committed config/config.yaml, a non-example
    profile, or anything under output/<user>/ fails the build)

Run locally:  pip install pyyaml && python3 scripts/validate-agents.py
Exit code 0 = OK, 1 = violations found.
"""
from __future__ import annotations
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(ROOT, "agents")

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except ImportError:  # local runs without PyYAML: structure still checked
    HAVE_YAML = False

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def tracked_files() -> list[str]:
    """Files git is tracking (used for the privacy guards)."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout
        return [line for line in out.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        warnings.append("git not available — skipping tracked-file privacy checks")
        return []


def parse_yaml(path: str):
    if not HAVE_YAML:
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def check_agent(name: str) -> None:
    base = os.path.join(AGENTS_DIR, name)
    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "GEMINI.md",
        "config/config.example.yaml",
        "config/profiles/example.yaml",
        "output/.gitkeep",
    ]
    for rel in required:
        if not os.path.isfile(os.path.join(base, rel)):
            err(f"[{name}] missing required file: {rel}")

    # Adapters must import the canonical manual, not duplicate it.
    for adapter in ("CLAUDE.md", "GEMINI.md"):
        p = os.path.join(base, adapter)
        if os.path.isfile(p):
            with open(p, "r", encoding="utf-8") as fh:
                if "@AGENTS.md" not in fh.read():
                    err(f"[{name}] {adapter} must import the canonical manual via '@AGENTS.md'")

    # config.example.yaml shape.
    cfg = os.path.join(base, "config/config.example.yaml")
    if os.path.isfile(cfg) and HAVE_YAML:
        try:
            data = parse_yaml(cfg) or {}
            for key in ("active_profile", "scoring", "application"):
                if key not in data:
                    err(f"[{name}] config.example.yaml missing top-level key: {key}")
        except Exception as e:  # noqa: BLE001
            err(f"[{name}] config.example.yaml does not parse: {e}")


def main() -> int:
    if not os.path.isdir(AGENTS_DIR):
        err("agents/ directory not found")
        return finish()

    agent_names = sorted(
        d for d in os.listdir(AGENTS_DIR)
        if os.path.isdir(os.path.join(AGENTS_DIR, d))
    )
    if not agent_names:
        err("no agents found under agents/")
    for name in agent_names:
        check_agent(name)

    # Privacy guards + YAML parse over everything git tracks.
    for rel in tracked_files():
        # Personal data must never be committed.
        if rel.endswith("/config/config.yaml"):
            err(f"personal data tracked: {rel} (config.yaml must be gitignored)")
        if "/config/profiles/" in rel and not rel.endswith("/profiles/example.yaml"):
            err(f"personal profile tracked: {rel} (only example.yaml may be committed)")
        # output/.gitkeep is fine; output/<user>/... is not.
        if "/output/" in rel and not rel.endswith("/output/.gitkeep"):
            err(f"generated output tracked: {rel} (output/<user>/ must be gitignored)")
        # Every tracked YAML must parse.
        if rel.endswith((".yaml", ".yml")) and HAVE_YAML:
            try:
                parse_yaml(os.path.join(ROOT, rel))
            except Exception as e:  # noqa: BLE001
                err(f"YAML does not parse: {rel}: {e}")

    if not HAVE_YAML:
        warnings.append("PyYAML not installed — YAML parse checks skipped "
                        "(run: pip install pyyaml)")
    return finish(agent_names)


def finish(agent_names: list[str] | None = None) -> int:
    for w in warnings:
        print(f"warning: {w}")
    if errors:
        print(f"\n✗ {len(errors)} problem(s) found:")
        for e in errors:
            print(f"  - {e}")
        return 1
    n = len(agent_names) if agent_names else 0
    print(f"✓ all checks passed ({n} agent{'s' if n != 1 else ''} validated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
