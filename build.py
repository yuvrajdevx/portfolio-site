"""
build.py — turns /incidents/*.md, /experience/*.md, and /certs/*.md into their
respective sections of index.html.

Usage:
    python build.py

Reads:
    template.html        — the site, with placeholder comments for each section
    incidents/*.md         — one file per incident (see incidents/README below)
    experience/*.md        — one file per job (optional — empty state if none)
    certs/*.md              — one file per certification (optional — empty state if none)

Writes:
    dist/index.html       — the finished, deployable site
"""

import os
import re
import yaml
import markdown

INCIDENTS_DIR = "incidents"
EXPERIENCE_DIR = "experience"
CERTS_DIR = "certs"
TEMPLATE_FILE = "template.html"
OUTPUT_DIR = "dist"

SEV_CLASS = {"SEV1": "sev1", "SEV2": "sev2", "SEV3": "sev3"}


def parse_frontmatter_file(path):
    """Generic parser: YAML frontmatter + optional markdown body."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError(f"{path} is missing YAML frontmatter (---\\n...\\n---)")

    front, body = match.groups()
    meta = yaml.safe_load(front) or {}
    meta["body_html"] = markdown.markdown(body.strip()) if body.strip() else ""
    meta["_filename"] = os.path.basename(path)
    return meta


def parse_incident(path):
    return parse_frontmatter_file(path)


def load_entries(dir_path):
    """Load and parse every .md file in a directory. Returns [] if the dir doesn't exist."""
    if not os.path.isdir(dir_path):
        return []
    entries = []
    for fname in sorted(os.listdir(dir_path)):
        if fname.endswith(".md"):
            entries.append(parse_frontmatter_file(os.path.join(dir_path, fname)))
    return entries


def render_experience(meta):
    role = meta.get("role", "")
    company = meta.get("company", "")
    start = meta.get("start", "")
    end = meta.get("end") or "Present"
    location = meta.get("location", "")
    date_range = f"{start} — {end}" if start else end
    location_html = f'<span class="exp-location">{location}</span>' if location else ""

    return f"""      <div class="exp-entry">
        <div class="exp-top">
          <div class="exp-role">{role}</div>
          <div class="exp-company">{company}</div>
        </div>
        <div class="exp-meta mono">{date_range}{location_html}</div>
        <div class="exp-body">
          {meta['body_html']}
        </div>
      </div>
"""


def render_cert(meta):
    name = meta.get("name", "")
    issuer = meta.get("issuer", "")
    date = meta.get("date", "")
    expires = meta.get("expires", "")
    verify_url = meta.get("verify_url", "")
    verify_html = (
        f'<a href="{verify_url}" class="cert-verify" target="_blank" rel="noopener">Verify →</a>'
        if verify_url else ""
    )
    meta_parts = [p for p in [issuer, date, (f"expires {expires}" if expires else "")] if p]
    body_html = meta.get("body_html", "")
    body_div = f'<div class="cert-body">{body_html}</div>' if body_html else ""

    return f"""      <div class="cert-entry">
        <div class="cert-name">{name}</div>
        <div class="cert-meta mono">{" · ".join(meta_parts)}</div>
        {body_div}
        {verify_html}
      </div>
"""


def render_incident(meta):
    sev = str(meta.get("severity", "SEV3")).upper()
    sev_class = SEV_CLASS.get(sev, "sev3")
    client = meta.get("client", "")
    client_html = f'<p class="incident-meta">{client}</p>' if client else ""
    pinned = bool(meta.get("pinned", False))
    pin_html = '<span class="pin-badge">📌 pinned</span>' if pinned else ""
    incident_class = "incident pinned" if pinned else "incident"

    return f"""      <details class="{incident_class}">
        <summary>
          <span class="sev {sev_class}">{sev}</span>
          <span class="incident-title">{meta['title']}</span>
          {pin_html}
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
    # Tolerant of a missing/empty incidents/ dir — Git doesn't track empty
    # directories, so a freshly-cleared incidents/ folder won't exist at all
    # right after a push, until the first real incident file lands in it.
    incidents = load_entries(INCIDENTS_DIR)

    # Most recent first (dates are "YYYY-MM" strings, so string sort works)
    incidents.sort(key=lambda m: str(m["date"]), reverse=True)

    # Pinned incidents (frontmatter: `pinned: true`) float to the top,
    # most-recent-first within each group.
    pinned = [m for m in incidents if m.get("pinned")]
    unpinned = [m for m in incidents if not m.get("pinned")]
    incidents = pinned + unpinned

    html_blocks = "\n".join(render_incident(m) for m in incidents)

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    if "<!-- INCIDENTS -->" not in template:
        raise SystemExit("template.html is missing the <!-- INCIDENTS --> placeholder.")
    if "__SEV_BREAKDOWN__" not in template:
        raise SystemExit("template.html is missing the __SEV_BREAKDOWN__ placeholder.")

    # Severity breakdown line above the Incident Log, e.g. "3 SEV1 · 6 SEV2 · 5 SEV3"
    sev_counts = {"SEV1": 0, "SEV2": 0, "SEV3": 0}
    for m in incidents:
        sev = str(m.get("severity", "SEV3")).upper()
        if sev not in sev_counts:
            sev = "SEV3"
        sev_counts[sev] += 1
    sev_breakdown = " · ".join(
        f'<span class="b-{sev.lower()}">{count} {sev}</span>'
        for sev, count in sev_counts.items()
        if count > 0
    )

    output = template.replace("<!-- INCIDENTS -->", html_blocks)
    output = output.replace("__SEV_BREAKDOWN__", sev_breakdown)

    # ---------- Experience ----------
    if "<!-- EXPERIENCE -->" not in template:
        raise SystemExit("template.html is missing the <!-- EXPERIENCE --> placeholder.")

    experience = load_entries(EXPERIENCE_DIR)
    experience.sort(key=lambda m: str(m.get("start", "")), reverse=True)

    if experience:
        experience_html = "\n".join(render_experience(m) for m in experience)
    else:
        experience_html = (
            '      <p class="section-empty mono">'
            "Full write-up coming soon — see the Incident Log and Projects above for real work in the meantime."
            "</p>\n"
        )

    output = output.replace("<!-- EXPERIENCE -->", experience_html)

    # ---------- Certifications ----------
    if "<!-- CERTS -->" not in template:
        raise SystemExit("template.html is missing the <!-- CERTS --> placeholder.")

    certs = load_entries(CERTS_DIR)
    certs.sort(key=lambda m: str(m.get("date", "")), reverse=True)

    if certs:
        certs_html = "\n".join(render_cert(m) for m in certs)
    else:
        certs_html = '      <p class="section-empty mono">None yet — check back soon.</p>\n'

    output = output.replace("<!-- CERTS -->", certs_html)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(
        f"Built {len(incidents)} incident(s), {len(experience)} experience entr{'y' if len(experience) == 1 else 'ies'}, "
        f"and {len(certs)} cert(s) into {out_path}"
    )


if __name__ == "__main__":
    main()
