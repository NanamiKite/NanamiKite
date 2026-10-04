#!/usr/bin/env python3
import json
import os
import urllib.request
import html
from pathlib import Path
from datetime import datetime, timezone

OWNER = "NanamiKite"
OUT = Path("assets/generated")
PROJECTS = [
    ("DirectHCI", "DirectHCI", "Windows Raw HCI infrastructure", ["Rust","Windows","WinUSB","HCI"], "#58d8ff", "directhci-card.svg"),
    ("FLOW-8-PC-Controller", "FLOW 8 PC Controller", "Native BLE desktop control", ["Rust","BLE/GATT","Protocol RE"], "#6ee7b7", "flow8-card.svg"),
    ("CodeRecoil-for-Coyote-2.0", "CodeRecoil", "Editor events to physical feedback", ["JavaScript","VS Code","BLE"], "#f7b955", "coderecoil-card.svg"),
]

def fetch(repo):
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "NanamiKite-profile",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request("https://api.github.com/repos/%s/%s" % (OWNER, repo), headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def age(iso):
    if not iso:
        return "unknown"
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    days = (datetime.now(timezone.utc) - dt).days
    if days == 0:
        return "today"
    if days < 30:
        return "%dd ago" % days
    return dt.strftime("%Y-%m-%d")

def make(title, subtitle, tags, accent, data):
    pills = []
    x = 22
    for tag in tags:
        w = 18 + len(tag) * 7.0
        pills.append(
            '<rect x="%.1f" y="118" width="%.1f" height="23" rx="11.5" fill="#111820" stroke="%s"/>'
            '<text x="%.1f" y="134" fill="#d7f4ff" font-size="11.5" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">%s</text>'
            % (x, w, accent, x+9, html.escape(tag))
        )
        x += w + 6
    meta = "★ %s   forks %s   ● %s   updated %s" % (
        data.get("stargazers_count", 0),
        data.get("forks_count", 0),
        data.get("language") or "Mixed",
        age(data.get("pushed_at")),
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="380" height="174" viewBox="0 0 380 174">'
        '<rect width="380" height="174" rx="14" fill="#0d1117"/>'
        '<rect x="1" y="1" width="378" height="172" rx="13" fill="none" stroke="#30363d"/>'
        '<rect x="0" y="0" width="6" height="174" rx="3" fill="%s"/>'
        '<text x="22" y="34" fill="%s" font-size="18" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">%s</text>'
        '<text x="22" y="62" fill="#e6edf3" font-size="12.5" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">%s</text>'
        '<text x="22" y="88" fill="#8b949e" font-size="11.8" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">%s</text>'
        '%s'
        '<circle cx="27" cy="158" r="4" fill="#3fb950"/>'
        '<text x="38" y="162" fill="#3fb950" font-size="11.5" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">LIVE</text>'
        '<text x="319" y="162" fill="#58a6ff" font-size="11.5" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">OPEN</text>'
        '</svg>'
    ) % (accent, accent, html.escape(title), html.escape(subtitle), html.escape(meta), "".join(pills))

OUT.mkdir(parents=True, exist_ok=True)
for repo, title, subtitle, tags, accent, fn in PROJECTS:
    data = fetch(repo)
    (OUT / fn).write_text(make(title, subtitle, tags, accent, data), encoding="utf-8")
print("cards refreshed")
