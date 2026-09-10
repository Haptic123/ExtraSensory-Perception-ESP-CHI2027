# Editing the documentation

Edit Markdown in `markdown/` and commit to `main`. GitHub Actions builds and publishes the website automatically. Sign in as the neutral publishing account when editing.

| Content | Source |
| --- | --- |
| Homepage and hub | `markdown/page-48.md` |
| System architecture | `markdown/page-45.md` |
| Installation | `markdown/page-18.md` |

Use the page number in a website URL to find its Markdown file. The homepage and the hub page are generated from the same source. Do not edit `docs/*.html` for future changes: those files are the previous deployment snapshot, and the automated deployment replaces the website from the Markdown build.

Keep emoji characters as normal UTF-8 text. Place diagrams between triple-backtick fences to preserve wording and spacing. Link to other source pages using relative Markdown links such as `[Architecture](page-45.md)`; the build converts them to website links.

This setup supports editing the existing 48 pages. Adding or removing pages also requires updating navigation in `scripts/design.py` and homepage references. Images and external links are not currently supported by the site validation; ask for a reviewed asset/links update when needed. New edits are not automatically anonymized, so retain the existing redactions.

## One-time activation

In Settings → Pages, change Source to **GitHub Actions**. Then open Actions → Build and publish documentation → Run workflow. Future pushes to main run automatically. The workflow reports broken internal links and conversion failures rather than publishing an incomplete build.

## Local preview

Install Python 3.12, then run `pip install -r requirements.txt` and `python scripts/build.py`. Open `_site/index.html`. The build does not modify the Markdown source.
