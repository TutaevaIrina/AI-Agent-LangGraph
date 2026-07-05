"""
Creates a visualization of the LangGraph workflow.

Usage:

python visualize_graph.py
"""

from pathlib import Path

from graph.builder import build_graph


def main():

    app = build_graph()

    output_dir = Path("images")
    output_dir.mkdir(exist_ok=True)

    png_path = output_dir / "langgraph_workflow.png"

    graph = app.get_graph()

    png = graph.draw_mermaid_png()

    png_path.write_bytes(png)

    print()
    print("=" * 50)
    print("LangGraph visualization created successfully.")
    print(f"Saved to: {png_path.resolve()}")
    print("=" * 50)


if __name__ == "__main__":
    main()