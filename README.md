# Nexwall partner release notes

Static release-notes site (en, es, pt-BR) in the style of releasenotes.nexwall.com.br. Python 3, no dependencies.

- `content/site.json` product name, links, host
- `content/releases.json` releases, newest first
- `content/<version>/<lang>.json` notes of one version (items tagged new, improved, changed, fixed)
- `python3 build.py` writes `site/`; every push to main publishes it (`.github/workflows/pages.yml`)
