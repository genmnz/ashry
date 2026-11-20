#!/usr/bin/env python3
"""Copy this session's working transcripts into the repository, redacted.

The repository is meant to be self-contained: the analysis, the sources it
rests on, and the record of how it was produced. The last of those is the
session transcripts, which are written by the agent harness outside the
repository and are lost when the container is reclaimed.

They cannot be committed as they stand. A transcript contains the email
address of the account that ran the session, the member's display name, links
that carry a session identifier, and, in principle, any credential that passed
through a shell command. This script copies them with those removed, and
refuses to write anything if the check at the end still finds one.

What is redacted:

* every email address except `noreply@anthropic.com`, which is a placeholder
  and identifies nobody;
* any literal string passed with --name, which is how the display name and
  the local part of an email address are removed: a bare token like that is
  identifying but matches no pattern, and it survives in the text of commands
  the session itself ran;
* claude.ai session links, which identify an account's session;
* anything shaped like an API token (GitHub, Anthropic, AWS, a bearer header).

What is deliberately kept: the repository's own name and branches, file paths
inside the container, every command run and its output, and the full text of
the reasoning. Those are the record.

Usage:
    python3 src/record_history.py --name "<display name>"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "history"
SOURCES = [
    Path("/root/.claude/projects"),
]

KEEP_EMAILS = {"noreply@anthropic.com"}

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SESSION_LINK = re.compile(r"https://claude\.ai/code/session_[A-Za-z0-9_-]+")
SESSION_ID = re.compile(r"\bsession_[A-Za-z0-9]{16,}\b")
TOKENS = [
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(?:authorization|bearer)\b[:=\s]+[A-Za-z0-9._-]{20,}"),
]


def redact(text: str, names: list[str]) -> str:
    def email_sub(m: re.Match) -> str:
        return m.group(0) if m.group(0).lower() in KEEP_EMAILS else "[email redacted]"

    text = EMAIL.sub(email_sub, text)
    text = SESSION_LINK.sub("[session link redacted]", text)
    text = SESSION_ID.sub("session_[redacted]", text)
    for pat in TOKENS:
        text = pat.sub("[credential redacted]", text)
    for name in names:
        if not name:
            continue
        text = re.sub(rf"\b{re.escape(name)}\b", "[name redacted]", text,
                      flags=re.IGNORECASE)
    return text


def residue(text: str, names: list[str]) -> list[str]:
    """Anything the redaction should have removed and did not."""
    found = []
    for m in EMAIL.finditer(text):
        if m.group(0).lower() not in KEEP_EMAILS:
            found.append(m.group(0))
    for pat in (SESSION_LINK, SESSION_ID, *TOKENS):
        found += [m.group(0) for m in pat.finditer(text)]
    for name in names:
        if name and re.search(rf"\b{re.escape(name)}\b", text, re.I):
            found.append(name)
    return found


def copy_tree(src: Path, dst: Path, names: list[str]) -> tuple[int, int]:
    files = kept = 0
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        files += 1
        rel = path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        clean = redact(text, names)
        left = residue(clean, names)
        if left:
            print(f"  REFUSED {rel}: {sorted(set(left))[:3]}", file=sys.stderr)
            continue
        target.write_text(clean)
        kept += 1
    return files, kept


def digest(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:16]


def worklog(names: list[str]) -> int:
    """A readable chronology to go beside the raw transcripts.

    The transcripts are the record, but nobody reads 13 MB of JSON. This walks
    them in order and writes one line per exchange: what was asked, what was
    done about it, and which commands ran, so the shape of the work is legible
    without opening the raw files.
    """
    rows: list[tuple[str, str, str]] = []
    for path in sorted((OUT / "transcripts").rglob("*.jsonl")):
        for line in path.read_text(errors="replace").splitlines():
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") not in ("user", "assistant"):
                continue
            msg = rec.get("message") or {}
            content = msg.get("content")
            when = (rec.get("timestamp") or "")[:19].replace("T", " ")
            texts, commands = [], []
            if isinstance(content, str):
                texts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        texts.append(block.get("text", ""))
                    elif block.get("type") == "tool_use":
                        inp = block.get("input") or {}
                        if block.get("name") == "Bash" and inp.get("description"):
                            commands.append(str(inp["description"]))
            body = " ".join(t.strip() for t in texts if t.strip())
            body = " ".join(body.split())
            if not body and not commands:
                continue
            who = "asked" if rec.get("type") == "user" else "did"
            if body:
                rows.append((when, who, body[:400]))
            for c in commands:
                rows.append((when, "ran", c[:160]))

    lines = ["# Work log", "",
             "A readable chronology derived from the transcripts in",
             "`docs/history/transcripts/`. \"asked\" is a message into the",
             "session, \"did\" is what it reported back, \"ran\" is a command it",
             "ran, described in its own words. Generated by",
             "`src/record_history.py`; the transcripts are the authority.", ""]
    last_day = ""
    for when, who, body in rows:
        day = when[:10]
        if day != last_day:
            lines += ["", f"## {day}", ""]
            last_day = day
        lines.append(f"- `{when[11:16]}` **{who}** — {redact(body, names)}")
    (OUT / "worklog.md").write_text("\n".join(lines) + "\n")
    return len(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", action="append", default=[],
                    help="a literal string to redact wherever it appears as a "
                         "whole word: a display name, an email's local part, "
                         "a host. Repeatable. Not stored anywhere, so that "
                         "this script can be committed and the values cannot.")
    args = ap.parse_args()

    if OUT.exists():
        shutil.rmtree(OUT / "transcripts", ignore_errors=True)
    (OUT / "transcripts").mkdir(parents=True, exist_ok=True)

    total = kept = 0
    for src in SOURCES:
        if not src.exists():
            print(f"  {src} not present in this container; skipped")
            continue
        f, k = copy_tree(src, OUT / "transcripts", args.name)
        total += f
        kept += k

    index = ["# Session transcripts", "",
             "The raw working record of the sessions that produced this",
             "repository, copied out of the agent harness and redacted by",
             "`src/record_history.py`. Email addresses, the member's display",
             "name, session links and anything shaped like a credential are",
             "removed; commands, outputs, reasoning and file paths are kept.",
             "",
             "Each session that ran in its own container keeps its own",
             "transcript there, so only the sessions whose container this is",
             "appear below.",
             "", "| File | Size | SHA-256 (first 16) |", "|---|---|---|"]
    for path in sorted((OUT / "transcripts").rglob("*")):
        if path.is_file():
            rel = path.relative_to(OUT / "transcripts")
            index.append(f"| `{rel}` | {path.stat().st_size // 1024} KB "
                         f"| `{digest(path)}` |")
    (OUT / "transcripts" / "README.md").write_text("\n".join(index) + "\n")

    print(f"  work log: {worklog(args.name):,} entries -> {OUT / 'worklog.md'}")
    print(f"copied {kept} of {total} transcript files -> {OUT / 'transcripts'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
