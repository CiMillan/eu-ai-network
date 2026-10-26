"""Applied Network Analysis 2026/27, group project proposal: who Europe's AI builds on, and who builds on Europe.

Run from the repo root:  streamlit run app/streamlit_app.py
Reads the frozen export in app/data/ (release eu-angle-v1), never the upstream YAML.
Sources: Bommasani et al. 2021 (foundation models) and Bommasani et al. 2024 (Ecosystem Graphs), linked in the sidebar.
"""
import collections
import csv
import json
import math
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).resolve().parent / "data"
DOCS = Path(__file__).resolve().parent / "docs"
UPSTREAM = "https://github.com/stanford-crfm/ecosystem-graphs"
FM_PAPER = "https://arxiv.org/abs/2108.07258"
EG_PAPER = "https://arxiv.org/abs/2303.15772"
STANFORD_PAGE = "https://crfm.stanford.edu/ecosystem-graphs/"
OUR_REPO = "https://github.com/CiMillan/eu-ai-network"
OUR_APP = "https://eu-ai-network.streamlit.app/"
MOODLE = "https://elearning.novaims.unl.pt/course/view.php?id=4859"

# Three categorical slots (network = all pairs in play, so at most three hues); outside sources stay neutral grey
COLOR = {"model": "#3987e5", "dataset": "#d95926", "application": "#199e70", "external": "#8a8984"}
LABEL = {"model": "Model", "dataset": "Dataset", "application": "App", "external": "Outside source"}


@st.cache_data
def load():
    nodes = list(csv.DictReader(open(DATA / "nodes.csv", encoding="utf-8")))
    edges = list(csv.DictReader(open(DATA / "edges.csv", encoding="utf-8")))
    manifest = json.loads((DATA / "manifest.json").read_text())
    return nodes, edges, manifest


@st.cache_data
def layout(_graph):
    """Node positions for the map, fixed seed so the picture is the same for everyone."""
    return nx.spring_layout(_graph.to_undirected(), seed=7, k=0.06, iterations=300)


