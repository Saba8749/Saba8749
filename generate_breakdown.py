import json
import math
import urllib.request

def fetch_repos():
    url = "https://api.github.com/users/Saba8749/repos?per_page=100"
    req = urllib.request.Request(url, headers={"User-Agent": "breakdown-svg-generator"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

def count_languages(repos):
    counts = {}
    for repo in repos:
        lang = repo.get("language") or "Config / Shell"
        counts[lang] = counts.get(lang, 0) + 1
    return counts

def generate_svg(counts):
    total = sum(counts.values())

    COLORS = {
        "C":              "#58a6ff",
        "Python":         "#3fb950",
        "Config / Shell": "#6e7681",
        "JavaScript":     "#f1e05a",
        "Shell":          "#89e051",
        "Makefile":       "#427819",
    }
    DEFAULT_COLOR = "#a371f7"

    # Sort by count descending, group unknowns at end
    ordered = sorted(counts.items(), key=lambda x: -x[1])

    circumference = 2 * math.pi * 78

    segments = []
    angle = -90
    for lang, count in ordered:
        color = COLORS.get(lang, DEFAULT_COLOR)
        pct = count / total
        arc = pct * circumference
        segments.append({
            "lang": lang, "color": color,
            "count": count, "arc": arc, "angle": angle
        })
        angle += pct * 360

    # Rows
    rows_svg = ""
    y = 102
    for seg in segments:
        label = f'{seg["count"]} project{"s" if seg["count"] != 1 else ""}'
        rows_svg += f'''
  <rect x="72" y="{y}" width="12" height="12" fill="{seg['color']}" rx="2"/>
  <text x="94" y="{y+11}" font-family="monospace" font-size="14" fill="#e6edf3">{seg['lang']}</text>
  <text x="300" y="{y+11}" font-family="monospace" font-size="14" fill="#8b949e">{label}</text>'''
        y += 36

    # Donut
    donut_svg = '  <circle cx="655" cy="138" r="78" fill="none" stroke="#21262d" stroke-width="26"/>\n'
    for seg in segments:
        donut_svg += f'  <circle cx="655" cy="138" r="78" fill="none" stroke="{seg["color"]}" stroke-width="24" stroke-dasharray="{seg["arc"]:.2f} {circumference:.2f}" transform="rotate({seg["angle"]:.2f} 655 138)"/>\n'

    svg = f'''<svg width="800" height="260" viewBox="0 0 800 260" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
  </defs>
  <rect width="800" height="260" rx="14" fill="url(#bg)"/>
  <rect width="800" height="260" rx="14" fill="none" stroke="#30363d" stroke-width="1"/>
  <text x="72" y="62" font-family="monospace" font-size="13" fill="#8b949e" letter-spacing="5">PROJECT BREAKDOWN</text>
  <line x1="72" y1="74" x2="480" y2="74" stroke="#21262d" stroke-width="1"/>
{rows_svg}
  <line x1="72" y1="210" x2="480" y2="210" stroke="#21262d" stroke-width="1"/>
  <text x="72" y="234" font-family="monospace" font-size="13" fill="#8b949e">Currently</text>
  <text x="300" y="234" font-family="monospace" font-size="13" fill="#e6edf3">42 Core Curriculum</text>
{donut_svg}
  <text x="655" y="130" font-family="monospace" font-size="34" fill="#e6edf3" text-anchor="middle" font-weight="bold">{total}</text>
  <text x="655" y="153" font-family="monospace" font-size="12" fill="#8b949e" text-anchor="middle">projects</text>
</svg>'''

    return svg

repos = fetch_repos()
counts = count_languages(repos)
svg = generate_svg(counts)

with open("breakdown.svg", "w") as f:
    f.write(svg)

print(f"Done — {sum(counts.values())} repos: {counts}")
