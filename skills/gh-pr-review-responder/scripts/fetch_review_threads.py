#!/usr/bin/env python3
"""Fetch review threads for the open PR on the current branch."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any
from urllib.parse import urlparse

QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $cursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      title
      url
      state
      reviews(first: 100) {
        nodes {
          id
          state
          body
          submittedAt
          url
          author { login }
        }
      }
      reviewThreads(first: 100, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          originalLine
          comments(first: 100) {
            nodes {
              id
              databaseId
              body
              createdAt
              updatedAt
              url
              author { login }
            }
          }
        }
      }
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


def parse_owner_repo_from_pr_url(raw_url: str) -> tuple[str, str]:
    """Extract owner/repo from a PR URL such as https://host/owner/repo/pull/123."""
    parsed = urlparse(raw_url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise RuntimeError(
            "Failed to parse owner/repo from PR URL. "
            f"Expected /<owner>/<repo>/pull/<number>, got: {raw_url}",
        )
    # Keep URL-based resolution to avoid gh JSON field compatibility issues.
    return parts[0], parts[1]


def get_current_pr_ref(pr_number: int | None = None) -> tuple[str, str, int]:
    cmd = ["gh", "pr", "view", "--json", "number,url"]
    if pr_number is not None:
        cmd.extend([str(pr_number)])
    pr = run_json(cmd)

    raw_number = pr.get("number")
    if not isinstance(raw_number, int):
        raise RuntimeError(
            "Failed to resolve PR number."
            if pr_number is not None
            else "Failed to resolve PR number for the current PR."
        )
    number = raw_number

    raw_url = str(pr.get("url", "")).strip()
    if not raw_url:
        raise RuntimeError("Failed to resolve PR URL for the current PR.")

    owner, repo = parse_owner_repo_from_pr_url(raw_url)
    return owner, repo, number


def call_graphql(owner: str, repo: str, number: int, cursor: str | None) -> dict[str, Any]:
    cmd = [
        "gh",
        "api",
        "graphql",
        "-F",
        "query=@-",
        "-f",
        f"owner={owner}",
        "-f",
        f"repo={repo}",
        "-F",
        f"number={number}",
    ]
    if cursor:
        cmd.extend(["-f", f"cursor={cursor}"])

    return run_json(cmd, QUERY)


def truncate_text(value: str, max_chars: int) -> str:
    text = value.strip()
    if len(text) <= max_chars:
        return text
    if max_chars <= 3:
        return text[:max_chars]
    return f"{text[: max_chars - 3]}..."


def extract_author(comment: dict[str, Any]) -> str:
    author = comment.get("author", {})
    if not isinstance(author, dict):
        return ""
    return str(author.get("login", "")).strip()


def summarize_thread(thread: dict[str, Any], index: int, max_body_chars: int) -> dict[str, Any]:
    raw_comments = thread.get("comments", {})
    comment_nodes = raw_comments.get("nodes") if isinstance(raw_comments, dict) else []
    comments = comment_nodes if isinstance(comment_nodes, list) else []

    latest_comment = comments[-1] if comments else {}

    latest_body = str(latest_comment.get("body", ""))
    latest_author = extract_author(latest_comment) if isinstance(latest_comment, dict) else ""
    latest_url = str(latest_comment.get("url", "")) if isinstance(latest_comment, dict) else ""
    latest_database_id: int | None = None
    if isinstance(latest_comment, dict):
        raw_id = latest_comment.get("databaseId")
        if isinstance(raw_id, int):
            latest_database_id = raw_id

    return {
        "index": index,
        "thread_id": str(thread.get("id", "")),
        "path": str(thread.get("path", "")),
        "line": thread.get("line"),
        "original_line": thread.get("originalLine"),
        "is_resolved": bool(thread.get("isResolved", False)),
        "is_outdated": bool(thread.get("isOutdated", False)),
        "latest_comment_author": latest_author,
        "latest_comment_url": latest_url,
        "latest_comment_database_id": latest_database_id,
        "latest_comment_body": truncate_text(latest_body, max_body_chars),
        "comment_count": len(comments),
    }


def should_include_thread(
    thread: dict[str, Any],
    include_resolved: bool,
    include_outdated: bool,
) -> bool:
    is_resolved = bool(thread.get("is_resolved", False))
    is_outdated = bool(thread.get("is_outdated", False))

    if not include_resolved and is_resolved:
        return False
    if not include_outdated and is_outdated:
        return False
    return True


def fetch_threads(max_body_chars: int, pr_number: int | None = None) -> dict[str, Any]:
    ensure_gh_auth()
    owner, repo, number = get_current_pr_ref(pr_number=pr_number)

    cursor: str | None = None
    raw_threads: list[dict[str, Any]] = []
    pr_meta: dict[str, Any] | None = None
    reviews: list[dict[str, Any]] = []

    while True:
        payload = call_graphql(owner=owner, repo=repo, number=number, cursor=cursor)
        if payload.get("errors"):
            raise RuntimeError(f"GraphQL returned errors: {json.dumps(payload['errors'])}")

        repository = payload.get("data", {}).get("repository", {})
        pull_request = repository.get("pullRequest")
        if pull_request is None:
            raise RuntimeError("Failed to load pull request data from GraphQL response.")

        if pr_meta is None:
            pr_meta = {
                "owner": owner,
                "repo": repo,
                "number": int(pull_request.get("number")),
                "title": str(pull_request.get("title", "")),
                "url": str(pull_request.get("url", "")),
                "state": str(pull_request.get("state", "")),
            }
            raw_reviews = pull_request.get("reviews", {}).get("nodes", [])
            if isinstance(raw_reviews, list):
                for review in raw_reviews:
                    if not isinstance(review, dict):
                        continue
                    author = extract_author(review)
                    reviews.append(
                        {
                            "id": str(review.get("id", "")),
                            "state": str(review.get("state", "")),
                            "author": author,
                            "url": str(review.get("url", "")),
                            "submitted_at": str(review.get("submittedAt", "")),
                            "body": truncate_text(str(review.get("body", "")), max_body_chars),
                        }
                    )

        review_threads = pull_request.get("reviewThreads", {})
        nodes = review_threads.get("nodes", [])
        if isinstance(nodes, list):
            for node in nodes:
                if isinstance(node, dict):
                    raw_threads.append(node)

        page_info = review_threads.get("pageInfo", {})
        has_next_page = bool(page_info.get("hasNextPage", False))
        end_cursor = page_info.get("endCursor")
        if has_next_page and isinstance(end_cursor, str) and end_cursor:
            cursor = end_cursor
            continue
        break

    if pr_meta is None:
        raise RuntimeError("PR metadata could not be initialized.")

    summarized_threads = [
        summarize_thread(thread=item, index=index + 1, max_body_chars=max_body_chars)
        for index, item in enumerate(raw_threads)
    ]
    pending_count = sum(
        1
        for thread in summarized_threads
        if not thread["is_resolved"] and not thread["is_outdated"]
    )

    return {
        "pull_request": pr_meta,
        "total_threads": len(summarized_threads),
        "pending_threads": pending_count,
        "review_threads": summarized_threads,
        "reviews": reviews,
    }


def render_markdown(result: dict[str, Any]) -> str:
    pr = result["pull_request"]
    threads = result["review_threads"]

    lines: list[str] = []
    lines.append(f"# PR #{pr['number']}: {pr['title']}")
    lines.append(f"- URL: {pr['url']}")
    lines.append(f"- State: {pr['state']}")
    lines.append(f"- Pending threads: {result['pending_threads']} / {result['total_threads']}")
    lines.append("")

    if not threads:
        lines.append("No review threads found.")
        return "\n".join(lines)

    for thread in threads:
        location = thread["path"] or "(unknown-path)"
        if isinstance(thread["line"], int):
            location = f"{location}:{thread['line']}"
        lines.append(f"## {thread['index']}. {location}")
        lines.append(f"- Thread ID: `{thread['thread_id']}`")
        lines.append(f"- Resolved: `{thread['is_resolved']}`")
        lines.append(f"- Outdated: `{thread['is_outdated']}`")
        if thread["latest_comment_author"]:
            lines.append(f"- Latest author: @{thread['latest_comment_author']}")
        if thread["latest_comment_url"]:
            lines.append(f"- Latest comment URL: {thread['latest_comment_url']}")
        lines.append("- Latest comment body:")
        lines.append("```text")
        lines.append(thread["latest_comment_body"] or "(empty)")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch review threads from the open PR on the current branch.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format (default: json).",
    )
    parser.add_argument(
        "--include-resolved",
        action="store_true",
        help="Include resolved threads.",
    )
    parser.add_argument(
        "--include-outdated",
        action="store_true",
        help="Include outdated threads.",
    )
    parser.add_argument(
        "--max-body-chars",
        type=int,
        default=300,
        help="Max characters to keep from each comment body.",
    )
    parser.add_argument(
        "--pr",
        type=int,
        metavar="NUMBER",
        default=None,
        help="Pull request number (default: PR for current branch).",
    )
    args = parser.parse_args()

    if args.max_body_chars <= 0:
        print("--max-body-chars must be greater than zero.", file=sys.stderr)
        return 2

    try:
        result = fetch_threads(max_body_chars=args.max_body_chars, pr_number=args.pr)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    filtered_threads: list[dict[str, Any]] = []
    for thread in result["review_threads"]:
        if should_include_thread(
            thread=thread,
            include_resolved=args.include_resolved,
            include_outdated=args.include_outdated,
        ):
            filtered_threads.append(thread)
    result["review_threads"] = filtered_threads

    if args.format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
