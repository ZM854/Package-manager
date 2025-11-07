import argparse
import sys
from urllib.parse import urlparse
from urllib.request import urlopen
from pathlib import Path
import json


def validate_repo(repo: str, mode: str) -> str:
    if mode == "remote":
        parsed = urlparse(repo)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError("Invalid repository URL in remote mode.")
    elif mode == "test":
        path = Path(repo)
        if not path.exists() or not path.is_file():
            raise ValueError("Invalid repository file path in test mode.")
    return repo


def parse_args():
    parser = argparse.ArgumentParser(
        description="Dependency graph visualizer - Stage 2: Data collection (NuGet API)"
    )

    parser.add_argument("-p", "--package", required=True, help="Name of the analyzed package.")
    parser.add_argument("-r", "--repo", required=True, help="Repository URL or test repo file.")
    parser.add_argument("-m", "--mode", required=True, choices=["remote", "test"], help="Mode: remote or test.")
    parser.add_argument("-f", "--filter", default="", help="Substring to filter packages (optional).")

    args = parser.parse_args()

    try:
        args.repo = validate_repo(args.repo, args.mode)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    return args


def fetch_json(url: str):
    try:
        with urlopen(url) as response:
            data = json.load(response)
        return data
    except Exception as e:
        print(f"Error fetching JSON from {url}: {e}", file=sys.stderr)
        sys.exit(1)


def get_registration_url(base_url: str) -> str:
    data = fetch_json(base_url)
    for resource in data.get("resources", []):
        if "RegistrationsBaseUrl" in resource.get("@type", "") or "RegistrationBaseUrl" in resource.get("@type", ""):
            return resource["@id"]
    print("Error: RegistrationBaseUrl not found in index.json", file=sys.stderr)
    sys.exit(1)




def get_dependencies_remote(package_name: str, repo_url: str):
    print(f"Connecting to NuGet repository: {repo_url}")
    registration_base = get_registration_url(repo_url)

    package_id = package_name.lower()
    if not registration_base.endswith("/"):
        registration_base += "/"

    package_url = f"{registration_base}{package_id}/index.json"
    print(f"Fetching package data: {package_url}")

    data = fetch_json(package_url)

    if data.get("items") and data["items"][0].get("items"):
        entries = data["items"][0]["items"]
    else:
        page_url = data["items"][0].get("@id")
        if not page_url:
            print("Error: No dependency data found.", file=sys.stderr)
            sys.exit(1)
        print(f"Fetching page data: {page_url}")
        page_data = fetch_json(page_url)
        entries = page_data.get("items", [])

    if not entries:
        print(f"No dependency data found for package '{package_name}'.")
        return []

    latest_entry = entries[-1]
    catalog_entry = latest_entry.get("catalogEntry", {})
    deps = catalog_entry.get("dependencyGroups", [])

    dependencies = []
    for group in deps:
        for dep in group.get("dependencies", []):
            dep_id = dep.get("id")
            if dep_id:
                dependencies.append(dep_id)

    return dependencies


def main():
    args = parse_args()

    print(f"Analyzing package: {args.package}")
    print(f"Mode: {args.mode}")
    print(f"Repository: {args.repo}")
    print("-" * 40)

    deps = get_dependencies_remote(args.package, args.repo)

    if deps:
        print("Direct dependencies:")
        for dep in deps:
            print(f"- {dep}")
    else:
        print("No direct dependencies found.")


if __name__ == "__main__":
    main()
