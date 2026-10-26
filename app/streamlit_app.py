"""Applied Network Analysis 2027, group project proposal: who Europe's AI builds on, and who builds on Europe.

Run from the repo root:  streamlit run app/streamlit_app.py
Reads the frozen export in app/data/ (release eu-angle-v1), never the upstream YAML.
"""
import collections
import csv
import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent / "data"
UPSTREAM = "https://github.com/stanford-crfm/ecosystem-graphs"
PAPER = "https://scholar.google.com/scholar?q=%22Ecosystem+Graphs%22+Bommasani+2024"


@st.cache_data
def load():
    nodes = list(csv.DictReader(open(DATA / "nodes.csv", encoding="utf-8")))
    edges = list(csv.DictReader(open(DATA / "edges.csv", encoding="utf-8")))
    manifest = json.loads((DATA / "manifest.json").read_text())
    return nodes, edges, manifest


nodes, edges, manifest = load()
by_name = {n["name"]: n for n in nodes}
assets = [n for n in nodes if n["type"] != "external"]
orgs = {n["organization"] for n in assets if n["organization"]}

st.set_page_config(page_title="Europe in the AI network", layout="centered")
st.title("Europe in the AI network")
st.caption("Applied Network Analysis 2027 · group project proposal · draft for the group")

step = st.sidebar.radio("Steps", ["1 · The question", "2 · The network", "3 · Who holds it up",
                                  "4 · Next: region tags", "5 · The plan"])

if step.startswith("1"):
    st.header("The question")
    st.markdown(
        "Every AI model is built on other things: datasets, other models, teacher models. "
        "Together they form a network.\n\n"
        "We ask it **both ways**:\n"
        "- **Who does Europe build on?** When a European model is made, how much of what it uses "
        "comes from outside the EU?\n"
        "- **Who builds on Europe?** Which European datasets and models do others depend on?")
    st.info("**Why we care.** If a few non-EU models hold up most European AI, Europe depends on them. "
            "If European work holds up others, Europe has weight in the network. The network shows which.")

elif step.startswith("2"):
    st.header("The network")
    st.markdown(
        f"- **Nodes:** AI models, datasets and apps. **Links:** one is built on another, "
        f"e.g. a model trained on a dataset (arrow from the dataset to the model).\n"
        f"- **Source:** Stanford's Ecosystem Graphs ([repo]({UPSTREAM}), [paper]({PAPER})), "
        f"frozen at commit `{manifest['upstream_commit']}`, cleaned in our earlier labs.")
    counts = collections.Counter(n["type"] for n in nodes)
    c = st.columns(4)
    c[0].metric("Nodes (N)", manifest["nodes"])
    c[1].metric("Links (L)", manifest["edges"])
    c[2].metric("Organisations", len(orgs))
    c[3].metric("Models", counts["model"])
    st.markdown(f"The {manifest['nodes']} nodes are {counts['model']} models, {counts['dataset']} datasets, "
                f"{counts['application']} apps, and {counts['external']} outside sources named as "
                f"dependencies (e.g. Common Crawl, Wikipedia).")
    st.subheader("Where we start: one record")
    st.dataframe(pd.DataFrame([by_name["GPT-4"]]), hide_index=True)
    st.dataframe(pd.DataFrame([e for e in edges if e["upstream"] == "LAION-5B"][:3]), hide_index=True)

elif step.startswith("3"):
    st.header("Who holds the network up today")
    st.markdown("The nodes with the most direct dependents: how many other nodes are built on each one.")
    out = collections.Counter(e["upstream"] for e in edges)
    top = [{"node": k, "type": by_name[k]["type"], "organisation": by_name[k]["organization"] or "—",
            "built on it": v} for k, v in out.most_common(10)]
    st.dataframe(pd.DataFrame(top), hide_index=True)
    st.info("Next we colour this table by region. That shows at a glance which side each hub sits on.")

elif step.startswith("4"):
    st.header("Next: region tags")
    st.markdown(
        f"We tag each of the {len(orgs)} organisations with where it is based: **EU, US, China or other**, "
        "each with a source (the organisation's own page or registry).")
    st.subheader("Why we tag them ourselves")
    st.markdown(
        "Upstream added a country field only in its last commit, after the version we use. "
        "A first look shows mistakes, so we can't take it as it is:")
    st.dataframe(pd.DataFrame([
        {"organisation": "01 AI (Yi, Yi-VL)", "upstream says": "France", "to check": "Chinese company"},
        {"organisation": "Mistral AI (9 assets)", "upstream says": "USA", "to check": "French company"},
    ]), hide_index=True)
    st.caption("Both still to be checked against each organisation's own pages.")

else:
    st.header("The plan")
    st.dataframe(pd.DataFrame([
        {"course step": "Basic measures", "what we do": "N, L, density, degree distribution, clustering, paths"},
        {"course step": "Centrality", "what we do": "Which nodes hold up the most work, on each side"},
        {"course step": "Communities", "what we do": "Do European nodes form their own cluster or sit inside others?"},
        {"course step": "Robustness", "what we do": "Remove one side's nodes: how much of the other side breaks?"},
        {"course step": "Null model", "what we do": "Compare with random networks of the same size"},
        {"course step": "Time", "what we do": "2019 to the newest dates: is dependence growing?"},
    ]), hide_index=True)
    st.success("**Your view?** Does the question make sense to you, and which side interests you most?")