def network_figure(graph, pos, label_top=6, height=560):
    """
    The whole map: one dot per node, coloured by type, sized by how many nodes are built on it.
    Grey lines are the links. The biggest hubs get their names written next to them.
    """
    fig = go.Figure()
    xs, ys = [], []
    for u, v in graph.edges:
        xs += [pos[u][0], pos[v][0], None]
        ys += [pos[u][1], pos[v][1], None]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(width=0.5, color="rgba(138,137,132,0.35)"),
                             hoverinfo="skip", showlegend=False))
    for kind in COLOR:
        ns = [n for n in graph if graph.nodes[n]["type"] == kind]
        fig.add_trace(go.Scatter(
            x=[pos[n][0] for n in ns], y=[pos[n][1] for n in ns], mode="markers", name=LABEL[kind],
            marker=dict(size=[5 + 2.2 * graph.out_degree(n) ** 0.8 for n in ns], color=COLOR[kind],
                        line=dict(width=1, color="rgba(14,17,23,0.9)")),
            customdata=[[graph.nodes[n]["organization"] or "—", graph.out_degree(n)] for n in ns],
            text=ns, hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>built on it: %{customdata[1]}<extra></extra>"))
    # Hubs sit close together in the middle, so each name goes out on its own short line, spread around a circle
    for i, (n, _) in enumerate(sorted(graph.out_degree, key=lambda t: -t[1])[:label_top]):
        angle = 2 * math.pi * (i + 0.5) / label_top
        fig.add_annotation(x=pos[n][0], y=pos[n][1], text=n, showarrow=True, arrowhead=0, arrowwidth=1,
                           arrowcolor="#c3c2b7", ax=75 * math.cos(angle), ay=-55 * math.sin(angle),
                           font=dict(size=12), bgcolor="rgba(14,17,23,0.75)")
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=10, b=0), legend=dict(orientation="h", y=1.04),
                      xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"))
    return fig


def flow_figure(columns, kinds=None, links=None, height=300):
    """
    A small left-to-right picture: each column is a list of boxes. links lists the arrows as (from, to); without
    it, every box points to every box in the next column. kinds maps a box to a node type for its colour; boxes
    without a type are drawn neutral.
    """
    kinds = kinds or {}
    links = links or [(a, b) for c in range(len(columns) - 1) for a in columns[c] for b in columns[c + 1]]
    fig = go.Figure()
    pos = {}
    for c, col in enumerate(columns):
        for r, name in enumerate(col):
            pos[name] = (c, (len(col) - 1) / 2 - r)
    for a, b in links:
        fig.add_annotation(x=pos[b][0] - 0.12, y=pos[b][1], ax=pos[a][0] + 0.12, ay=pos[a][1],
                           xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2,
                           arrowwidth=1.5, arrowcolor="#8a8984", text="")
    # A tall last column has no room for names under its boxes, so they go to the right instead
    crowded = len(columns[-1]) if len(columns[-1]) > 4 else 0

    def side(n):
        return "middle right" if crowded and pos[n][0] == len(columns) - 1 else "bottom center"

    for kind in list(COLOR) + [None]:
        ns = [n for n in pos if kinds.get(n) == kind]
        if not ns:
            continue
        fig.add_trace(go.Scatter(
            x=[pos[n][0] for n in ns], y=[pos[n][1] for n in ns], mode="markers+text", text=ns,
            textposition=[side(n) for n in ns], name=LABEL.get(kind, ""), showlegend=kind is not None,
            marker=dict(size=22 if crowded == 0 else 14, color=COLOR.get(kind, "#c3c2b7"), line=dict(width=2, color="rgba(14,17,23,0.9)")),
            hoverinfo="text"))
    rows = max(len(col) for col in columns)
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), legend=dict(orientation="h", y=1.15),
                      xaxis=dict(visible=False, range=[-0.5, len(columns) - 0.5 + (0.6 if crowded else 0)]),
                      yaxis=dict(visible=False, range=[-rows / 2 - 0.3, rows / 2 + 0.1]))
    return fig


def bar_figure(labels, values, colors, height=360, horizontal=True):
    """Plain bars, thin and rounded, one colour per bar."""
    bar = go.Bar(x=values if horizontal else labels, y=labels if horizontal else values,
                 orientation="h" if horizontal else "v", marker=dict(color=colors, cornerradius=4),
                 hovertemplate="%{y}: %{x}<extra></extra>" if horizontal else "%{x}: %{y}<extra></extra>")
    fig = go.Figure(bar)
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=10, b=0), bargap=0.35)
    if horizontal:
        fig.update_yaxes(autorange="reversed")
    return fig


nodes, edges, manifest = load()
by_name = {n["name"]: n for n in nodes}
assets = [n for n in nodes if n["type"] != "external"]
orgs = {n["organization"] for n in assets if n["organization"]}
graph = nx.DiGraph()
graph.add_nodes_from((n["name"], n) for n in nodes)
graph.add_edges_from((e["upstream"], e["downstream"]) for e in edges)

st.set_page_config(page_title="Europe in the AI network", layout="centered")
st.title("Europe in the AI network")
st.caption("Applied Network Analysis 2026/27 · group project proposal · draft for the group")

STEPS = ["The project", "What is a foundation model?", "AI has a supply chain", "Stanford's map",
         "A few hubs hold it up", "Our question: Europe", "The plan", "References and links"]
i = st.sidebar.radio("Steps", range(len(STEPS)), format_func=lambda k: f"{k + 1} · {STEPS[k]}")
st.sidebar.caption(f"Sources: [Bommasani et al. 2021]({FM_PAPER}) · [Bommasani et al. 2024]({EG_PAPER}) · "
                   f"[data]({UPSTREAM})")

