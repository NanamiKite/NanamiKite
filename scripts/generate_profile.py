#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OWNER = "NanamiKite"
OUT = Path("assets/generated")
OUT.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    {
        "repo": "DirectHCI",
        "title": "DirectHCI",
        "subtitle": "Windows userspace Bluetooth controller ownership & Raw HCI",
        "tags": ["Rust", "Windows", "WinUSB", "HCI"],
        "accent": "#58d8ff",
    },
    {
        "repo": "FLOW-8-PC-Controller",
        "title": "FLOW 8 PC Controller",
        "subtitle": "Native BLE desktop control for the Behringer FLOW 8",
        "tags": ["Rust", "BLE/GATT", "Protocol RE", "Desktop"],
        "accent": "#6ee7b7",
    },
    {
        "repo": "CodeRecoil-for-Coyote-2.0",
        "title": "CodeRecoil for Coyote 2.0",
        "subtitle": "Editor / compiler events to physical BLE feedback",
        "tags": ["JavaScript", "VS Code", "BLE", "Hardware"],
        "accent": "#f7b955",
    },
]

def github_json(path: str):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "NanamiKite-profile-card-generator",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def esc(value):
    return html.escape(str(value), quote=True)

def age_label(iso):
    if not iso:
        return "unknown"
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    seconds = max(0, int((now - dt).total_seconds()))
    if seconds < 3600:
        return f"{max(1, seconds // 60)}m ago"
    if seconds < 86400:
        return f"{seconds // 3600}h ago"
    if seconds < 86400 * 60:
        return f"{seconds // 86400}d ago"
    return dt.strftime("%Y-%m-%d")

def status_from(iso):
    if not iso:
        return "UNKNOWN", "#8b949e"
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    days = (datetime.now(timezone.utc) - dt).days
    if days <= 14:
        return "ACTIVE", "#3fb950"
    if days <= 60:
        return "RECENT", "#d29922"
    return "QUIET", "#8b949e"

def pill(x, y, label, stroke, color="#d7f4ff"):
    width = 18 + len(label) * 8
    svg = (
        f'<rect x="{x}" y="{y}" width="{width}" height="26" rx="13" '
        f'fill="#111820" stroke="{stroke}"/>'
        f'<text x="{x + 9}" y="{y + 18}" fill="{color}" font-size="13" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{esc(label)}</text>'
    )
    return svg, width

def render_card(cfg, data):
    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    language = data.get("language") or "Mixed"
    pushed = data.get("pushed_at")
    status, status_color = status_from(pushed)
    updated = age_label(pushed)
    tags = []
    x = 28
    for tag in cfg["tags"]:
        svg, width = pill(x, 142, tag, cfg["accent"])
        tags.append(svg)
        x += width + 8

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="245" viewBox="0 0 520 245">
<rect width="520" height="245" rx="16" fill="#0d1117"/>
<rect x="1" y="1" width="518" height="243" rx="15" fill="none" stroke="#30363d"/>
<rect x="0" y="0" width="7" height="245" rx="3.5" fill="{cfg['accent']}"/>
<text x="28" y="42" fill="{cfg['accent']}" font-size="24" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{esc(cfg['title'])}</text>
<text x="28" y="75" fill="#e6edf3" font-size="15" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{esc(cfg['subtitle'])}</text>
<text x="28" y="108" fill="#8b949e" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">★ {stars}    ⑂ {forks}    ● {esc(language)}    updated {esc(updated)}</text>
{''.join(tags)}
<line x1="28" y1="190" x2="492" y2="190" stroke="#21262d"/>
<circle cx="37" cy="218" r="5" fill="{status_color}"/>
<text x="51" y="223" fill="{status_color}" font-size="14" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{status}</text>
<text x="430" y="223" fill="#58a6ff" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">OPEN ↗</text>
</svg>'''

def render_telemetry(rows):
    total_stars = sum(r["data"].get("stargazers_count", 0) for r in rows)
    total_forks = sum(r["data"].get("forks_count", 0) for r in rows)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    project_rows = []
    y = 124
    for row in rows:
        status, color = status_from(row["data"].get("pushed_at"))
        project_rows.append(
            f'<text x="40" y="{y}" fill="#e6edf3" font-size="15" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{esc(row["cfg"]["title"])}</text>'
            f'<circle cx="365" cy="{y-5}" r="5" fill="{color}"/>'
            f'<text x="379" y="{y}" fill="{color}" font-size="13" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{status}</text>'
            f'<text x="500" y="{y}" text-anchor="end" fill="#8b949e" font-size="13" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{esc(age_label(row["data"].get("pushed_at")))}</text>'
        )
        y += 31

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="245" viewBox="0 0 1040 245">
<rect width="1040" height="245" rx="16" fill="#0d1117"/>
<rect x="1" y="1" width="1038" height="243" rx="15" fill="none" stroke="#30363d"/>
<text x="38" y="42" fill="#58d8ff" font-size="22" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">&gt; PROFILE TELEMETRY</text>
<text x="38" y="75" fill="#8b949e" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">manual snapshot · generated {generated}</text>
{''.join(project_rows)}
<line x1="540" y1="42" x2="540" y2="207" stroke="#21262d"/>
<text x="585" y="76" fill="#8b949e" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">TRACKED PROJECTS</text>
<text x="585" y="115" fill="#e6edf3" font-size="25" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{len(rows)}</text>
<text x="720" y="76" fill="#8b949e" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">TOTAL STARS</text>
<text x="720" y="115" fill="#e6edf3" font-size="25" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{total_stars}</text>
<text x="850" y="76" fill="#8b949e" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">TOTAL FORKS</text>
<text x="850" y="115" fill="#e6edf3" font-size="25" font-weight="700" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{total_forks}</text>
<text x="585" y="166" fill="#6ee7b7" font-size="14" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">[ LINK STATUS ] ACTIVE</text>
<text x="585" y="195" fill="#8b949e" font-size="13" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">refreshes only when you press Run workflow</text>
</svg>'''

rows = []
for cfg in PROJECTS:
    try:
        data = github_json(f"/repos/{OWNER}/{cfg['repo']}")
    except Exception as exc:
        print(f"warning: failed to fetch {cfg['repo']}: {exc}")
        data = {"stargazers_count": 0, "forks_count": 0, "language": "Unknown", "pushed_at": None}
    rows.append({"cfg": cfg, "data": data})
    (OUT / f"{cfg['repo'].lower()}-card.svg").write_text(render_card(cfg, data), encoding="utf-8")

(OUT / "profile-telemetry.svg").write_text(render_telemetry(rows), encoding="utf-8")
print("Profile cards generated.")
