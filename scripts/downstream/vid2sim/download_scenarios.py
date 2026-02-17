# Download vid2sim scenario assets from Google Drive.
#
# This script downloads the shared vid2sim scenario folder from Google Drive
# and saves it to a local target directory.
#
# Usage:
#   python download_scenarios.py --target_dir /path/to/save
#
# Dependencies:
#   pip install gdown
#
# Copyright (c) 2022-2025, The UrbanSim Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Download vid2sim scenario assets from Google Drive."""

from __future__ import annotations

import argparse
import os
import re
import sys

import gdown

SCENARIO_DRIVE_LINK = "https://drive.google.com/drive/folders/1RDe17eq6akLte-NoiOVWvV5deFg5a_Gh?usp=sharing"


def extract_folder_id(url: str) -> str:
    """Extract the Google Drive folder ID from a sharing URL.

    Args:
        url: Google Drive folder sharing URL.

    Returns:
        The folder ID string.

    Raises:
        ValueError: If the folder ID cannot be extracted from the URL.
    """
    match = re.search(r"folders/([a-zA-Z0-9_-]+)", url)
    if match is None:
        raise ValueError(f"Could not extract folder ID from URL: {url}")
    return match.group(1)


def download_folder(url: str, target_dir: str, *, quiet: bool = False) -> None:
    """Download a Google Drive folder to a local directory.

    Args:
        url: Google Drive folder sharing URL.
        target_dir: Local directory path to save the downloaded files.
        quiet: If True, suppress download progress output.
    """
    folder_id = extract_folder_id(url)
    os.makedirs(target_dir, exist_ok=True)

    print(f"Downloading scenario folder to: {target_dir}")
    print(f"Google Drive folder ID: {folder_id}")

    gdown.download_folder(id=folder_id, output=target_dir, quiet=quiet)

    print(f"Download complete. Files saved to: {target_dir}")


def main() -> None:
    """Parse arguments and run the download."""
    parser = argparse.ArgumentParser(description="Download vid2sim scenario assets from Google Drive.")
    parser.add_argument(
        "--target_dir",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "vid2sim", "scenarios"),
        help="Local directory to save the downloaded scenario files. "
        "Defaults to <repo_root>/data/vid2sim/scenarios.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=SCENARIO_DRIVE_LINK,
        help="Google Drive folder sharing URL. Defaults to the vid2sim scenario folder.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress download progress output.",
    )
    args = parser.parse_args()

    target_dir = os.path.abspath(args.target_dir)

    try:
        download_folder(args.url, target_dir, quiet=args.quiet)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