if i == 0:
    st.header("The project")
    st.markdown(
        "**Course:** Applied Network Analysis 2026/27, group project. It counts for **50%** of the final grade.  \n"
        "**Group F:** Ifeoluwa Adeboye, Sofiia Makhortova, Cintia Millan and Ella Tiihonen.  \n"
        "**Rule of the course:** find the article behind the dataset, replicate its analysis, then extend it. "
        f"Our article: Stanford's [Ecosystem Graphs paper]({EG_PAPER}); our extension: the Europe question.")
    st.subheader("Deadlines")
    st.dataframe(pd.DataFrame([
        {"when": "Mon 2 Nov 2026 (Lecture 5)", "what": "Proposal: 5 slides in at most 5 minutes"},
        {"when": "Every class from Mon 16 Nov 2026 (Lab 5)", "what": "60-second update per group: done, next, blocks"},
        {"when": "Sun 10 Jan 2027, 15:59", "what": "Send the slides as a PDF on Moodle (course template); no report"},
        {"when": "January 2027 (date to be set)", "what": "Final: 10-minute talk by one member, then Q&A for all"},
    ]), hide_index=True)
    st.caption(f"Dates from the course syllabus and [Moodle]({MOODLE}), where all the course details are. "
               "The syllabus may still change them.")
    st.subheader("What the proposal must show")
    st.dataframe(pd.DataFrame([
        {"the course asks": "Our network: nodes N and links L, with N > 100",
         "our answer": f"{graph.number_of_nodes()} nodes, {graph.number_of_edges()} links (steps 3 and 4)"},
        {"the course asks": "How we collect the data", "our answer": "Stanford's public records, frozen at one commit (step 4)"},
        {"the course asks": "Which questions we ask", "our answer": "Europe, both ways (step 6)"},
        {"the course asks": "Why we care", "our answer": "A few hubs hold up the rest (steps 2 and 5)"},
    ]), hide_index=True)
    st.subheader("How it is graded")
    st.dataframe(pd.DataFrame([
        {"criterion": "C1 Problem and research question", "weight": "10%"},
        {"criterion": "C2 Data and methods, with the descriptive network analysis", "weight": "20%"},
        {"criterion": "C3 Depth and correctness of the network analysis", "weight": "25%"},
        {"criterion": "C4 Insights and interpretation", "weight": "20%"},
        {"criterion": "C5 Clarity and compliance", "weight": "10%"},
        {"criterion": "C6 Presentation and Q&A", "weight": "15%"},
    ]), hide_index=True)
    st.download_button("Download the course's project description (PDF)", (DOCS / "project-description.pdf").read_bytes(),
                       file_name="project-description.pdf", mime="application/pdf")

elif i == 1:
    with st.container(border=True):
        st.subheader("The network we study")
        st.markdown(
            "We increasingly hand AI our questions, our choices and our trust: what to read, how to write, "
            "what to believe. Every answer comes out of a chain. **Datasets teach models, and models power the "
            "apps people use.** Stanford's *Ecosystem Graphs* write this chain down as a network of "
            f"{graph.number_of_nodes()} pieces and {graph.number_of_edges()} links.  \n"
            "As more of what people learn passes through AI, **this network becomes part of how knowledge "
            "travels**. When we trust an "
            "answer, we also trust everything behind it: the data it learned from and the models it was built "
            "on. But that chain is hidden from the person asking. **Knowing where the information we trust comes "
            "from** is why this network matters. What a few models learn, and what they miss, reaches everyone "
            "built on them. So we ask who sits at the centre, who depends on whom, and where Europe stands.")
    st.header("What is a foundation model?")
    st.markdown(
        "A **foundation model** is one large AI model trained on broad data, such as huge amounts of text or "
        "images from the web. Afterwards it can be **adapted to many different tasks**. "
        "Examples are GPT-3, BERT and CLIP.")
    apps = ["Chatbot", "Search", "Code helper", "Image tool"]
    st.plotly_chart(flow_figure([["Broad data"], ["Foundation model"], apps],
                                kinds={"Broad data": "dataset", "Foundation model": "model",
                                       **{a: "application" for a in apps}}), use_container_width=True)
    st.info("**Why the name?** Many things are built on one base. That is powerful, but any flaw in the base "
            "is inherited by everything built on it.")
    st.caption(f"Definition and the flaw point: Stanford, [Bommasani et al. 2021]({FM_PAPER}), "
               "*On the Opportunities and Risks of Foundation Models*.")

