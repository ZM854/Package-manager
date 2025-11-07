import argparse
import sys
from urllib.parse import urlparse
from pathlib import Path


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
        description="Dependency graph visualizer configuration prototype"
    )

    parser.add_argument(
        "-p", "--package",
        required=True,
        help="Name of the analyzed package."
    )
    parser.add_argument(
        "-r", "--repo",
        required=True,
        help="URL of repository (remote) or path to test repo file (test)."
    )
    parser.add_argument(
        "-m", "--mode",
        required=True,
        choices=["remote", "test"],
        help="Working mode: 'remote' or 'test'."
    )
    parser.add_argument(
        "-f", "--filter",
        default="",
        help="Substring to filter packages (optional)."
    )

    args = parser.parse_args()

    try:
        args.repo = validate_repo(args.repo, args.mode)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    return args


def main():
    args = parse_args()

    config = {
        "package": args.package,
        "repo": args.repo,
        "mode": args.mode,
        "filter": args.filter
    }

    for key, value in config.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()


