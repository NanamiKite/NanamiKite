#!/usr/bin/env python3
import json, os, urllib.request, html
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
    headers = {"Accept":"application/vnd.github+json", "User-Agent":"NanamiKite-profile"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{repo}", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def age(iso):
    if not iso:
        return "unknown"
    dt = datetime.fromisoformat(iso.replace("Z","+00:00"))
    days = (datetime.now(timezone.utc)-dt).days
    if days == 0:
        return "today"
    if days < 30:
        return f"{days}d ago"
    return dt.strftime("%Y-%m-%d")

def make(title, subtitle, tags, accent, data):
    x = 24
    pills = []
    for tag in tags:
        w = 22 + len(tag)*8.0
        pills.append(
            f'<rect x="{x:.1f}" y="124" width="{w:.1f}" height="26" rx="13" fill="#101820" stroke="{accent}"/>'
            f'<text x="{x+11:.1f}" y="142" fill="#e6edf3" font-size="13" '
            f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(tag)}</text>'
        )
        x += w + 7

    meta = f'★ {data.get("stargazers_count",0)}   forks {data.get("forks_count",0)}   ● {data.get("language") or "Mixed"}   updated {age(data.get("pushed_at"))}'

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="182" viewBox="0 0 390 182">'
        f'<rect width="390" height="182" rx="14" fill="#0d1117"/>'
        f'<rect x="1" y="1" width="388" height="180" rx="13" fill="none" stroke="#30363d"/>'
        f'<rect x="0" y="0" width="6" height="182" rx="3" fill="{accent}"/>'
        f'<text x="24" y="38" fill="{accent}" font-size="23" font-weight="700" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(title)}</text>'
        f'<text x="24" y="72" fill="#e6edf3" font-size="15.5" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(subtitle)}</text>'
        f'<text x="24" y="101" fill="#b1bac4" font-size="13" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(meta)}</text>'
        + ''.join(pills)
        + '</svg>'
    )

OUT.mkdir(parents=True, exist_ok=True)
for repo,title,subtitle,tags,accent,fn in PROJECTS:
    data = fetch(repo)
    (OUT/fn).write_text(make(title,subtitle,tags,accent,data), encoding="utf-8")

print("cards refreshed")