elif i == 2:
    st.header("AI has a supply chain")
    st.markdown(
        "Models are not built alone. **Datasets** feed **models**, and models feed **apps**. "
        "Stanford calls each piece an *asset* and each 'built on' a *dependency*.")
    st.markdown("A real example from the data: one dataset, two models, two apps.")
    st.plotly_chart(flow_figure(
        [["The Pile"], ["GPT-NeoX", "YaLM"], ["GooseAI API", "Yandex Search"]],
        kinds={"The Pile": "dataset", "GPT-NeoX": "model", "YaLM": "model",
               "GooseAI API": "application", "Yandex Search": "application"},
        links=[("The Pile", "GPT-NeoX"), ("The Pile", "YaLM"), ("GPT-NeoX", "GooseAI API"),
               ("YaLM", "Yandex Search")]), use_container_width=True)
    st.caption("Read the arrows as 'is used to build'.")
    st.info("**Why a network?** Once links are written down, we can ask network questions: who sits in the "
            "middle, who depends on whom, and what breaks if one piece goes away.")
    st.caption(f"Assets and dependencies: Stanford, [Bommasani et al. 2024]({EG_PAPER}), *Ecosystem Graphs*.")

elif i == 3:
    st.header("Stanford's map")
    st.markdown(
        f"Stanford researchers documented this supply chain in **Ecosystem Graphs** ([paper]({EG_PAPER}), "
        f"[data]({UPSTREAM})). The 2024 AI Index and the UK's Competition and Markets Authority both use it.")
    counts = collections.Counter(n["type"] for n in nodes)
    c = st.columns(4)
    c[0].metric("Models", counts["model"])
    c[1].metric("Datasets", counts["dataset"])
    c[2].metric("Apps", counts["application"])
    c[3].metric("Links", manifest["edges"])
    giant = graph.subgraph(max(nx.weakly_connected_components(graph), key=len))
    st.plotly_chart(network_figure(giant, layout(giant)), use_container_width=True)
    st.caption(f"Each dot is a node; bigger means more is built on it. Hover for names. Grey dots are outside "
               f"sources named as inputs, e.g. Common Crawl and Wikipedia. Shown: the biggest connected part, "
               f"{len(giant)} of {len(graph)} nodes; the rest are small islands or have no links. "
               f"Snapshot: commit `{manifest['upstream_commit']}`.")
    st.subheader("It grew fast")
    years = collections.Counter(n["created_date"][:4] for n in assets if n["created_date"][:4].isdigit())
    shown = [str(y) for y in range(2018, 2025)]
    st.plotly_chart(bar_figure(shown, [years[y] for y in shown], COLOR["model"], height=260, horizontal=False),
                    use_container_width=True)
    st.caption("New assets per year. The map stops in April 2024, so the last bar is incomplete.")

elif i == 4:
    st.header("A few hubs hold it up")
    st.markdown(
        "Most pieces are used by almost nobody. A few are used by many. Network science calls these **hubs**. "
        "Stanford points out that hubs show where power concentrates, and what to check for safety.")
    out = dict(graph.out_degree)
    bins = [("0", 0, 0), ("1", 1, 1), ("2", 2, 2), ("3–5", 3, 5), ("6–10", 6, 10), ("11+", 11, 10 ** 6)]
    st.plotly_chart(bar_figure([b[0] for b in bins], [sum(lo <= d <= hi for d in out.values()) for _, lo, hi in bins],
                               COLOR["external"], height=240, horizontal=False), use_container_width=True)
    st.caption("How many nodes are built on each node. Most have none or one; a handful have more than ten.")
    st.subheader("The top ten")
    top = sorted(out, key=lambda n: -out[n])[:10]
    st.plotly_chart(bar_figure(top, [out[n] for n in top], [COLOR[by_name[n]["type"]] for n in top]),
                    use_container_width=True)
    st.caption("Colour = type: blue model, orange dataset, green app, grey outside source.")
    st.subheader("Zoom on one hub")
    hub = st.selectbox("Hub", top, index=top.index("ChatGPT API"))
    up, down = list(graph.predecessors(hub)), list(graph.successors(hub))
    kinds = {n: by_name[n]["type"] for n in up + down + [hub]}
    st.plotly_chart(flow_figure([up, [hub], down] if up else [[hub], down], kinds=kinds,
                                height=max(300, 34 * len(down))), use_container_width=True)
    st.caption("Left: what it is built on. Right: what is built on it.")

