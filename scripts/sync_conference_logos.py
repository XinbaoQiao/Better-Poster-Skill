#!/usr/bin/env python3
"""Sync conference logos from CS-Conference-Logo-Maintainer."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

DEFAULT_SOURCE_REPO = "https://github.com/XinbaoQiao/CS-Conference-Logo-Maintainer.git"
DEFAULT_SOURCE_SUBDIR = "assets/logos"
DEFAULT_TARGET_DIR = "assets/conference-logos"
LOGO_SUFFIXES = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".pdf"}
GIT_TIMEOUT_SECONDS = 300
PROXY_ENV_KEYS = (
    "http_proxy",
    "https_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "all_proxy",
    "ALL_PROXY",
)


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in PROXY_ENV_KEYS:
        env.pop(key, None)
    return env


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> str:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        raise RuntimeError(f"Command timed out after {GIT_TIMEOUT_SECONDS}s: {' '.join(cmd)}\n{output}") from exc
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{result.stdout}")
    return result.stdout.strip()


def clone_source(repo: str, branch: str | None, source_subdir: str, env: dict[str, str]) -> tuple[Path, str, tempfile.TemporaryDirectory[str]]:
    temp_dir = tempfile.TemporaryDirectory(prefix="conference-logo-source-")
    root = Path(temp_dir.name) / "repo"
    cmd = ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse"]
    if branch:
        cmd.extend(["--branch", branch])
    cmd.extend([repo, str(root)])
    run(cmd, Path.cwd(), env)
    run(["git", "-C", str(root), "sparse-checkout", "set", source_subdir], Path.cwd(), env)
    source_sha = run(["git", "-C", str(root), "rev-parse", "HEAD"], Path.cwd(), env)
    return root, source_sha, temp_dir


def resolve_logo_dir(source_root: Path, source_subdir: str) -> Path:
    nested = source_root / source_subdir
    if nested.is_dir():
        return nested
    if source_root.is_dir() and any(path.is_file() and path.suffix.lower() in LOGO_SUFFIXES for path in source_root.iterdir()):
        return source_root
    raise FileNotFoundError(f"Could not find logo directory: {nested}")


def iter_logo_files(source_logo_dir: Path) -> list[Path]:
    files = [
        path
        for path in source_logo_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in LOGO_SUFFIXES
    ]
    return sorted(files, key=lambda path: path.relative_to(source_logo_dir).as_posix().lower())


def sync_logo_files(source_logo_dir: Path, target_dir: Path, dry_run: bool) -> tuple[int, int, int]:
    target_dir.mkdir(parents=True, exist_ok=True)
    added = 0
    updated = 0
    unchanged = 0

    for source in iter_logo_files(source_logo_dir):
        rel = source.relative_to(source_logo_dir)
        target = target_dir / rel
        if not target.exists():
            added += 1
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            continue
        if filecmp.cmp(source, target, shallow=False):
            unchanged += 1
            continue
        updated += 1
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    return added, updated, unchanged


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", default=DEFAULT_SOURCE_REPO)
    parser.add_argument("--source-branch", default=None, help="Optional source branch or tag.")
    parser.add_argument("--source-subdir", default=DEFAULT_SOURCE_SUBDIR)
    parser.add_argument("--source-dir", type=Path, help="Use an existing local checkout or logo directory instead of cloning.")
    parser.add_argument("--target-dir", type=Path, default=Path(DEFAULT_TARGET_DIR))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    env = clean_env()
    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    source_sha = "local-source"

    if args.source_dir:
        source_root = args.source_dir
    else:
        source_root, source_sha, temp_dir = clone_source(args.source_repo, args.source_branch, args.source_subdir, env)

    try:
        source_logo_dir = resolve_logo_dir(source_root, args.source_subdir)
        source_count = len(iter_logo_files(source_logo_dir))
        added, updated, unchanged = sync_logo_files(source_logo_dir, args.target_dir, args.dry_run)
        mode = "dry-run" if args.dry_run else "sync"
        print(f"{mode}: source={source_logo_dir} target={args.target_dir}")
        print(f"source logos: {source_count}")
        print(f"added: {added}")
        print(f"updated: {updated}")
        print(f"unchanged: {unchanged}")
        print(f"source revision: {source_sha}")
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
