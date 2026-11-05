# Meghan Botkin — Design Studio draft

Open **index.html** in a current desktop browser. The studio is self-contained: no installation or server is needed. The original source-board images and export library are embedded in the file.

## Using the studio

1. Choose **301 Kearsarge** or **93 Main Street**, then choose a space.
2. Change the material dropdowns to compare compatible choices from either board. **Omit from presentation** removes that choice from the slides. Use **Browse all materials** to search the full catalog and add a choice to the current space.
3. Edit the project title, slide titles, presentation notes, theme, and slide order. Selections update the preview immediately. **Undo last change** reverses edits made during the current visit.
4. Use **Present** for the slideshow. Arrow keys move between slides; Escape exits.
5. Use **Download** for an editable PowerPoint, an offline HTML slideshow, a project JSON backup, or the browser's print/save-as-PDF dialog.
6. Use **Open saved project** to restore a JSON backup. Each board keeps its own project in this browser's local storage. Download backups before clearing browser data or moving to another browser.

## Source coverage

- **Material Board - slim down - updated 4.pdf**: 301 Kearsarge, four pages.
- **Copy of Material Board - updated 7-28-26.pdf**: 93 Main Street, five pages.
- All **84 source images** are represented in the catalog, with **20 additional text-only choices or instructions**, for **104 entries** in total.
- The source-board viewer includes all nine pages. Every catalog entry identifies its source board and page; product links are preserved when supplied.
- Repeated products remain separate where the boards place them in different rooms. Reference images and unresolved instructions are labeled. The initial selections reproduce the boards; they are not a new approval or a finalized design.
- Source PDFs are included in `sources/`. Their Drive links and SHA-256 hashes appear in `source-manifest.json`. `catalog-inventory.csv` provides a readable inventory.

## Files and compatibility

- `index.html`: ready-to-open draft website, with no external runtime dependencies.
- `app.js`, `studio.template.html`, `catalog.json`, `build_site.py`: editable website source. Running `python build_site.py` rebuilds `index.html` after source edits.
- `build_catalog.py`, `extract_sources.py`: source extraction and catalog build scripts.
