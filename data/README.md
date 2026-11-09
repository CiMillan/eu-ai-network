# Data

The network, frozen. Don't edit `nodes.csv` or `edges.csv`; `manifest.json` holds their checksums.

- Source: Stanford CRFM's Ecosystem Graphs (https://github.com/stanford-crfm/ecosystem-graphs), commit `d3c06a4`, cleaned.
- `nodes.csv`: 742 nodes = 359 models, 112 datasets, 97 applications, 174 outside sources (type `external`, no organisation). Columns: name, type, organization, created_date, access, license, modality.
- `edges.csv`: 751 directed links, `upstream → downstream` = "upstream is used to build downstream".

## Region tags: `regions.csv`

One row per organisation string in `nodes.csv` (192), largest first. `region` is pre-filled as a first guess; we check it.

- `region`: EU, US, China or other (headquarters). `mixed` = a collaboration across regions, until we settle the open decision in the [main README](../README.md#open-decisions).
- `source_url`: the page that shows it, e.g. the organisation's own site. The checker adds it.
- `checked_by`: who checks this row. 48 rows each, in blocks: Ifeoluwa rows 1–48, Sofiia 49–96, Cintia 97–144, Ella 145–192.
- `note`: why the guess. "unsure, please check" marks the 33 rows to look at hardest. UK and Switzerland are tagged `other` with a note "Europe, not EU".

## How to send your changes

Easiest, all in the browser:

1. Open [`regions.csv`](regions.csv) on GitHub and click the pencil icon ("Edit this file").
2. Change only your own rows: fix `region` if wrong, paste the page in `source_url`.
3. Click **Commit changes**, pick **"Create a new branch for this commit and start a pull request"**, then **Propose changes** and **Create pull request**.
4. Cintia reviews and merges it.

Do it in one go, or one pull request per sitting; both are fine. Because each of us edits a separate block of rows, the pull requests don't clash.

Keep commas inside quotes: a name like `"Avignon University, Nantes University"` keeps its quotes. If you work in Excel or Google Sheets instead, export as CSV (UTF-8) and upload it the same way ("Add file" → "Upload files"), but say so in the pull request so we check nothing else changed.
