import os
import csv
import json
import subprocess
from collections import deque
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Commit(BaseModel):
    commit_hash: str
    message: str
    files_changed: List[str]


class Repo(BaseModel):
    dirname: str
    remote_url: Optional[HttpUrl]
    branch: str
    commits: List[Commit]


def find_git_repos(root_dir):
    """
    Recursively find all git repositories under root_dir using BFS.
    """
    git_repos = []
    queue = deque([root_dir])

    while queue:
        current_dir = queue.popleft()
        git_dir = os.path.join(current_dir, ".git")
        if os.path.isdir(git_dir):
            git_repos.append(current_dir)
            continue  # Do not traverse subdirectories of a git repo
        try:
            with os.scandir(current_dir) as it:
                for entry in it:
                    if entry.is_dir() and not entry.name.startswith("."):
                        queue.append(os.path.join(current_dir, entry.name))
        except PermissionError:
            continue

    return git_repos


def get_remote_url(repo_path):
    try:
        remote_url = (
            subprocess.check_output(
                ["git", "-C", repo_path, "config", "--get", "remote.origin.url"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        remote_url = None

    return remote_url


def get_current_branch(repo_path):
    try:
        branch = (
            subprocess.check_output(
                ["git", "-C", repo_path, "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        branch = ""

    return branch


def get_git_info(repo_path, since_date, until_date):
    """
    Get commit logs from the git repository within the specified date range.
    """
    commits = []

    # Get commits within date range
    try:
        git_log = (
            subprocess.check_output(
                [
                    "git",
                    "-C",
                    repo_path,
                    "log",
                    f"--since={since_date}",
                    f"--until={until_date}",
                    "--pretty=format:%H|%s",
                ],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        git_log = ""

    if not git_log:
        return commits

    for line in git_log.split("\n"):
        if not line.strip():
            continue
        commit_hash, message = line.split("|", 1)

        # Get files changed in the commit
        try:
            files_output = (
                subprocess.check_output(
                    [
                        "git",
                        "-C",
                        repo_path,
                        "show",
                        "--name-status",
                        "--pretty=format:",
                        commit_hash,
                    ],
                    stderr=subprocess.DEVNULL,
                )
                .decode()
                .strip()
            )

        except subprocess.CalledProcessError:
            files_output = ""

        files_changed = []
        for file_line in files_output.split("\n"):
            if not file_line.strip():
                continue
            status, filepath = file_line.split("\t", 1)
            files_changed.append(f"{status}: {filepath}")

        commits.append(
            Commit(
                commit_hash=commit_hash, message=message, files_changed=files_changed
            )
        )

    return commits


def aggregate_git_logs(code_dir, since_date, until_date):
    """
    Aggregate git logs from all repositories under code_dir into a list of Repo instances.
    """
    git_repos = find_git_repos(code_dir)
    repos = []

    for repo in git_repos:
        commits = get_git_info(repo, since_date, until_date)
        if commits:
            repo_instance = Repo(
                dirname=os.path.basename(repo),
                remote_url=get_remote_url(repo),
                branch=get_current_branch(repo),
                commits=commits,
            )
            repos.append(repo_instance)

    return repos


def write_csv(output_file, repos):
    """
    Write the git commit logs to a CSV file.
    """
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "dirname",
            "remote_url",
            "branch",
            "commit_hash",
            "message",
            "files_changed",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for repo in repos:
            for commit in repo.commits:
                writer.writerow(
                    {
                        "dirname": repo.dirname,
                        "remote_url": repo.remote_url,
                        "branch": repo.branch,
                        "commit_hash": commit.commit_hash,
                        "message": commit.message,
                        "files_changed": ";".join(commit.files_changed),
                    }
                )


def write_json(output_file, repos):
    """
    Write the git commit logs to a JSON file.
    """
    import json

    with open(output_file, "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps([repo.dict() for repo in repos], indent=4))


def write_yaml(output_file, repos):
    """
    Write the git commit logs to a YAML file.
    """
    import yaml

    with open(output_file, "w", encoding="utf-8") as yamlfile:
        yaml.dump([repo.dict() for repo in repos], yamlfile, default_flow_style=False)


def write_markdown(output_file, repos):
    """
    Write the git commit logs to a Markdown file.
    """
    import markdown

    with open(output_file, "w", encoding="utf-8") as mdfile:
        mdfile.write("# Git Commit Log Report\n\n")
        for repo in repos:
            mdfile.write(f"## {repo.dirname} ({repo.branch})\n")
            mdfile.write(f"**Remote URL**: {repo.remote_url}\n")
            for commit in repo.commits:
                mdfile.write(f"### Commit {commit.commit_hash}\n")
                mdfile.write(f"**Message**: {commit.message}\n")
                mdfile.write(
                    f"**Files Changed**: {'; '.join(commit.files_changed)}\n\n"
                )


def aggregate_and_export_git_logs(
    code_dir, output_file, output_format, since_date, until_date
):
    """
    Aggregate git logs from all repositories and export in the desired format.
    """
    repos = aggregate_git_logs(code_dir, since_date, until_date)

    if output_format == "csv":
        write_csv(output_file, repos)
    elif output_format == "json":
        write_json(output_file, repos)
    elif output_format == "yaml":
        write_yaml(output_file, repos)
    elif output_format == "md":
        write_markdown(output_file, repos)
