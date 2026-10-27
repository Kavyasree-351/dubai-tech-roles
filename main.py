"""CLI application entry point for dubai-tech-roles.

Handles job fetching from ATS APIs and README generation.
"""

import argparse
import logging
import sys
from typing import Any, Dict, List

from src.builder import build_readme, load_listings, save_listings, deduplicate_and_sort
from src.fetchers import fetch_all_jobs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("dubai-tech-roles")


def merge_listings(
    existing_jobs: List[Dict[str, Any]], new_jobs: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Merge existing jobs with newly fetched jobs without overriding manual listings."""
    job_map: Dict[str, Dict[str, Any]] = {}

    # Load existing jobs first
    for job in existing_jobs:
        jid = job.get("job_id")
        if jid:
            job_map[jid] = job

    # Insert or update with newly fetched jobs
    for job in new_jobs:
        jid = job.get("job_id")
        if not jid:
            continue
        # If job already exists and is manual, preserve manual metadata
        if jid in job_map and job_map[jid].get("source") == "manual":
            continue
        job_map[jid] = job

    merged = list(job_map.values())
    return deduplicate_and_sort(merged)


def run_pipeline(
    fetch: bool = False,
    data_path: str = "data/listings.json",
    template_path: str = "templates/README.template.md",
    output_path: str = "README.md",
) -> int:
    """Execute the pipeline steps based on provided options."""
    existing_jobs = load_listings(data_path)
    logger.info("Loaded %d existing job listings from %s", len(existing_jobs), data_path)

    if fetch:
        logger.info("Initiating ATS job fetchers...")
        fetched_jobs = fetch_all_jobs()
        logger.info("Fetched %d relevant jobs from configured endpoints", len(fetched_jobs))
        merged_jobs = merge_listings(existing_jobs, fetched_jobs)
        save_listings(merged_jobs, data_path)
        logger.info("Updated %s with total %d listings", data_path, len(merged_jobs))

    logger.info("Compiling README at %s...", output_path)
    build_readme(template_path=template_path, data_path=data_path, output_path=output_path)
    logger.info("Pipeline execution completed successfully.")
    return 0


def main() -> None:
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="dubai-tech-roles: ATS Scraper and README Table Generator"
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Poll configured ATS endpoints (Greenhouse, Lever, SmartRecruiters) and merge updates.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Compile README.md from data/listings.json (default action).",
    )
    parser.add_argument(
        "--data",
        type=str,
        default="data/listings.json",
        help="Path to job listings JSON file (default: data/listings.json).",
    )
    parser.add_argument(
        "--template",
        type=str,
        default="templates/README.template.md",
        help="Path to README template file (default: templates/README.template.md).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="README.md",
        help="Path to output markdown file (default: README.md).",
    )

    args = parser.parse_args()

    # If neither flag is passed, default to building the README
    fetch_flag = args.fetch

    try:
        exit_code = run_pipeline(
            fetch=fetch_flag,
            data_path=args.data,
            template_path=args.template,
            output_path=args.output,
        )
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
