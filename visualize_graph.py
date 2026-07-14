"""
Creates a visualization of the LangGraph workflow.

Usage:

python visualize_graph.py
"""

from pathlib import Path

from graph.builder import build_graph
from langchain_core.runnables.graph_mermaid import draw_mermaid_png


def main():

    app = build_graph()

    output_dir = Path("images")
    output_dir.mkdir(exist_ok=True)

    png_path = output_dir / "langgraph_workflow.png"

    graph = app.get_graph()

    mermaid_syntax = graph.draw_mermaid()
    mermaid_syntax = mermaid_syntax.replace("graph TD;", "graph LR;", 1)

    png = draw_mermaid_png(mermaid_syntax)

    png_path.write_bytes(png)

    print()
    print("=" * 50)
    print("LangGraph visualization created successfully.")
    print(f"Saved to: {png_path.resolve()}")
    print("=" * 50)


if __name__ == "__main__":
    main()