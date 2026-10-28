"""Markdown compilation script for dubai-tech-roles README."""

import datetime
import json
import logging
import os
from typing import Any, Dict, List, Optional

from src.filter import filter_expired_jobs

logger = logging.getLogger(__name__)


def load_listings(data_path: str) -> List[Dict[str, Any]]:
    """Load JSON job postings from the specified file path."""
    if not os.path.exists(data_path):
        logger.warning("Data file %s not found. Returning empty list.", data_path)
        return []

    with open(data_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            logger.error("Data file does not contain a JSON array.")
            return []
        except json.JSONDecodeError as e:
            logger.error("JSON decode error in %s: %s", data_path, e)
            return []


def save_listings(listings: List[Dict[str, Any]], data_path: str) -> None:
    """Save listings list into JSON file formatted with 2-space indentation."""
    os.makedirs(os.path.dirname(os.path.abspath(data_path)), exist_ok=True)
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)
        f.write("\n")


def deduplicate_and_sort(
    jobs: List[Dict[str, Any]],
    max_age_days: Optional[int] = None,
    reference_date: Optional[datetime.date] = None,
    keep_manual: bool = False,
) -> List[Dict[str, Any]]:
    """Deduplicate jobs by job_id, prune expired roles if max_age_days is set, and sort chronologically.

    If job_id is missing, falls back to combination of company + role + location.
    """
    seen_ids = set()
    unique_jobs: List[Dict[str, Any]] = []

    for job in jobs:
        jid = job.get("job_id")
        if not jid:
            # Fallback signature
            company = (job.get("company") or "").strip().lower()
            role = (job.get("role") or "").strip().lower()
            location = (job.get("location") or "").strip().lower()
            jid = f"{company}::{role}::{location}"

        if jid not in seen_ids:
            seen_ids.add(jid)
            unique_jobs.append(job)

    # Prune expired postings if retention cutoff is specified
    if max_age_days is not None and max_age_days > 0:
        unique_jobs = filter_expired_jobs(
            unique_jobs,
            max_age_days=max_age_days,
            reference_date=reference_date,
            keep_manual=keep_manual,
        )

    # Sort newest first (chronological descending)
    def sort_key(item: Dict[str, Any]) -> str:
        return item.get("date_posted") or "1970-01-01"

    unique_jobs.sort(key=sort_key, reverse=True)
    return unique_jobs


def _escape_cell(text: Optional[str]) -> str:
    """Escape pipe characters and line breaks for Markdown table cells."""
    if not text:
        return ""
    clean = str(text).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()
    return clean


def generate_markdown_table(
    jobs: List[Dict[str, Any]], include_category: bool = False
) -> str:
    """Generate Markdown rows corresponding to:

    | Company | Role | [Discipline |] Location | Apply Link | Date Posted |
    """
    if not jobs:
        if include_category:
            return "| *No active roles currently listed* | - | - | - | - | - |"
        return "| *No active roles currently listed* | - | - | - | - |"

    rows: List[str] = []
    for job in jobs:
        company = _escape_cell(job.get("company", "Unknown"))
        role = _escape_cell(job.get("role", "Open Position"))
        location = _escape_cell(job.get("location", "Dubai, UAE"))
        category = _escape_cell(job.get("category", "Software Engineering"))
        apply_url = str(job.get("apply_url") or "").strip()
        date_posted = _escape_cell(job.get("date_posted", "-"))

        if apply_url and (apply_url.startswith("http://") or apply_url.startswith("https://")):
            apply_link = f"[Apply ↗]({apply_url})"
        else:
            apply_link = "Apply"

        if include_category:
            row = f"| **{company}** | {role} | `{category}` | {location} | {apply_link} | {date_posted} |"
        else:
            row = f"| **{company}** | {role} | {location} | {apply_link} | {date_posted} |"
        rows.append(row)

    return "\n".join(rows)


def build_readme(
    template_path: str = "templates/README.template.md",
    data_path: str = "data/listings.json",
    output_path: str = "README.md",
    include_category: Optional[bool] = None,
    max_age_days: Optional[int] = 60,
    reference_date: Optional[datetime.date] = None,
    keep_manual: bool = False,
) -> str:
    """Parse listings, sort and deduplicate, prune expired postings, render README template, and save to output."""
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    listings = load_listings(data_path)
    cleaned_jobs = deduplicate_and_sort(
        listings,
        max_age_days=max_age_days,
        reference_date=reference_date,
        keep_manual=keep_manual,
    )

    if max_age_days is not None and max_age_days > 0:
        pruned_count = len(listings) - len(cleaned_jobs)
        if pruned_count > 0:
            logger.info(
                "Pruned %d expired role(s) (> %d days old) from %s",
                pruned_count,
                max_age_days,
                data_path,
            )

    # Also persist deduplicated and sorted data back to listings.json
    save_listings(cleaned_jobs, data_path)

    # Auto-detect whether template table header has Discipline/Category column
    if include_category is None:
        has_discipline = bool(
            "| Discipline |" in template_content or "| Category |" in template_content
        )
    else:
        has_discipline = include_category

    table_rows = generate_markdown_table(cleaned_jobs, include_category=has_discipline)
    total_roles = str(len(cleaned_jobs))
    last_updated = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    rendered = template_content
    # Replace template placeholders
    rendered = rendered.replace("{{TABLE_ROWS}}", table_rows)
    rendered = rendered.replace("{{table_rows}}", table_rows)
    rendered = rendered.replace("{{LAST_UPDATED}}", last_updated)
    rendered = rendered.replace("{{last_updated}}", last_updated)
    rendered = rendered.replace("{{TOTAL_ROLES}}", total_roles)
    rendered = rendered.replace("{{total_roles}}", total_roles)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    logger.info("README built successfully with %s roles at %s", total_roles, output_path)
    return rendered

