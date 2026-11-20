#!/usr/bin/env python3
"""Install the canonical Skill into one or more agent-specific skill directories."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "mao-quote-poster"

TARGETS = {
    "agents": ".agents/skills",
    "codex": ".codex/skills",
    "claude": ".claude/skills",
    "pi": ".pi/skills",
    "opencode": ".opencode/skills",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Target project directory")
    parser.add_argument(
        "--targets",
        default="agents,codex,claude,pi,opencode",
        help="Comma-separated targets: agents,codex,claude,pi,opencode",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing Skill copies")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        raise SystemExit(f"Project directory does not exist: {project}")
    if not SOURCE.is_dir():
        raise SystemExit(f"Canonical Skill source not found: {SOURCE}")

    names = [name.strip().lower() for name in args.targets.split(",") if name.strip()]
    unknown = sorted(set(names) - set(TARGETS))
    if unknown:
        raise SystemExit(f"Unknown target(s): {', '.join(unknown)}")

    for name in names:
        destination = project / TARGETS[name] / "mao-quote-poster"
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if not args.force:
                print(f"SKIP (already exists; use --force to replace): {destination}")
                continue
            shutil.rmtree(destination)
        shutil.copytree(SOURCE, destination)
        print(f"INSTALLED {name}: {destination}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
