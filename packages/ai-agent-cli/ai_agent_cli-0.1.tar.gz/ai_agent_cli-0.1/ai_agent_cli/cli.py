import argparse
from my_cli_tool.ai_agent import setup_and_run_backend

def main():
    parser = argparse.ArgumentParser(description="AI Agent for Backend Creation")
    parser.add_argument("project_name", type=str, help="Name of the project")
    parser.add_argument("--github_token", type=str, help="GitHub token to push the repo")
    args = parser.parse_args()

    setup_and_run_backend(args.project_name, args.github_token)

