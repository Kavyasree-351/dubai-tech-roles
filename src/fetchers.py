"""ATS endpoint client module for Greenhouse, Lever, and SmartRecruiters."""

import datetime
import logging
from typing import Any, Dict, List, Optional
import requests

from src.filter import filter_job

logger = logging.getLogger(__name__)

# User-Agent to comply with API best practices
DEFAULT_HEADERS = {
    "User-Agent": "dubai-tech-roles-bot/1.0 (+https://github.com/dubai-tech-roles)",
    "Accept": "application/json",
}

DEFAULT_TIMEOUT = 12

# Registry of UAE-operating companies and their ATS providers
DEFAULT_COMPANIES = [
    {"name": "Careem", "ats": "greenhouse", "token": "careem"},
    {"name": "Kitopi", "ats": "greenhouse", "token": "kitopi"},
    {"name": "Sarwa", "ats": "lever", "token": "sarwa"},
    {"name": "Tabby", "ats": "greenhouse", "token": "tabby"},
    {"name": "Property Finder", "ats": "smartrecruiters", "token": "PropertyFinder"},
    {"name": "Postpay", "ats": "lever", "token": "postpay"},
    {"name": "Huspy", "ats": "greenhouse", "token": "huspy"},
]


def _format_date(date_val: Any) -> str:
    """Format various date types to YYYY-MM-DD string."""
    if not date_val:
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    # If epoch millisecond integer (Lever createdAt)
    if isinstance(date_val, (int, float)):
        try:
            return datetime.datetime.fromtimestamp(
                date_val / 1000.0, tz=datetime.timezone.utc
            ).strftime("%Y-%m-%d")
        except Exception:
            return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    # String date parsing
    date_str = str(date_val).strip()
    # Check if ISO format YYYY-MM-DD...
    if len(date_str) >= 10 and date_str[4] == "-" and date_str[7] == "-":
        return date_str[:10]

    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def fetch_greenhouse_jobs(
    company_name: str, board_token: str, session: Optional[requests.Session] = None
) -> List[Dict[str, Any]]:
    """Fetch and normalize job postings from Greenhouse API.

    API: https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    client = session or requests
    listings: List[Dict[str, Any]] = []

    try:
        resp = client.get(
            url,
            params={"content": "true"},
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code != 200:
            logger.warning(
                "Greenhouse board %s returned status %s", board_token, resp.status_code
            )
            return listings

        data = resp.json()
        raw_jobs = data.get("jobs", [])
        for job in raw_jobs:
            job_id = f"gh-{board_token}-{job.get('id')}"
            title = job.get("title", "").strip()
            loc_data = job.get("location", {})
            location = loc_data.get("name", "").strip() if isinstance(loc_data, dict) else str(loc_data)
            apply_url = job.get("absolute_url", "").strip()
            updated_at = job.get("updated_at")

            item = {
                "job_id": job_id,
                "company": company_name,
                "role": title,
                "location": location,
                "apply_url": apply_url,
                "date_posted": _format_date(updated_at),
                "source": "greenhouse",
                "description": job.get("content", ""),
            }
            if filter_job(item):
                # Clean description before saving to listings
                clean_item = {k: v for k, v in item.items() if k != "description"}
                listings.append(clean_item)

    except Exception as e:
        logger.error("Error fetching Greenhouse jobs for %s: %s", company_name, e)

    return listings


def fetch_lever_jobs(
    company_name: str, board_token: str, session: Optional[requests.Session] = None
) -> List[Dict[str, Any]]:
    """Fetch and normalize job postings from Lever API.

    API: https://api.lever.co/v0/postings/{board_token}?mode=json
    """
    url = f"https://api.lever.co/v0/postings/{board_token}"
    client = session or requests
    listings: List[Dict[str, Any]] = []

    try:
        resp = client.get(
            url,
            params={"mode": "json"},
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code != 200:
            logger.warning(
                "Lever board %s returned status %s", board_token, resp.status_code
            )
            return listings

        raw_jobs = resp.json()
        if not isinstance(raw_jobs, list):
            return listings

        for job in raw_jobs:
            job_id = f"lever-{board_token}-{job.get('id')}"
            title = job.get("text", "").strip()
            cats = job.get("categories", {}) or {}
            location = cats.get("location", "").strip() if isinstance(cats, dict) else ""
            apply_url = job.get("hostedUrl") or job.get("applyUrl") or ""
            created_at = job.get("createdAt")
            description = job.get("descriptionPlain") or ""

            item = {
                "job_id": job_id,
                "company": company_name,
                "role": title,
                "location": location,
                "apply_url": apply_url,
                "date_posted": _format_date(created_at),
                "source": "lever",
                "description": description,
            }
            if filter_job(item):
                clean_item = {k: v for k, v in item.items() if k != "description"}
                listings.append(clean_item)

    except Exception as e:
        logger.error("Error fetching Lever jobs for %s: %s", company_name, e)

    return listings


def fetch_smartrecruiters_jobs(
    company_name: str, company_token: str, session: Optional[requests.Session] = None
) -> List[Dict[str, Any]]:
    """Fetch and normalize job postings from SmartRecruiters API.

    API: https://api.smartrecruiters.com/v1/companies/{company_token}/postings
    """
    url = f"https://api.smartrecruiters.com/v1/companies/{company_token}/postings"
    client = session or requests
    listings: List[Dict[str, Any]] = []

    try:
        resp = client.get(
            url,
            headers=DEFAULT_HEADERS,
            timeout=DEFAULT_TIMEOUT,
        )
        if resp.status_code != 200:
            logger.warning(
                "SmartRecruiters company %s returned status %s", company_token, resp.status_code
            )
            return listings

        data = resp.json()
        raw_jobs = data.get("content", [])
        for job in raw_jobs:
            job_id = f"sr-{company_token}-{job.get('id')}"
            title = job.get("name", "").strip()
            loc_data = job.get("location", {}) or {}
            city = loc_data.get("city", "")
            region = loc_data.get("region", "")
            country = loc_data.get("country", "")
            loc_parts = [p for p in [city, region, country] if p]
            location = ", ".join(loc_parts)

            apply_url = f"https://jobs.smartrecruiters.com/{company_token}/{job.get('id')}"
            released_date = job.get("releasedDate")

            item = {
                "job_id": job_id,
                "company": company_name,
                "role": title,
                "location": location,
                "apply_url": apply_url,
                "date_posted": _format_date(released_date),
                "source": "smartrecruiters",
            }
            if filter_job(item):
                listings.append(item)

    except Exception as e:
        logger.error("Error fetching SmartRecruiters jobs for %s: %s", company_name, e)

    return listings


def fetch_all_jobs(
    companies: Optional[List[Dict[str, str]]] = None,
    session: Optional[requests.Session] = None,
) -> List[Dict[str, Any]]:
    """Query all configured ATS endpoints and return filtered tech listings."""
    target_companies = companies or DEFAULT_COMPANIES
    sess = session or requests.Session()
    all_jobs: List[Dict[str, Any]] = []

    for comp in target_companies:
        name = comp["name"]
        ats = comp.get("ats", "").lower()
        token = comp.get("token", "")

        logger.info("Fetching jobs for %s via %s...", name, ats)
        if ats == "greenhouse":
            jobs = fetch_greenhouse_jobs(name, token, session=sess)
        elif ats == "lever":
            jobs = fetch_lever_jobs(name, token, session=sess)
        elif ats == "smartrecruiters":
            jobs = fetch_smartrecruiters_jobs(name, token, session=sess)
        else:
            logger.warning("Unsupported ATS '%s' for company %s", ats, name)
            continue

        logger.info("Retrieved %d matched jobs for %s", len(jobs), name)
        all_jobs.extend(jobs)

    return all_jobs
