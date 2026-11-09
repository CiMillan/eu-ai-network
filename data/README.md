# Data

The network, frozen. Don't edit `nodes.csv` or `edges.csv`; `manifest.json` holds their checksums.

- Source: Stanford CRFM's Ecosystem Graphs (https://github.com/stanford-crfm/ecosystem-graphs), commit `d3c06a4`, cleaned.
- `nodes.csv`: 742 nodes = 359 models, 112 datasets, 97 applications, 174 outside sources (type `external`, no organisation). Columns: name, type, organization, created_date, access, license, modality.
- `edges.csv`: 751 directed links, `upstream → downstream` = "upstream is used to build downstream".

## Region tags: `regions.csv`

One row per organisation string in `nodes.csv` (192), largest first. Fill in:

- `region`: EU, US, China or other (headquarters).
- `source_url`: the page that shows it, e.g. the organisation's own site.
- `tagged_by`: your name.
- `note`: anything unsure. For collaborations (several organisations in one string), see the open decision in `PLAN.md`.
