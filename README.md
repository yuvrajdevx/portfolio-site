# Portfolio

A status-page-styled portfolio site. Incidents live as markdown files and get
built into the site automatically on every push.

## How it's structured

```
template.html              the site (edit this for your name, projects, skills, links)
incidents/*.md              one file per incident — this is what you'll add to over time
build.py                    reads incidents/*.md + template.html → dist/index.html
requirements.txt            build dependencies (markdown, pyyaml)
.github/workflows/deploy.yml   auto-builds and deploys on every push to main
```

## Adding a new incident (this is the part you'll actually use)

Create a new file in `incidents/`, named however you like, e.g.
`incidents/2026-03-cache-stampede.md`:

```markdown
---
title: A one-line summary of what happened
date: "2026-03"
severity: SEV2
client: Short anonymized description, e.g. "Healthcare client, patient portal"
---
**Symptom**

What users or systems experienced.

**Investigation**

How you tracked it down.

**Root cause**

What was actually wrong.

**Fix**

What you did to resolve it.

**Prevention**

What changed so it doesn't happen again.
```

`severity` can be `SEV1`, `SEV2`, or `SEV3` — anything else falls back to SEV3 styling.
`date` should be `"YYYY-MM"` in quotes, so incidents sort correctly (newest first).

Commit and push. GitHub Actions rebuilds and redeploys the site automatically —
nothing else to do.

**A reminder on NDAs:** anonymize client names, exact traffic/revenue figures, and
anything identifying. Keep the technical substance, change the specifics.

## First-time setup

1. Create a new **public** repo on GitHub (private repos need a paid plan for Pages
   on personal accounts, though GitHub Pages itself is free either way for public repos).
2. Push this folder to it:
   ```bash
   cd portfolio-repo
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
3. In the repo on GitHub: **Settings → Pages → Source → Deploy from a branch →
   `gh-pages` branch → `/ (root)`**. (The `gh-pages` branch appears automatically
   after the first Action run finishes — give it a minute after your first push.)
4. Your site will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO/`.
   If you want it at the root (`YOUR_USERNAME.github.io`), name the repo exactly
   `YOUR_USERNAME.github.io`.
5. Optional: buy a domain (~$10–15/year from Namecheap, Porkbun, etc.) and point it
   at GitHub Pages via a `CNAME` file + DNS records — GitHub's docs walk through this
   under Pages → Custom domain.

## Editing everything else

Projects, skills, hero stats, and contact links live directly in `template.html` —
edit that file the same way you'd edit any HTML/CSS/JS, then push. Only incidents
are pulled from a separate folder, since those are the thing you'll add to most often.

## Why this setup

- **Free**: GitHub repo + GitHub Pages + GitHub Actions all free for public repos.
- **Nothing is ever lost**: every incident is a committed file with full git history.
  Delete something by accident, `git log` and `git checkout` bring it back.
- **Low friction to add content**: a new incident is "write a markdown file, git push."
  No CMS, no database, no server to maintain.
