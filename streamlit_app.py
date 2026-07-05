from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from app import run_scientific_agent


st.set_page_config(
    page_title="Scientific Search Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 750;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 1.05rem;
    color: var(--text-color);
    opacity: 0.75;
    margin-bottom: 1.5rem;
}

.paper-card {
    padding: 1rem;
    border-radius: 1rem;
    border: 1px solid rgba(128, 128, 128, 0.25);
    background: rgba(128, 128, 128, 0.08);
    margin-bottom: 0.8rem;
}

.paper-title {
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-color);
}

.paper-text {
    color: var(--text-color);
}

.small-muted {
    color: var(--text-color);
    opacity: 0.7;
    font-size: 0.9rem;
}

.score-high {
    color: #10b981;
    font-weight: 700;
}

.score-mid {
    color: #f59e0b;
    font-weight: 700;
}

.score-low {
    color: #ef4444;
    font-weight: 700;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def score_class(score: int) -> str:
    if score >= 75:
        return "score-high"
    if score >= 50:
        return "score-mid"
    return "score-low"


def safe_get(data: Dict[str, Any], key: str, default: Any = "") -> Any:
    value = data.get(key, default)
    return default if value is None else value


def paper_table(papers: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for index, paper in enumerate(papers, start=1):
        rows.append({
            "Rank": index,
            "Final Score": safe_get(paper, "final_score", 0),
            "Relevance": safe_get(paper, "relevance_score", 0),
            "Quality": safe_get(paper, "quality_score", 0),
            "Recency": safe_get(paper, "recency_score", 0),
            "Year": safe_get(paper, "year", ""),
            "Title": safe_get(paper, "title", ""),
            "Source": safe_get(paper, "source", ""),
            "Tool": safe_get(paper, "tool", ""),
            "URL": safe_get(paper, "url", ""),
        })
    return pd.DataFrame(rows)


def render_paper_cards(papers: List[Dict[str, Any]]) -> None:
    for index, paper in enumerate(papers, start=1):
        score = int(safe_get(paper, "final_score", 0) or 0)
        title = safe_get(paper, "title", "Untitled")
        year = safe_get(paper, "year", "n/a")
        source = safe_get(paper, "source", "Unknown source")
        url = safe_get(paper, "url", "")
        reason = safe_get(paper, "ranking_reason", "")
        abstract = safe_get(paper, "abstract", "")

        st.markdown(
            f"""
            <div class="paper-card">
                <div class="paper-title">{index}. {title}</div>
                <div class="small-muted">{year} · {source}</div>
                <div class="paper-text">
                    Final score: <span class="{score_class(score)}">{score}/100</span>
                </div>
                <div class="small-muted">
                    Relevance {safe_get(paper, "relevance_score", 0)} ·
                    Quality {safe_get(paper, "quality_score", 0)} ·
                    Recency {safe_get(paper, "recency_score", 0)}
                </div>
                <div class="paper-text" style="margin-top:0.5rem;">{reason}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if url:
            st.link_button("Open paper source", url)

        with st.expander("Show abstract and metadata"):
            if abstract:
                st.write(abstract)
            else:
                st.info("No abstract available.")            
            st.json(paper)


with st.sidebar:
    st.title("🔬 Scientific Agent")    

    st.markdown("### What this app does")
    st.write(
        "It checks whether your question is scientific, searches scholarly databases, "
        "ranks papers, selects the strongest sources, and generates an evaluated answer."
    )

    st.markdown("### Example questions")
    examples = [
        "How can I use Google Gemini in my scientific search project?",
        "What does the literature say about digital detox and well-being?",
        "Which theories explain the impact of fake reviews on consumer trust?",
        "What are suitable methods for evaluating a multi-agent research assistant?",
    ]

    selected_example = st.selectbox("Choose an example", [""] + examples)

    st.markdown("### Settings")
    show_raw_json = st.toggle("Show raw JSON", value=False)
    show_all_ranked = st.toggle("Show all ranked paper cards", value=True)


st.markdown('<div class="main-title">Scientific Search Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ask an academic question. The agent will search, rank, select, answer, and evaluate.</div>',
    unsafe_allow_html=True,
)

query = st.text_area(
    "Your scientific question",
    value=selected_example if selected_example else "",
    height=110,
    placeholder="Example: How can I use Google Gemini in my scientific search project?",
)

col_run, col_clear = st.columns([1, 5])
run_clicked = col_run.button("Run agent", type="primary", use_container_width=True)
clear_clicked = col_clear.button("Clear result", use_container_width=False)

if clear_clicked:
    st.session_state.pop("result", None)
    st.rerun()

if run_clicked:
    if not query.strip():
        st.warning("Please enter a scientific question.")
    else:
        with st.status("Running multi-agent workflow...", expanded=True) as status:
            st.write("Checking scientific relevance...")
            st.write("Creating academic search queries...")
            st.write("Searching scientific databases...")
            st.write("Ranking and selecting papers...")
            st.write("Generating and evaluating answer...")
            try:
                st.session_state["result"] = run_scientific_agent(query.strip())
                status.update(label="Workflow finished", state="complete", expanded=False)
            except Exception as exc:
                status.update(label="Workflow failed", state="error", expanded=True)
                st.error(str(exc))

result = st.session_state.get("result")

if result:
    if result.get("status") == "not_scientific":
        st.error("This question was classified as not scientific.")
        st.write(result.get("reason", "No reason provided."))
        st.stop()

    st.success("Scientific question accepted.")

    top_cols = st.columns([2, 1, 1, 1])
    top_cols[0].markdown("#### Research domain")
    top_cols[0].markdown(f"### {result.get('research_domain', 'Unknown')}")
    top_cols[1].metric("Ranked papers", len(result.get("ranked_papers", [])))
    top_cols[2].metric("Selected papers", len(result.get("selected_papers", [])))
    top_cols[3].metric("Evaluation", "Passed" if result.get("evaluation_passed") else "Needs revision")

    tabs = st.tabs([
        "Answer",
        "Ranked papers",
        "Selected papers",
        "Search queries",
        "Evaluation",
        "Raw JSON",
    ])

    with tabs[0]:
        st.markdown("## Final answer")
        st.markdown(result.get("answer", ""))

    with tabs[1]:
        st.markdown("## Ranked papers")
        ranked = result.get("ranked_papers", [])
        if ranked:
            df = paper_table(ranked)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "URL": st.column_config.LinkColumn("URL"),
                    "Final Score": st.column_config.ProgressColumn("Final Score", min_value=0, max_value=100),
                    "Relevance": st.column_config.ProgressColumn("Relevance", min_value=0, max_value=100),
                    "Quality": st.column_config.ProgressColumn("Quality", min_value=0, max_value=100),
                    "Recency": st.column_config.ProgressColumn("Recency", min_value=0, max_value=100),
                },
            )
            if show_all_ranked:
                render_paper_cards(ranked)
        else:
            st.info("No ranked papers returned.")

    with tabs[2]:
        st.markdown("## Selected papers used for the answer")
        selected = result.get("selected_papers", [])
        if selected:
            render_paper_cards(selected)
        else:
            st.warning("No selected papers were returned.")

    with tabs[3]:
        st.markdown("## Search queries")
        for item in result.get("search_queries", []):
            st.code(item, language="text")

    with tabs[4]:
        st.markdown("## Answer evaluation")
        if result.get("evaluation_passed"):
            st.success("Evaluation passed.")
        else:
            st.warning("Evaluation did not pass.")
        st.write(result.get("evaluation_feedback", ""))

    with tabs[5]:
        if show_raw_json:
            st.json(result)
        else:
            st.info("Enable 'Show raw JSON' in the sidebar to inspect the complete state.")
else:
    st.info("Enter a scientific question and click **Run agent**.")
