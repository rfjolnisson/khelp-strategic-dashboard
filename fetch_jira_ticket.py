#!/usr/bin/env python3
"""Fetch a KHELP (or any Jira) ticket and its linked tickets using the workspace API token."""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://kaptio.atlassian.net")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_TIMEOUT = int(os.getenv("JIRA_TIMEOUT", "30"))


class JiraFetcher:
    def __init__(self) -> None:
        if not JIRA_USERNAME or not JIRA_API_TOKEN:
            raise ValueError("JIRA_USERNAME and JIRA_API_TOKEN must be set in .env")
        self.base_url = JIRA_BASE_URL.rstrip("/")
        self.auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def _request(self, method: str, path: str, params: Dict | None = None) -> requests.Response:
        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            auth=self.auth,
            headers=self.headers,
            params=params,
            timeout=JIRA_TIMEOUT,
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _adf_to_text(node: Any) -> str:
        parts: list[str] = []

        def walk(n: Any) -> None:
            if isinstance(n, dict):
                if n.get("type") == "text":
                    parts.append(n.get("text", ""))
                if n.get("type") == "hardBreak":
                    parts.append("\n")
                if n.get("type") in {"paragraph", "heading"}:
                    for child in n.get("content", []) or []:
                        walk(child)
                    parts.append("\n")
                    return
                for child in n.get("content", []) or []:
                    walk(child)
            elif isinstance(n, list):
                for item in n:
                    walk(item)

        walk(node)
        return "".join(parts).strip()

    def get_issue(self, key: str) -> Dict[str, Any]:
        r = self._request(
            "GET",
            f"/rest/api/3/issue/{key}",
            params={"expand": "renderedFields,names,changelog", "fields": "*all"},
        )
        return r.json()

    def process(self, issue: Dict) -> Dict[str, Any]:
        f = issue.get("fields", {})
        key = issue.get("key", "N/A")

        description = f.get("description", "")
        if isinstance(description, dict):
            description = self._adf_to_text(description)

        issue_links = []
        for link in f.get("issuelinks", []) or []:
            ltype = link.get("type", {}).get("name", "Unknown")
            for side in ("outwardIssue", "inwardIssue"):
                if side in link:
                    li = link[side]
                    issue_links.append({
                        "direction": "outward" if side == "outwardIssue" else "inward",
                        "type": ltype,
                        "type_detail": link.get("type", {}).get(
                            "outward" if side == "outwardIssue" else "inward", ""
                        ),
                        "key": li.get("key"),
                        "summary": li.get("fields", {}).get("summary"),
                        "status": li.get("fields", {}).get("status", {}).get("name"),
                        "priority": li.get("fields", {}).get("priority", {}).get("name"),
                    })

        comments = []
        for c in (f.get("comment") or {}).get("comments", []) or []:
            body = c.get("body", "")
            if isinstance(body, dict):
                body = self._adf_to_text(body)
            comments.append({
                "author": c.get("author", {}).get("displayName", "Unknown"),
                "created": c.get("created"),
                "body": body,
            })

        history = []
        for h in (issue.get("changelog") or {}).get("histories", []) or []:
            for item in h.get("items", []) or []:
                history.append({
                    "author": h.get("author", {}).get("displayName", "Unknown"),
                    "created": h.get("created"),
                    "field": item.get("field"),
                    "from": item.get("fromString"),
                    "to": item.get("toString"),
                })

        subtasks = [
            {
                "key": st.get("key"),
                "summary": st.get("fields", {}).get("summary"),
                "status": st.get("fields", {}).get("status", {}).get("name"),
            }
            for st in f.get("subtasks", []) or []
        ]

        account = f.get("customfield_11400")
        if isinstance(account, dict):
            organization = account.get("name")
        elif isinstance(account, str):
            organization = account
        else:
            organization = None

        severity = f.get("customfield_10077") or {}
        support_type = f.get("customfield_10083") or {}

        return {
            "key": key,
            "url": f"{self.base_url}/browse/{key}",
            "summary": f.get("summary", ""),
            "description": description,
            "status": f.get("status", {}).get("name"),
            "priority": (f.get("priority") or {}).get("name"),
            "severity": severity.get("value") if isinstance(severity, dict) else None,
            "issue_type": (f.get("issuetype") or {}).get("name"),
            "assignee": (f.get("assignee") or {}).get("displayName") if f.get("assignee") else "Unassigned",
            "reporter": (f.get("reporter") or {}).get("displayName") if f.get("reporter") else "Unknown",
            "organization": organization,
            "support_type": support_type.get("value") if isinstance(support_type, dict) else None,
            "created": f.get("created"),
            "updated": f.get("updated"),
            "resolved": f.get("resolutiondate"),
            "resolution": (f.get("resolution") or {}).get("name") if f.get("resolution") else None,
            "components": [c.get("name") for c in f.get("components", []) or []],
            "labels": f.get("labels", []) or [],
            "fix_versions": [v.get("name") for v in f.get("fixVersions", []) or []],
            "subtasks": subtasks,
            "issue_links": issue_links,
            "comments": comments,
            "history": history,
        }


