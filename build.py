"""
build.py — turns /incidents/*.md into the Incident Log section of index.html.

Usage:
    python build.py

Reads:
    template.html        — the site, with an <!-- INCIDENTS --> placeholder
    incidents/*.md        — one file per incident (see incidents/README below)

Writes:
    dist/index.html       — the finished, deployable site
"""

import os
import re
import yaml
import markdown

INCIDENTS_DIR = "incidents"
TEMPLATE_FILE = "template.html"
OUTPUT_DIR = "dist"

SEV_CLASS = {"SEV1": "sev1", "SEV2": "sev2", "SEV3": "sev3"}


def parse_incident(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter (---\\n...\\n---)")

    front, body = match.groups()
    meta = yaml.safe_load(front)
    meta["body_html"] = markdown.markdown(body.strip())
    meta["_filename"] = os.path.basename(path)
    return meta


def render_incident(meta):
    sev = str(meta.get("severity", "SEV3")).upper()
    sev_class = SEV_CLASS.get(sev, "sev3")
    client = meta.get("client", "")
    client_html = f'<p class="incident-meta">{client}</p>' if client else ""

    return f"""      <details class="incident">
        <summary>
          <span class="sev {sev_class}">{sev}</span>
          <span class="incident-title">{meta['title']}</span>
          <span class="incident-date">{meta['date']}</span>
          <span class="chevron">▶</span>
        </summary>
        <div class="incident-body">
          {client_html}
          {meta['body_html']}
        </div>
      </details>
"""


def main():
    if not os.path.isdir(INCIDENTS_DIR):
        raise SystemExit(f"No '{INCIDENTS_DIR}/' directory found.")

    incidents = []
    for fname in sorted(os.listdir(INCIDENTS_DIR)):
        if fname.endswith(".md"):
            incidents.append(parse_incident(os.path.join(INCIDENTS_DIR, fname)))

    # Most recent first (dates are "YYYY-MM" strings, so string sort works)
    incidents.sort(key=lambda m: str(m["date"]), reverse=True)

    html_blocks = "\n".join(render_incident(m) for m in incidents)

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    if "<!-- INCIDENTS -->" not in template:
        raise SystemExit("template.html is missing the <!-- INCIDENTS --> placeholder.")

    output = template.replace("<!-- INCIDENTS -->", html_blocks)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Built {len(incidents)} incident(s) into {out_path}")


if __name__ == "__main__":
    main()
