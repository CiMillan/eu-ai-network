# Data

The network, frozen. Don't edit `nodes.csv` or `edges.csv`; `manifest.json` holds their checksums.

- Source: Stanford CRFM's Ecosystem Graphs (https://github.com/stanford-crfm/ecosystem-graphs), commit `d3c06a4`, cleaned.
- `nodes.csv`: 742 nodes = 359 models, 112 datasets, 97 applications, 174 outside sources (type `external`, no organisation). Columns: name, type, organization, created_date, access, license, modality.
- `edges.csv`: 751 directed links, `upstream → downstream` = "upstream is used to build downstream".

## Region tags: `regions.csv`

One row per organisation string in `nodes.csv` (192), largest first. `region` is pre-filled as a first guess; we check it.

- `region`: EU, US, China or other (headquarters). `mixed` = a collaboration across regions, until we settle the open decision in `PLAN.md`.
- `source_url`: the page that shows it, e.g. the organisation's own site. The checker adds it.
- `checked_by`: who checks this row (48 each, rows dealt in turn so everyone gets big and small ones).
- `note`: why the guess. "unsure, please check" marks the 33 rows to look at hardest. UK and Switzerland are tagged `other` with a note "Europe, not EU".
