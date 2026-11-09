# Plan: Europe in the AI network

Group F · Applied Network Analysis 2026/27 · final slides due **Sun 10 Jan 2027, 15:59** (PDF on Moodle, course [template](https://elearning.novaims.unl.pt/mod/resource/view.php?id=112978)).

## What the course asks ([Project Description](https://elearning.novaims.unl.pt/mod/resource/view.php?id=112567), rubric)

- **C2, 20%:** N, L, density, average degree, degree distribution (plot), clustering, average path length and diameter (largest component), connected components, how we handle direction.
- **C3, 25%:** at least two centrality measures; community detection with modularity, or robustness; a calibrated null model; a sensitivity check.
- **C4, 20%:** for every number: what we expected, the random reference, how it compares, what we learned.
- **C1, C5, C6:** research question, template and figures, a 10-minute talk by one member, Q&A for everyone.
- Lab 4 tip: two null models, the random twin (same N and L, `nx.gnm_random_graph`) and the configuration model (same degrees).

## Our four questions (from the proposal)

1. Who does Europe build on?
2. Who builds on Europe?
3. Which hubs hold it up? (centrality, then removing hubs)
4. How did it change, 2019 → 2024? (yearly snapshots vs a null model)

## Steps and dates

Each step says what to do, where the theory is (lecture and slide numbers) and which lab cells to copy. Lecture 3 and the classes after 9 Nov are not on Moodle yet; their slides and cells get added when they are posted.

| date | step |
|---|---|
| 9 – 22 Nov | Step 0, check region tags · Step 1, basics |
| 23 – 29 Nov | Step 2, null models · Step 3, Europe both ways |
| 30 Nov – 6 Dec | Step 4, centrality and communities · Step 5, robustness |
| 7 – 10 Dec | Step 6, time and sensitivity. **Thu 10 Dec: results and figures frozen** |
| 14 – 18 Dec | first slide draft (14 Dec), full draft (Fri 18 Dec) |
| 18 Dec – 3 Jan | rehearse; Q&A prep for everyone |
| **Sun 10 Jan, 15:59** | **slides PDF on Moodle**; 10-minute talk in January |

Weekly 60-second updates in class start on 16 Nov.

### Step 0: check region tags (9 – 22 Nov)

- **Do:** `data/regions.csv` has a first guess for every region. Check your 48 rows (column `checked_by`): fix the region if wrong, add the page that shows it. Start with the rows marked "unsure, please check".
- **Theory and code:** none.

### Step 1: basics, `01_basics` (16 – 22 Nov) · C2

- **Do:**
    1. Load `nodes.csv` and `edges.csv` as a directed graph; attach type and region to each node.
    2. N, L, density, average in- and out-degree.
    3. In- and out-degree distributions, log-log plot.
    4. Weak and strong components; size of the largest one; is it a DAG (no cycles)?
    5. Clustering, average path length and diameter on the largest weak component, treated as undirected. Say so in the slides: this is how we handle direction.
- **Theory:** [Lecture 2](https://elearning.novaims.unl.pt/mod/resource/view.php?id=112451): connectivity and largest component, slides 29–30; degree 38–40; degree distribution 41–46; density 47–48; paths, distance, average path length 49–53; diameter 54–56; clustering 58–65; fat tails and small worlds 68–70. Why these numbers: [Lecture 1](https://elearning.novaims.unl.pt/mod/resource/view.php?id=112972), slide 57.
- **Code:**
    - [Lab 1](https://elearning.novaims.unl.pt/mod/resource/view.php?id=114988): edge list, cells 21–23; isolated nodes, 25–26; node attributes and colour, 27–28.
    - [Lab 2](https://elearning.novaims.unl.pt/mod/resource/view.php?id=116045): `from_pandas_edgelist`, cell 10; attributes, 12; components, 14–15; degree distribution, 21; density, 23; clustering, 25; path length and diameter, 27. **Cell 31, `network_id_card(G, label, domain)`, gives the whole C2 row in one call.**
    - [Lab 3](https://elearning.novaims.unl.pt/mod/resource/view.php?id=116851): fat-tailed degree plot, cells 28–29; directed graphs, 72–73; weak vs strong components and bow-tie, 74–75; cycles and DAGs, 76–77.

### Step 2: null models, `02_null_models` (23 – 29 Nov) · C3, C4

- **Do:**
    1. Random twin: same N and L, `nx.gnm_random_graph`, 100 seeds.
    2. Configuration model: same degrees, 100 seeds.
    3. For each: clustering, path length, largest-component share, largest hub. Mean and spread over the seeds.
    4. One table: our network vs both twins.
- **Theory:** [Lecture 4](https://elearning.novaims.unl.pt/mod/resource/view.php?id=117686): the random model, slides 2–13; expected links and degree, 16–22; Poisson degrees and why real networks are not, 23–29; small world, 30–35; clustering, 36–37; real vs random summary, 38 and 50; birth of the giant component, 39–49; why randomise a network, 60–61; degree-preserving randomisation, 62–63; configuration model, 66; hubs and power laws, 72–100. [Lecture 5](https://elearning.novaims.unl.pt/mod/resource/view.php?id=118985): slide numbers to add.
- **Code:** [Lab 4](https://elearning.novaims.unl.pt/mod/resource/view.php?id=119336): `giant()`, cells 13–14; **random twin `fingerprint(G, n_sources=100, seed=0)`, 15–20**; `giant_share(G)`, 22–25; **`configuration_twin(G, seed=0)`, 44–46**; what each model keeps, 47; **null-model report table, 56–57**.

### Step 3: Europe both ways, `03_europe_both_ways` (23 – 29 Nov) · questions 1 and 2, C4

- **Do:**
    1. Count links by region pair: upstream region → downstream region.
    2. Question 1: EU's downstream nodes, which regions do they build on?
    3. Question 2: EU's upstream nodes, which regions build on them?
    4. Compare the counts with the configuration twin from Step 2.
- **Theory:** Lecture 2, assortativity, slide 66; Lecture 4, why randomise, slides 60–61.
- **Code:** Lab 2, assortativity, cell 29; Lab 1, colour by attribute, cells 27–28; Lab 4, configuration twin, cells 44–46.

### Step 4: centrality and communities, `04_centrality_communities` (30 Nov – 6 Dec) · question 3, C3

- **Do:**
    1. Two or more centralities (see open decisions); top 10 nodes and their regions.
    2. Communities with modularity; which regions sit in each.
- **Theory:** Lab 5 class (16 Nov), slides to add.
- **Code:** Lab 3, degree vs strength, cells 56–57; Lab 5 cells to add.

### Step 5: robustness, `05_robustness` (30 Nov – 6 Dec) · question 3, C3

- **Do:** remove the top hubs one by one, then random nodes; plot the largest-component share after each removal.
- **Theory:** Lecture 2, resilience, slide 73; Lecture 4, giant component, slides 39–49. Lab 6 class (30 Nov), slides to add.
- **Code:** Lab 4, `giant_share(G)`, cells 22–25; Lab 6 attack simulator, to add.

### Step 6: time and sensitivity, `06_time_and_sensitivity` (7 – 10 Dec) · question 4, C3, C4

- **Do:**
    1. Yearly snapshots 2019 → 2024 from `created_date`.
    2. For each: the Step 1 numbers and the Step 2 twins.
    3. Sensitivity check (see open decisions): rerun Steps 1–3 without it, see if the story holds.
- **Theory:** Lecture 2, shrinking diameter and densification, slides 71–72.
- **Code:** Lab 3, time slices, cells 80–81; Lab 2, `network_id_card`, cell 31; Lab 4, `fingerprint`, cells 15–20.

## Workstreams (one owner each)

| workstream | owner |
|---|---|
| Data and region tags | |
| Basics and null models | |
| Centrality and communities | |
| Robustness and time | |

Everyone checks 48 region tags in the first two weeks (Step 0).

## Open decisions

- Organisations listed together (e.g. "Avignon University, Nantes University"): how do we tag a collaboration? One region per partner, or EU if any partner is EU?
- Which centrality measures, and why (in-degree, PageRank, betweenness?).
- Which sensitivity check (drop the 174 outside sources? change uncertain tags?).