def main() -> None:
    key = sys.argv[1] if len(sys.argv) > 1 else "KHELP-12711"
    out_path = sys.argv[2] if len(sys.argv) > 2 else f"{key.lower().replace('-', '_')}_analysis.json"

    j = JiraFetcher()
    me = j._request("GET", "/rest/api/3/myself").json()
    print(f"Connected as: {me.get('displayName')} <{me.get('emailAddress')}>")

    print(f"Fetching {key} ...")
    raw = j.get_issue(key)
    main_issue = j.process(raw)

    linked: list[Dict[str, Any]] = []
    for link in main_issue["issue_links"]:
        lk = link["key"]
        try:
            print(f"  linked: {lk}")
            linked.append(j.process(j.get_issue(lk)))
        except Exception as e:
            print(f"    skip {lk}: {e}")

    subtasks_full: list[Dict[str, Any]] = []
    for st in main_issue["subtasks"]:
        sk = st["key"]
        try:
            print(f"  subtask: {sk}")
            subtasks_full.append(j.process(j.get_issue(sk)))
        except Exception as e:
            print(f"    skip {sk}: {e}")

    result = {
        "retrieved_at": datetime.now().isoformat(),
        "main_issue": main_issue,
        "linked_issues": linked,
        "subtask_details": subtasks_full,
    }

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, default=str)
    print(f"\nWrote {out_path}")

    mi = main_issue
    print("\n" + "=" * 70)
    print(f"{mi['key']}  |  {mi['status']}  |  {mi['priority']}  |  sev={mi['severity']}")
    print("=" * 70)
    print(f"Summary      : {mi['summary']}")
    print(f"Type         : {mi['issue_type']}")
    print(f"Reporter     : {mi['reporter']}")
    print(f"Assignee     : {mi['assignee']}")
    print(f"Organization : {mi['organization']}")
    print(f"Support type : {mi['support_type']}")
    print(f"Created      : {mi['created']}")
    print(f"Updated      : {mi['updated']}")
    print(f"Resolved     : {mi['resolved']}  ({mi['resolution']})")
    print(f"Components   : {', '.join(mi['components']) or 'None'}")
    print(f"Labels       : {', '.join(mi['labels']) or 'None'}")
    print(f"Fix versions : {', '.join(mi['fix_versions']) or 'None'}")

    print("\n--- Description ---")
    print(mi["description"] or "(none)")

    if mi["issue_links"]:
        print(f"\n--- Linked issues ({len(mi['issue_links'])}) ---")
        for link in mi["issue_links"]:
            print(f"  [{link['type_detail']:>18}] {link['key']}: {link['summary']} ({link['status']}, {link['priority']})")

    if mi["subtasks"]:
        print(f"\n--- Subtasks ({len(mi['subtasks'])}) ---")
        for st in mi["subtasks"]:
            print(f"  {st['key']}: {st['summary']} ({st['status']})")

    if mi["comments"]:
        print(f"\n--- Comments ({len(mi['comments'])}) ---")
        for c in mi["comments"]:
            print(f"\n  [{(c['created'] or '')[:19]}] {c['author']}:")
            body = (c["body"] or "").strip()
            for line in body.splitlines():
                print(f"    {line}")


if __name__ == "__main__":
    main()
