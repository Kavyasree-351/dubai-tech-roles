"""CLI application entry point for dubai-tech-roles.

Handles job fetching from ATS APIs and README / INTERNSHIPS markdown generation.
"""

import argparse
import logging
import sys
from typing import Any, Dict, List

from src.builder import build_readme, deduplicate_and_sort, load_listings, save_listings
from src.fetchers import fetch_all_internships, fetch_all_jobs

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
    build: bool = True,
    data_path: str = "data/listings.json",
    template_path: str = "templates/README.template.md",
    output_path: str = "README.md",
    fetch_internships_flag: bool = False,
    build_internships_flag: bool = False,
    internships_data_path: str = "data/internships.json",
    internships_template_path: str = "templates/INTERNSHIPS.template.md",
    internships_output_path: str = "INTERNSHIPS.md",
) -> int:
    """Execute the pipeline steps based on provided options."""
    # 1. Main UAE Tech Roles Pipeline
    if fetch or build:
        existing_jobs = load_listings(data_path)
        logger.info("Loaded %d existing job listings from %s", len(existing_jobs), data_path)

        if fetch:
            logger.info("Initiating ATS job fetchers for experienced tech roles...")
            fetched_jobs = fetch_all_jobs()
            logger.info("Fetched %d relevant jobs from configured endpoints", len(fetched_jobs))
            merged_jobs = merge_listings(existing_jobs, fetched_jobs)
            save_listings(merged_jobs, data_path)
            logger.info("Updated %s with total %d listings", data_path, len(merged_jobs))

        if build:
            logger.info("Compiling README at %s...", output_path)
            build_readme(template_path=template_path, data_path=data_path, output_path=output_path)

    # 2. Tech Internships & Early Graduate Pipeline
    if fetch_internships_flag or build_internships_flag:
        existing_internships = load_listings(internships_data_path)
        logger.info(
            "Loaded %d existing internships from %s",
            len(existing_internships),
            internships_data_path,
        )

        if fetch_internships_flag:
            logger.info("Initiating ATS job fetchers for tech internships & early graduates...")
            fetched_internships = fetch_all_internships()
            logger.info(
                "Fetched %d relevant internships from configured endpoints",
                len(fetched_internships),
            )
            merged_internships = merge_listings(existing_internships, fetched_internships)
            save_listings(merged_internships, internships_data_path)
            logger.info(
                "Updated %s with total %d listings",
                internships_data_path,
                len(merged_internships),
            )

        if build_internships_flag:
            logger.info("Compiling INTERNSHIPS.md at %s...", internships_output_path)
            build_readme(
                template_path=internships_template_path,
                data_path=internships_data_path,
                output_path=internships_output_path,
            )

    logger.info("Pipeline execution completed successfully.")
    return 0


def main() -> None:
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="dubai-tech-roles: ATS Scraper, README and Internships Table Generator"
    )
    # Main pipeline arguments
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Poll configured ATS endpoints and merge general tech role updates.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Compile README.md from data/listings.json.",
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

    # Internship pipeline arguments
    parser.add_argument(
        "--fetch-internships",
        action="store_true",
        help="Poll configured ATS endpoints specifically for early career and internship roles.",
    )
    parser.add_argument(
        "--build-internships",
        action="store_true",
        help="Compile INTERNSHIPS.md from data/internships.json.",
    )
    parser.add_argument(
        "--internships",
        action="store_true",
        help="Shortcut to build INTERNSHIPS.md.",
    )
    parser.add_argument(
        "--internships-data",
        type=str,
        default="data/internships.json",
        help="Path to internships JSON file (default: data/internships.json).",
    )
    parser.add_argument(
        "--internships-template",
        type=str,
        default="templates/INTERNSHIPS.template.md",
        help="Path to internships template file (default: templates/INTERNSHIPS.template.md).",
    )
    parser.add_argument(
        "--internships-output",
        type=str,
        default="INTERNSHIPS.md",
        help="Path to internships markdown output (default: INTERNSHIPS.md).",
    )

    # Master switch
    parser.add_argument(
        "--all",
        action="store_true",
        help="Execute both main tech roles and internships pipelines (fetch and compile both).",
    )

    args = parser.parse_args()

    # Determine actions based on flags
    if args.all:
        fetch_main = True
        build_main = True
        fetch_intern = True
        build_intern = True
    elif args.fetch_internships or args.build_internships or args.internships:
        fetch_main = args.fetch
        build_main = args.build
        fetch_intern = args.fetch_internships
        build_intern = args.build_internships or args.internships or args.fetch_internships
    else:
        # Default behavior: build main and build internships
        fetch_main = args.fetch
        build_main = True
        fetch_intern = False
        build_intern = True

    try:
        exit_code = run_pipeline(
            fetch=fetch_main,
            build=build_main,
            data_path=args.data,
            template_path=args.template,
            output_path=args.output,
            fetch_internships_flag=fetch_intern,
            build_internships_flag=build_intern,
            internships_data_path=args.internships_data,
            internships_template_path=args.internships_template,
            internships_output_path=args.internships_output,
        )
        sys.exit(exit_code)
    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

