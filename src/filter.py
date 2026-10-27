"""Filtering and matching engine for Dubai and UAE tech roles."""

import re
from typing import Any, Dict, List, Optional

# Keywords that explicitly exclude jobs reserved for national quota programs.
# While vital for citizens, this repository tracks open-market developer positions.
EXCLUSION_TERMS: List[str] = [
    r"\bemiratisation\b",
    r"\bemiratization\b",
    r"\bemirati\b",
    r"\bnational program\b",
    r"\buae national\b",
    r"\buae nationals\b",
    r"\bnational only\b",
    r"\bfor uae nationals\b",
    r"\bnafis\b",
]

# Target technical engineering and scientific job title patterns
TARGET_ROLE_PATTERNS: List[str] = [
    r"\bsoftware engineer\b",
    r"\bsoftware developer\b",
    r"\bswe\b",
    r"\bbackend\b",
    r"\bback-end\b",
    r"\bback end\b",
    r"\bfrontend\b",
    r"\bfront-end\b",
    r"\bfront end\b",
    r"\bfull stack\b",
    r"\bfullstack\b",
    r"\bfull-stack\b",
    r"\bmachine learning\b",
    r"\bml engineer\b",
    r"\bmlops\b",
    r"\bai engineer\b",
    r"\bartificial intelligence\b",
    r"\bgenai\b",
    r"\bgenerative ai\b",
    r"\bdata scientist\b",
    r"\bdata science\b",
    r"\bdata engineer\b",
    r"\bdata engineering\b",
    r"\bquant\b",
    r"\bquantitative\b",
    r"\bdevops\b",
    r"\bplatform engineer\b",
    r"\bsite reliability engineer\b",
    r"\bsre\b",
    r"\bcloud engineer\b",
    r"\binfrastructure engineer\b",
    r"\bsystems engineer\b",
    r"\bembedded engineer\b",
    r"\bfirmware engineer\b",
    r"\bsecurity engineer\b",
    r"\btech lead\b",
    r"\bengineering manager\b",
    r"\barchitect\b",
]

# UAE and regional location patterns
TARGET_LOCATION_PATTERNS: List[str] = [
    r"\bdubai\b",
    r"\babu dhabi\b",
    r"\bdifc\b",
    r"\bdubai internet city\b",
    r"\bdic\b",
    r"\bdso\b",
    r"\bdubai silicon oasis\b",
    r"\buae\b",
    r"\bu\.a\.e\b",
    r"\bunited arab emirates\b",
    r"\bsharjah\b",
    r"\bremote\b",
]

# Explicit non-UAE remote restrictions (e.g., "Remote - US Only", "Remote (Europe)")
NON_UAE_REMOTE_PATTERNS: List[str] = [
    r"\bus only\b",
    r"\busa only\b",
    r"\bnorth america\b",
    r"\beurope only\b",
    r"\buk only\b",
    r"\blatam\b",
    r"\bapac\b",
    r"\bindia only\b",
]


def is_emiratisation_role(*texts: Optional[str]) -> bool:
    """Check if any provided text mentions Emiratisation or national quota requirements.

    Args:
        *texts: Strings to inspect (e.g. title, description, department, tags).

    Returns:
        bool: True if an exclusion term is matched, False otherwise.
    """
    combined = " ".join(t for t in texts if t).lower()
    if not combined:
        return False

    for pattern in EXCLUSION_TERMS:
        if re.search(pattern, combined, re.IGNORECASE):
            return True
    return False


def matches_target_role(title: Optional[str]) -> bool:
    """Verify if a job title aligns with Software, AI, ML, Data, or Quant disciplines.

    Args:
        title: Job title string.

    Returns:
        bool: True if matches target tech roles, False otherwise.
    """
    if not title:
        return False

    title_lower = title.lower()
    for pattern in TARGET_ROLE_PATTERNS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return True
    return False


def matches_target_location(location: Optional[str]) -> bool:
    """Verify if a location is within Dubai, UAE, or open to UAE candidates.

    Args:
        location: Location string from ATS or posting.

    Returns:
        bool: True if in Dubai/UAE or viable remote, False otherwise.
    """
    if not location:
        return False

    loc_lower = location.lower()

    # Reject non-UAE restricted remote positions
    for non_uae_pattern in NON_UAE_REMOTE_PATTERNS:
        if re.search(non_uae_pattern, loc_lower, re.IGNORECASE):
            return False

    for pattern in TARGET_LOCATION_PATTERNS:
        if re.search(pattern, loc_lower, re.IGNORECASE):
            return True
    return False


def filter_job(job: Dict[str, Any]) -> bool:
    """Complete validation pipeline for a single job listing.

    Checks:
    1. Not an Emiratisation/National-only quota listing.
    2. Matches target technology disciplines.
    3. Located in Dubai, UAE, or valid remote.

    Args:
        job: Dictionary containing job properties (role/title, location, description, etc.).

    Returns:
        bool: True if the job should be included, False otherwise.
    """
    title = job.get("role") or job.get("title") or ""
    location = job.get("location") or ""
    description = job.get("description") or ""

    # 1. Emiratisation check
    if is_emiratisation_role(title, description, location):
        return False

    # 2. Location check
    if not matches_target_location(location):
        return False

    # 3. Role check
    if not matches_target_role(title):
        return False

    return True
