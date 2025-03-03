import argparse
import os
import os.path

from sarif_parser import run_sarif_parser

import sentry

sentry.initialize()


class CommunityAnalyzerArgs:
    analyzer: str


def get_issue_map(analyzer_name: str) -> str:
    """Returns the appropriate issue map filepath for the given analyzer."""
    analyzers_dir = os.path.join(os.path.dirname(__file__), "analyzers")
    return os.path.join(analyzers_dir, analyzer_name, "utils", "issue_map.json")


def main(argv: list[str] | None = None) -> None:
    """Runs the CLI."""
    toolbox_path = os.getenv("TOOLBOX_PATH", "/toolbox")
    output_path = os.path.join(toolbox_path, "analysis_results.json")
    artifacts_path = os.getenv("ARTIFACTS_PATH", "/artifacts")

    parser = argparse.ArgumentParser("sarif_parser")
    parser.add_argument(
        "--analyzer",
        help="Which community analyzer to run. Example: 'kube-linter'",
        required=True,
    )
    args = parser.parse_args(argv, namespace=CommunityAnalyzerArgs)

    analyzer_name = args.analyzer
    issue_map_path = get_issue_map(analyzer_name)
    run_sarif_parser(artifacts_path, output_path, issue_map_path)


if __name__ == "__main__":
    main()  # pragma: no cover
