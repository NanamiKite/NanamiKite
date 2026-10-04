#!/usr/bin/env python3
import json, os, urllib.request, html
from pathlib import Path
from datetime import datetime, timezone

OWNER = "NanamiKite"
OUT = Path("assets/generated")

PROJECTS = [
    ("DirectHCI", "directhci", "DirectHCI", "Windows Raw HCI infrastructure", ["Rust","Windows","WinUSB","HCI"], "#249cd2", "#58d8ff"),
    ("FLOW-8-PC-Controller", "flow8", "FLOW 8 PC Controller", "Native BLE desktop control", ["Rust","BLE/GATT","Protocol RE"], "#2ea06f", "#6ee7b7"),
    ("CodeRecoil-for-Coyote-2.0", "coderecoil", "CodeRecoil", "Editor events to physical feedback", ["JavaScript","VS Code","BLE"], "#d29922", "#f7b955"),
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

def make(title, subtitle, tags, accent, theme, data):
    if theme == "light":
        bg, border, text, muted, pillbg = "#f6f8fa", "#d0d7de", "#24292f", "#57606a", "#ffffff"
    else:
        bg, border, text, muted, pillbg = "#0d1117", "#30363d", "#e6edf3", "#b1bac4", "#111820"

    x = 22
    pills=[]
    for tag in tags:
        w = 18 + len(tag)*7.2
        pills.append(
            f'<rect x="{x:.1f}" y="98" width="{w:.1f}" height="24" rx="12" fill="{pillbg}" stroke="{accent}"/>'
            f'<text x="{x+9:.1f}" y="114" fill="{text}" font-size="11.8" '
            f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(tag)}</text>'
        )
        x += w + 6

    meta = f'★ {data.get("stargazers_count",0)}   forks {data.get("forks_count",0)}   ● {data.get("language") or "Mixed"}   updated {age(data.get("pushed_at"))}'

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="390" height="140" viewBox="0 0 390 140">'
        f'<rect width="390" height="140" rx="13" fill="{bg}"/>'
        f'<rect x="1" y="1" width="388" height="138" rx="12" fill="none" stroke="{border}"/>'
        f'<rect x="0" y="0" width="5" height="140" rx="2.5" fill="{accent}"/>'
        f'<text x="22" y="32" fill="{accent}" font-size="20" font-weight="700" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(title)}</text>'
        f'<text x="22" y="59" fill="{text}" font-size="14" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(subtitle)}</text>'
        f'<text x="22" y="82" fill="{muted}" font-size="11.5" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">{html.escape(meta)}</text>'
        + ''.join(pills)
        + '</svg>'
    )

OUT.mkdir(parents=True, exist_ok=True)
for repo,key,title,subtitle,tags,accent_light,accent_dark in PROJECTS:
    data = fetch(repo)
    (OUT/f"{key}-light.svg").write_text(make(title,subtitle,tags,accent_light,"light",data), encoding="utf-8")
    (OUT/f"{key}-dark.svg").write_text(make(title,subtitle,tags,accent_dark,"dark",data), encoding="utf-8")

print("cards refreshed")