elif i == 5:
    st.header("Our question: Europe")
    st.markdown(
        "We ask it **both ways**:\n"
        "- **Who does Europe build on?** When a European model is made, how much of what it uses comes from "
        "outside the EU?\n"
        "- **Who builds on Europe?** Which European datasets and models do others depend on?")
    st.info("**Why we care.** If a few non-EU hubs hold up most European AI, Europe depends on them. "
            "If European work holds up others, Europe has weight in the network.")
    st.subheader("First job: tag each organisation EU, US, China or other")
    st.markdown(
        f"The records list {len(orgs)} organisation names. Some are joint teams, like 'Zhipu AI, Tsinghua "
        "University', so this differs from the paper's 117. We tag each one with a source, such as its own page.")
    st.markdown("Upstream added a country field later, but a first look shows mistakes:")
    st.dataframe(pd.DataFrame([
        {"organisation": "01 AI (Yi, Yi-VL)", "upstream says": "France", "to check": "Chinese company"},
        {"organisation": "Mistral AI (9 assets)", "upstream says": "USA", "to check": "French company"},
    ]), hide_index=True)
    st.caption("Both still to be checked against each organisation's own pages.")

elif i == 6:
    st.header("The plan")
    st.dataframe(pd.DataFrame([
        {"course step": "Basic measures", "what we do": "N, L, density, degree distribution, clustering, paths"},
        {"course step": "Centrality", "what we do": "Which nodes hold up the most work, on each side"},
        {"course step": "Communities", "what we do": "Do European nodes form their own cluster or sit inside others?"},
        {"course step": "Robustness", "what we do": "Remove one side's nodes: how much of the other side breaks?"},
        {"course step": "Null model", "what we do": "Compare with random networks of the same size"},
        {"course step": "Time", "what we do": "2019 to April 2024: is dependence growing?"},
    ]), hide_index=True)
    st.success("**Your view?** Does the question make sense to you, and which side interests you most?")

else:
    st.header("References and links")
    st.subheader("Papers")
    st.markdown(
        f"- Bommasani, R. et al. (2021). *On the Opportunities and Risks of Foundation Models*. "
        f"[arXiv:2108.07258]({FM_PAPER})\n"
        f"- Bommasani, R. et al. (2024). *Ecosystem Graphs: Documenting the Foundation Model Supply Chain*. "
        f"AIES 2024, pp. 196–209. [arXiv:2303.15772]({EG_PAPER})")
    st.subheader("Stanford's Ecosystem Graphs")
    st.markdown(
        f"- Website: [{STANFORD_PAGE}]({STANFORD_PAGE})\n"
        f"- GitHub: [{UPSTREAM}]({UPSTREAM})\n"
        f"- The snapshot we use: commit [{manifest['upstream_commit']}]({UPSTREAM}/commit/{manifest['upstream_commit']})")
    st.subheader("Our work")
    st.markdown(
        f"- This app's code and data: [{OUR_REPO}]({OUR_REPO})\n"
        f"- This app online: [{OUR_APP}]({OUR_APP})\n"
        "- Built with Python: networkx, pandas, plotly and Streamlit")
    st.subheader("Course")
    st.markdown(f"- Course page on Moodle (all details and dates): [{MOODLE}]({MOODLE})")
    st.download_button("Download the course's project description (PDF)", (DOCS / "project-description.pdf").read_bytes(),
                       file_name="project-description.pdf", mime="application/pdf", key="pdf_refs")
