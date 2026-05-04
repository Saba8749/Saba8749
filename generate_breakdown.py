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
        "C":              "#79c0ff",
        "Python":         "#a371f7",
        "Config / Shell": "#6e7681",
        "JavaScript":     "#f1e05a",
        "Shell":          "#89e051",
        "Makefile":       "#427819",
    }
    DEFAULT_COLOR = "#ffa657"

    ordered = sorted(counts.items(), key=lambda x: -x[1])
    BAR_WIDTH = 300

    rows_svg = ""
    y = 155
    for lang, count in ordered:
        color = COLORS.get(lang, DEFAULT_COLOR)
        pct = count / total
        fill = int(pct * BAR_WIDTH)
        pct_label = f"{int(pct*100)}%"
        count_label = f"{count} repo{'s' if count != 1 else ''}"
        rows_svg += f'''
  <text x="52" y="{y}" font-family="monospace" font-size="12" fill="#768390">❯</text>
  <text x="70" y="{y}" font-family="monospace" font-size="12" fill="{color}" font-weight="bold">{lang}</text>
  <rect x="240" y="{y-13}" width="{BAR_WIDTH}" height="14" rx="3" fill="#1c2128"/>
  <rect x="240" y="{y-13}" width="{fill}" height="14" rx="3" fill="{color}" opacity="0.75"/>
  <text x="552" y="{y}" font-family="monospace" font-size="12" fill="{color}">{pct_label}</text>
  <text x="600" y="{y}" font-family="monospace" font-size="12" fill="#768390">{count_label}</text>'''
        y += 42

    footer_y = y + 10
    height = footer_y + 60

    svg = f'''<svg width="800" height="{height}" viewBox="0 0 800 {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1f35"/>
      <stop offset="100%" style="stop-color:#0d1117"/>
    </linearGradient>
    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1e3a5f"/>
      <stop offset="50%" style="stop-color:#2d2b6b"/>
      <stop offset="100%" style="stop-color:#1a3a5c"/>
    </linearGradient>
    <clipPath id="roundAll"><rect width="800" height="{height}" rx="14"/></clipPath>
  </defs>
  <rect width="800" height="{height}" rx="14" fill="url(#bgGrad)"/>
  <rect width="800" height="{height}" rx="14" fill="none" stroke="#30363d" stroke-width="1"/>
  <path d="M0,0 Q200,38 400,22 Q600,6 800,30 L800,0 Z" fill="url(#waveGrad)" opacity="0.9" clip-path="url(#roundAll)"/>
  <path d="M0,{height} Q200,{height-38} 400,{height-22} Q600,{height-6} 800,{height-30} L800,{height} Z" fill="url(#waveGrad)" opacity="0.9" clip-path="url(#roundAll)"/>
  <circle cx="48" cy="46" r="6" fill="#ff5f57"/>
  <circle cx="68" cy="46" r="6" fill="#febc2e"/>
  <circle cx="88" cy="46" r="6" fill="#28c840"/>
  <text x="400" y="51" font-family="monospace" font-size="12" fill="#768390" text-anchor="middle">saba@42school: ~/stats</text>
  <line x1="32" y1="64" x2="768" y2="64" stroke="#2d3a4a" stroke-width="1"/>
  <text x="52" y="92" font-family="monospace" font-size="13" fill="#a371f7">~</text>
  <text x="68" y="92" font-family="monospace" font-size="13" fill="#768390">❯</text>
  <text x="86" y="92" font-family="monospace" font-size="13" fill="#cdd9e5">git stats --languages</text>
  <line x1="52" y1="104" x2="748" y2="104" stroke="#2d3a4a" stroke-width="1"/>
  <text x="70"  y="122" font-family="monospace" font-size="11" fill="#4a5568">LANGUAGE</text>
  <text x="240" y="122" font-family="monospace" font-size="11" fill="#4a5568">USAGE</text>
  <text x="552" y="122" font-family="monospace" font-size="11" fill="#4a5568">PCT</text>
  <text x="600" y="122" font-family="monospace" font-size="11" fill="#4a5568">REPOS</text>
  <line x1="52" y1="130" x2="748" y2="130" stroke="#2d3a4a" stroke-width="1"/>
{rows_svg}
  <line x1="52" y1="{footer_y}" x2="748" y2="{footer_y}" stroke="#2d3a4a" stroke-width="1"/>
  <text x="52"  y="{footer_y+22}" font-family="monospace" font-size="12" fill="#768390">total</text>
  <text x="240" y="{footer_y+22}" font-family="monospace" font-size="12" fill="#cdd9e5">{total} repos  ·  42 Core Curriculum</text>
  <rect x="86" y="{footer_y+32}" width="8" height="13" fill="#a371f7" opacity="0.8">
    <animate attributeName="opacity" values="0.8;0;0.8" dur="1.2s" repeatCount="indefinite"/>
  </rect>
</svg>'''
    return svg

repos = fetch_repos()
counts = count_languages(repos)
svg = generate_svg(counts)

with open("breakdown.svg", "w") as f:
    f.write(svg)

print(f"Done — {sum(counts.values())} repos: {counts}")
