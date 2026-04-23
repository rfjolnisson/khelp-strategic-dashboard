#!/usr/bin/env python3
"""Post a comment on a Jira ticket and (optionally) transition it."""

import json
import os
import sys

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

BASE = os.getenv("JIRA_BASE_URL", "https://kaptio.atlassian.net").rstrip("/")
AUTH = HTTPBasicAuth(os.getenv("JIRA_USERNAME"), os.getenv("JIRA_API_TOKEN"))
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def text_to_adf(text: str) -> dict:
    """Convert plain text (with blank-line paragraphs) to Atlassian Document Format."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    content = []
    for para in paragraphs:
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": para}],
        })
    return {"type": "doc", "version": 1, "content": content}


def add_comment(issue_key: str, body_text: str) -> dict:
    resp = requests.post(
        f"{BASE}/rest/api/3/issue/{issue_key}/comment",
        auth=AUTH,
        headers=HEADERS,
        json={"body": text_to_adf(body_text)},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def list_transitions(issue_key: str) -> list[dict]:
    resp = requests.get(
        f"{BASE}/rest/api/3/issue/{issue_key}/transitions",
        auth=AUTH,
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("transitions", [])


def transition(issue_key: str, transition_id: str) -> None:
    resp = requests.post(
        f"{BASE}/rest/api/3/issue/{issue_key}/transitions",
        auth=AUTH,
        headers=HEADERS,
        json={"transition": {"id": transition_id}},
        timeout=30,
    )
    resp.raise_for_status()


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage:")
        print("  jira_comment.py <ISSUE> comment <PATH_TO_BODY_FILE>")
        print("  jira_comment.py <ISSUE> transitions")
        print("  jira_comment.py <ISSUE> transition <ID>")
        sys.exit(1)

    issue = sys.argv[1]
    cmd = sys.argv[2]

    if cmd == "transitions":
        transitions = list_transitions(issue)
        for t in transitions:
            to = t.get("to", {})
            print(f"  id={t['id']:<4}  name={t['name']:<30}  to_status={to.get('name')}")
    elif cmd == "comment":
        path = sys.argv[3]
        with open(path, "r", encoding="utf-8") as fh:
            body = fh.read()
        result = add_comment(issue, body)
        print(f"Comment posted, id={result.get('id')} url={BASE}/browse/{issue}")
    elif cmd == "transition":
        transition_id = sys.argv[3]
        transition(issue, transition_id)
        print(f"Transitioned {issue} via transition id {transition_id}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
