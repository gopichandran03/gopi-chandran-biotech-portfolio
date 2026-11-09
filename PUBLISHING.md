# Publishing and maintaining this site

The portfolio is published with GitHub Pages from the repository root.

- Live site: <https://gopichandran03.github.io/gopi-chandran-biotech-portfolio/>
- Settings → Pages → deploy from `main`, folder `/ (root)`

## Making a change

Everything is static — no build step is needed to publish, and no server is
required to preview.

```bash
git clone https://github.com/gopichandran03/gopi-chandran-biotech-portfolio.git
cd gopi-chandran-biotech-portfolio
python3 -m http.server 8000      # then open http://localhost:8000
```

Edit, commit, push. Pages redeploys within a minute or two.

## Changing a project walkthrough

Walkthrough pages under `projects/` are **generated** — do not edit them by
hand, because the next build will overwrite your changes.

1. Edit the matching content module in `scripts/content/`
   (for example `scripts/content/ricestressdb.py`).
2. Rebuild:
   ```bash
   python3 scripts/build_pages.py
   ```
3. Commit both the content module and the regenerated pages.

`python3 scripts/build_pages.py --check` renders without writing, which is a
quick way to confirm a module still parses.

To add a tenth project: create `scripts/content/<slug_with_underscores>.py`
exposing a `PAGE` dict shaped like the existing ones, add its slug to `ORDER`
in `scripts/build_pages.py`, rebuild, and add a card to the projects grid in
`index.html`.

## Checking before you push

```bash
# every workflow tool still runs
python3 workflows/ssr_finder/find_ssrs.py --demo
python3 workflows/rice_stress_db/query_demo.py
python3 workflows/quality_control/process_monitor.py --fault shift
python3 workflows/rnaseq/qc_summary.py --counts workflows/rnaseq/data/example_counts.tsv

# pages still render
python3 scripts/build_pages.py --check
```

Then open a couple of walkthrough pages in a browser and click through the
slides — the interactive demos are plain JavaScript with no dependencies, so if
they work locally they work on Pages.

## Things to keep true

- **Do not upload** proprietary data, unpublished collaborators' data, or
  restricted research materials.
- **Keep the data labels honest.** Pages that run on synthetic or example data
  say so in a visible note. If you swap in real data, update the note.
- **Keep the citations attached.** Each walkthrough's final slide carries the
  sources for its factual claims. If you change a claim, change the source.
- **Verify any claim that goes stale** — titles, dates, counts, registration
  numbers — before publishing a new version.

## Assets

- `assets/gopi-chandran-professional.jpg` — portrait used on the home page
- `assets/css/deck.css` — shared styling for walkthrough pages
- `assets/js/deck.js` — slide navigation (keyboard, swipe, buttons)

Keep the `assets/` paths intact; the pages reference them relatively.
