#!/usr/bin/env python3
"""Reply to a GitHub PR review thread and optionally resolve it."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPLY_MUTATION = """\
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(
    input: { pullRequestReviewThreadId: $threadId, body: $body }
  ) {
    comment {
      id
      url
      body
      author {
        login
      }
    }
  }
}
"""

RESOLVE_MUTATION = """\
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread {
      id
      isResolved
    }
  }
}
"""


def run(cmd: list[str], stdin_text: str | None = None) -> str:
    try:
        completed = subprocess.run(
            cmd,
            input=stdin_text,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(f"Failed to execute command: {' '.join(cmd)}") from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "(no stderr)"
        raise RuntimeError(f"Command failed ({completed.returncode}): {' '.join(cmd)}\n{stderr}")

    return completed.stdout


def run_json(cmd: list[str], stdin_text: str | None = None) -> dict[str, Any]:
    raw = run(cmd, stdin_text)
    try:
        data: dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Command output is not valid JSON: {exc}") from exc
    return data


def ensure_gh_auth() -> None:
    try:
        run(["gh", "auth", "status"])
    except RuntimeError as exc:
        raise RuntimeError("GitHub CLI is not authenticated. Run `gh auth login` first.") from exc


def graphql(query: str, fields: dict[str, str]) -> dict[str, Any]:
    """Call GitHub GraphQL via `gh api`. Large `body` values are passed with `-F body=@file` (UTF-8) to avoid argv length limits and shell newline issues."""
    paths: list[str] = []
    try:
        qfile = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            suffix=".graphql",
        )
        qfile.write(query)
        qfile.close()
        paths.append(qfile.name)

        cmd: list[str] = ["gh", "api", "graphql", "-F", f"query=@{qfile.name}"]
        for key, value in fields.items():
            if key == "body":
                bfile = tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    delete=False,
                    suffix=".txt",
                )
                bfile.write(value)
                bfile.close()
                paths.append(bfile.name)
                cmd.extend(["-F", f"{key}=@{bfile.name}"])
            else:
                cmd.extend(["-F", f"{key}={value}"])
        return run_json(cmd)
    finally:
        for path in paths:
            try:
                os.unlink(path)
            except OSError:
                pass


def extract_graphql_data(payload: dict[str, Any]) -> dict[str, Any]:
    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        raise RuntimeError(f"GraphQL returned errors: {json.dumps(errors)}")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("GraphQL response did not include `data`.")
    return data


def load_body(args: argparse.Namespace) -> str:
    if args.body and args.body_file:
        raise RuntimeError("Use either --body or --body-file, not both.")
    if not args.body and not args.body_file:
        raise RuntimeError("Provide --body or --body-file.")

    if args.body:
        text = args.body.strip()
        if not text:
            raise RuntimeError("--body is empty.")
        return text

    file_path = Path(args.body_file).expanduser().resolve()
    if not file_path.exists():
        raise RuntimeError(f"Body file not found: {file_path}")
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            f"Body file is not valid UTF-8 (use UTF-8 for Japanese and other Unicode): {file_path}\n{exc}"
        ) from exc
    text = text.strip()
    if not text:
        raise RuntimeError("Body file is empty.")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reply to a GitHub PR review thread and optionally resolve it.",
    )
    parser.add_argument(
        "--thread-id",
        required=True,
        help="GraphQL review thread ID (for example PRRT_xxx).",
    )
    parser.add_argument("--body", help="Reply body text.")
    parser.add_argument("--body-file", help="Path to a text file containing the reply.")
    parser.add_argument(
        "--resolve",
        action="store_true",
        help="Resolve the review thread after posting the reply.",
    )
    args = parser.parse_args()

    try:
        body = load_body(args)
        ensure_gh_auth()

        reply_payload = graphql(
            query=REPLY_MUTATION,
            fields={
                "threadId": args.thread_id,
                "body": body,
            },
        )
        reply_data = extract_graphql_data(reply_payload)
        reply_info = reply_data.get("addPullRequestReviewThreadReply", {}).get("comment", {})

        output: dict[str, Any] = {
            "thread_id": args.thread_id,
            "reply": {
                "id": reply_info.get("id"),
                "url": reply_info.get("url"),
                "author": reply_info.get("author", {}).get("login")
                if isinstance(reply_info.get("author"), dict)
                else None,
            },
            "resolved": None,
        }

        if args.resolve:
            resolve_payload = graphql(
                query=RESOLVE_MUTATION,
                fields={"threadId": args.thread_id},
            )
            resolve_data = extract_graphql_data(resolve_payload)
            thread_info = resolve_data.get("resolveReviewThread", {}).get("thread", {})
            output["resolved"] = {
                "id": thread_info.get("id"),
                "is_resolved": thread_info.get("isResolved"),
            }

        print(json.dumps(output, indent=2))
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
