#!/usr/bin/env python3
"""JQL search utility using the Jira REST API."""

import json
import os
import sys
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

BASE = os.getenv("JIRA_BASE_URL", "https://kaptio.atlassian.net").rstrip("/")
AUTH = HTTPBasicAuth(os.getenv("JIRA_USERNAME"), os.getenv("JIRA_API_TOKEN"))
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def search(jql: str, fields: List[str], limit: int = 50) -> Dict[str, Any]:
    r = requests.post(
        f"{BASE}/rest/api/3/search/jql",
        auth=AUTH,
        headers=HEADERS,
        json={"jql": jql, "fields": fields, "maxResults": limit},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    jql = sys.argv[1] if len(sys.argv) > 1 else ""
    if not jql:
        print("Usage: jql_search.py '<JQL>'")
        sys.exit(1)
    fields = ["summary", "status", "priority", "labels", "components", "assignee", "reporter", "created", "updated", "resolution"]
    result = search(jql, fields, limit=50)
    issues = result.get("issues", [])
    print(f"Found {len(issues)} issues (showing up to 50)")
    print("-" * 90)
    for iss in issues:
        f = iss["fields"]
        status = (f.get("status") or {}).get("name", "?")
        pr = (f.get("priority") or {}).get("name", "?")
        reporter = (f.get("reporter") or {}).get("displayName", "?")
        labels = ",".join(f.get("labels", []) or [])
        print(f"{iss['key']:>14}  {status:<22}  {pr:<10}  {reporter[:20]:<20}  {f.get('summary', '')[:55]}  [{labels}]")


if __name__ == "__main__":
    main()
