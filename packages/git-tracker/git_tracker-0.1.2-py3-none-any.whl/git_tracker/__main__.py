import os
import csv
import json
import subprocess
from datetime import datetime, timedelta
from collections import deque
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl
from typer import Typer, Argument
from enum import Enum
from git_tracker.core import aggregate_and_export_git_logs, Commit, Repo

app = Typer()


class OutputFormat(str, Enum):
    csv = "csv"
    json = "json"
    yaml = "yaml"
    md = "md"


@app.command()
def main(
    code_dir: str = Argument(
        default=os.path.join(os.path.expanduser("~"), "code"),
        help="Directory containing git repositories (default: ~/code)",
    ),
    output: str = Argument(
        default="git_aggregate_report",
        help="Output file name without extension (default: git_aggregate_report)",
    ),
    format: OutputFormat = Argument(
        default=OutputFormat.csv,
        help="Output format: csv, json, yaml, or md (default: csv)",
    ),
    since: Optional[str] = Argument(
        None, help="Start date for git log (format: YYYY-MM-DD)"
    ),
    until: Optional[str] = Argument(
        None, help="End date for git log (format: YYYY-MM-DD)"
    ),
):
    if not since:
        since = datetime.now().strftime("%Y-%m-01")
    if not until:
        until = datetime.now().strftime("%Y-%m-%d")
    since_date, until_date = since, until

    output_file = f"{output}.{format}"
    aggregate_and_export_git_logs(code_dir, output_file, format, since_date, until_date)
    print(f"Aggregated git logs have been written to {output_file}")


if __name__ == "__main__":
    app()
