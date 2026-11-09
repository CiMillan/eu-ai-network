# Plan: Europe in the AI network

Group F · Applied Network Analysis 2026/27 · final slides due **Sun 10 Jan 2027, 15:59** (PDF on Moodle, course template).

## What the course asks (Project Description, rubric)

- **C2, 20%:** N, L, density, average degree, degree distribution (plot), clustering, average path length and diameter (largest component), connected components, how we handle direction.
- **C3, 25%:** at least two centrality measures; community detection with modularity, or robustness; a calibrated null model; a sensitivity check.
- **C4, 20%:** for every number: what we expected, the random reference, how it compares, what we learned.
- **C1, C5, C6:** research question, template and figures, a 10-minute talk by one member, Q&A for everyone.
- Lab 4 tip: use two null models, the random twin (same N and L, `nx.gnm_random_graph`) and the configuration model (same degrees).

## Our four questions (from the proposal)

1. Who does Europe build on?
2. Who builds on Europe?
3. Which hubs hold it up? (centrality, then removing hubs)
4. How did it change, 2019 → 2024? (yearly snapshots vs a null model)

## Steps and dates

| week | course class | what we finish | notebook | rubric |
|---|---|---|---|---|
| 9 Nov | Lab 4, random models | split agreed; region tags started (`data/regions.csv`) | | |
| 16 Nov | Lab 5, centrality and communities. Weekly 60-second updates start | basics; tags done by Sun 22 Nov | `01_basics` | C2 |
| 23 Nov | Lecture, diffusion | null models; questions 1 and 2 | `02_null_models`, `03_europe_both_ways` | C3, C4 |
| 30 Nov | Lab 6, vulnerability (attack simulator) | centrality and communities; question 3, removing hubs vs random removal | `04_centrality_communities`, `05_robustness` | C3 |
| 7 Dec | Lecture, GNNs and link prediction | question 4, yearly snapshots; sensitivity check | `06_time_and_sensitivity` | C3, C4 |
| 14 Dec | Lab 7, motifs (last class) | results frozen; presenter chosen; first slide draft | | C5 |
| Fri 18 Dec | | full slide draft (our own deadline) | | |
| 18 Dec – 3 Jan | | rehearse; Q&A prep for everyone | | C6 |
| **Sun 10 Jan, 15:59** | | **slides PDF on Moodle** | | |
| January (date to be set) | | 10-minute talk | | |

## Workstreams (one owner each)

| workstream | owner |
|---|---|
| Data and region tags | |
| Basics and null models | |
| Centrality and communities | |
| Robustness and time | |

Everyone tags organisations in week one (about 48 each).

## Open decisions

- Organisations listed together (e.g. "Avignon University, Nantes University"): how do we tag a collaboration? One region per partner, or EU if any partner is EU?
- Which centrality measures, and why (in-degree, PageRank, betweenness?).
- Which sensitivity check (drop the 174 outside sources? change uncertain tags?).
