import datetime
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
    r"\bsoftware engineering\b",
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
    r"\bai research\b",
    r"\bai researcher\b",
    r"\bartificial intelligence\b",
    r"\bgenai\b",
    r"\bgenerative ai\b",
    r"\bdata scientist\b",
    r"\bdata science\b",
    r"\bdata engineer\b",
    r"\bdata engineering\b",
    r"\bdata analyst\b",
    r"\bdata analytics\b",
    r"\bquant\b",
    r"\bquantitative\b",
    r"\balgo trader\b",
    r"\balgorithmic trading\b",
    r"\btrading\b",
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
    r"\btechnology intern\b",
    r"\btech intern\b",
]

# Patterns explicitly matching student, intern, and early-graduate opportunities
INTERNSHIP_ROLE_PATTERNS: List[str] = [
    r"\bintern\b",
    r"\binternship\b",
    r"\binternships\b",
    r"\binterns\b",
    r"\bgraduate\b",
    r"\bgraduates\b",
    r"\bnew grad\b",
    r"\bnew graduate\b",
    r"\brecent graduate\b",
    r"\bfresh graduate\b",
    r"\bearly graduate\b",
    r"\bearly career\b",
    r"\bearly careers\b",
    r"\btrainee\b",
    r"\btraineeship\b",
    r"\bapprentice\b",
    r"\bapprenticeship\b",
    r"\bfellowship\b",
    r"\baccelerator program\b",
    r"\baccelerator\b",
    r"\bco-op\b",
    r"\bcoop\b",
    r"\bcampus\b",
    r"\bstudent\b",
    r"\bstudents\b",
    r"\bundergraduate\b",
    r"\bundergraduates\b",
    r"\bundergrad\b",
    r"\bjunior\b",
    r"\bentry level\b",
    r"\bentry-level\b",
    r"\bapm\b",
    r"\bassociate product manager\b",
    r"\bassociate project manager\b",
    r"\bassociate project coordinator\b",
]

# Patterns for Product Management and Associate Project Management (intern/early-career scope)
PRODUCT_AND_PROJECT_PATTERNS: List[str] = [
    r"\bproduct manag\w*\b",
    r"\bproduct manager\b",
    r"\bassociate product manager\b",
    r"\bapm\b",
    r"\bproduct intern\b",
    r"\bproduct internship\b",
    r"\bproduct analyst\b",
    r"\bproduct owner\b",
    r"\bproject manag\w*\b",
    r"\bproject manager\b",
    r"\bassociate project manager\b",
    r"\bproject intern\b",
    r"\bproject internship\b",
    r"\bproject coordinator\b",
    r"\btechnical project\b",
    r"\bprogram manager\b",
    r"\bprogram management\b",
]

# Senior / executive exclusion patterns for early career filtering
SENIOR_EXCLUSION_PATTERNS: List[str] = [
    r"\bsenior\b",
    r"\bsr\.\b",
    r"\bsr\b",
    r"\blead\b",
    r"\bprincipal\b",
    r"\bstaff\b",
    r"\bdirector\b",
    r"\bhead of\b",
    r"\bvp\b",
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
    r"\bremote,\s*(?:usa?|united states|uk|india|canada|brazil)\b",
    r"\bremote\s*-\s*(?:usa?|united states|uk|india|canada|brazil)\b",
    r"\bremote\s*\((?:usa?|united states|uk|india|canada|brazil)\)\b",
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


def is_job_expired(
    date_posted: Optional[str],
    max_age_days: int = 60,
    reference_date: Optional[datetime.date] = None,
) -> bool:
    """Determine whether a job posting has exceeded the maximum retention period (expired).

    Args:
        date_posted: Date string (e.g. 'YYYY-MM-DD' or ISO format).
        max_age_days: Maximum number of days a listing remains active (default 60 days).
        reference_date: Optional date to calculate age against (defaults to today UTC).

    Returns:
        bool: True if date is valid and age in days > max_age_days; False otherwise.
    """
    if not date_posted or not isinstance(date_posted, str):
        return False

    date_str = date_posted.strip()
    if not date_str:
        return False

    try:
        if "T" in date_str:
            date_str = date_str.split("T")[0]
        elif " " in date_str:
            date_str = date_str.split(" ")[0]

        parsed_date = datetime.date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return False

    if reference_date is None:
        reference_date = datetime.datetime.now(datetime.timezone.utc).date()

    age_days = (reference_date - parsed_date).days
    return age_days > max_age_days


def filter_expired_jobs(
    jobs: List[Dict[str, Any]],
    max_age_days: int = 60,
    reference_date: Optional[datetime.date] = None,
    keep_manual: bool = False,
) -> List[Dict[str, Any]]:
    """Remove expired jobs from a listings collection.

    Args:
        jobs: List of job dictionaries.
        max_age_days: Maximum age in days before a job is pruned (default 60).
        reference_date: Optional reference date for age calculation.
        keep_manual: If True, jobs with source == 'manual' will not be pruned.

    Returns:
        List[Dict[str, Any]]: Filtered active job listings within retention window.
    """
    active_jobs: List[Dict[str, Any]] = []
    for job in jobs:
        if keep_manual and job.get("source") == "manual":
            active_jobs.append(job)
            continue

        date_posted = job.get("date_posted")
        if is_job_expired(date_posted, max_age_days=max_age_days, reference_date=reference_date):
            continue
        active_jobs.append(job)
    return active_jobs


def filter_job(
    job: Dict[str, Any],
    max_age_days: Optional[int] = None,
    reference_date: Optional[datetime.date] = None,
) -> bool:
    """Complete validation pipeline for a single job listing.

    Checks:
    1. Not an Emiratisation/National-only quota listing.
    2. Matches target technology disciplines.
    3. Located in Dubai, UAE, or valid remote.
    4. Optional expiration cutoff.

    Args:
        job: Dictionary containing job properties (role/title, location, description, etc.).
        max_age_days: Optional maximum age in days before rejection.
        reference_date: Optional reference date for age calculation.

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

    # 4. Optional Expiration check
    if max_age_days is not None:
        if is_job_expired(
            job.get("date_posted"),
            max_age_days=max_age_days,
            reference_date=reference_date,
        ):
            return False

    return True


def matches_internship_or_early_grad_role(
    title: Optional[str], description: Optional[str] = None
) -> bool:
    """Verify if a position is tailored for interns, trainees, students, or early graduates.

    Args:
        title: Job title string.
        description: Optional job description text.

    Returns:
        bool: True if position is an internship or early graduate role, False otherwise.
    """
    if not title:
        return False

    title_lower = title.lower()

    # Reject if clear senior/lead/staff/director role without junior indicators
    has_junior_indicator = any(
        re.search(w, title_lower, re.IGNORECASE)
        for w in [r"\bjunior\b", r"\bintern\b", r"\btrainee\b", r"\bapprentice\b", r"\bentry[- ]level\b"]
    )
    if not has_junior_indicator:
        for sen in SENIOR_EXCLUSION_PATTERNS:
            if re.search(sen, title_lower, re.IGNORECASE):
                return False

    # Check title for internship/early career patterns
    for pattern in INTERNSHIP_ROLE_PATTERNS:
        if re.search(pattern, title_lower, re.IGNORECASE):
            return True

    # Check description for structured cohort keywords if title is generic
    if description:
        desc_lower = description.lower()
        if any(
            term in desc_lower
            for term in [
                "internship program",
                "graduate scheme",
                "graduate programme",
                "early career program",
                "university internship",
            ]
        ):
            return True

    return False


def categorize_tech_role(title: Optional[str]) -> str:
    """Assign a normalized technology, product, or project discipline category to a job title.

    Disciplines:
    1. Software Engineering
    2. AI & Machine Learning
    3. Data Science & Engineering
    4. Quantitative Finance
    5. Product Management
    6. Associate Project Management
    """
    if not title:
        return "Software Engineering"

    t = title.lower()

    # Product Management
    if any(
        k in t
        for k in [
            "product manag",
            "product intern",
            "product analyst",
            "associate product",
            "apm",
            "product owner",
            "product track",
        ]
    ):
        return "Product Management"

    # Associate Project Management
    if any(
        k in t
        for k in [
            "project manag",
            "project intern",
            "project coordinator",
            "associate project",
            "technical project",
            "program manager",
            "program management",
        ]
    ):
        return "Associate Project Management"

    # Quantitative Finance & Trading
    if any(k in t for k in ["quant", "quantitative", "trader", "trading", "algorithmic"]):
        return "Quantitative Finance"

    # AI & Machine Learning
    if any(k in t for k in ["ai ", "ai-", "(ai", "machine learning", "ml ", "mlops", "genai", "generative ai", "deep learning", "llm"]):
        return "AI & Machine Learning"

    # Data Science & Data Engineering
    if any(k in t for k in ["data scientist", "data science", "data engineer", "data engineering", "data analyst", "analytics"]):
        return "Data Science & Engineering"

    # Default to Software Engineering (Backend, Frontend, Full Stack, Systems, Platform, DevOps, SRE)
    return "Software Engineering"


def filter_internship_job(
    job: Dict[str, Any],
    max_age_days: Optional[int] = None,
    reference_date: Optional[datetime.date] = None,
) -> bool:
    """Complete validation pipeline for an internship or early graduate job listing.

    Checks:
    1. Not an Emiratisation/National-only quota listing.
    2. Located in Dubai, UAE, or valid remote.
    3. Matches target disciplines (SWE, AI/ML, Data, Quant, Product Management, Associate Project Management).
    4. Explicitly designed for interns, trainees, students, undergraduates, or early graduates.
    5. Optional expiration cutoff.

    Args:
        job: Dictionary containing job properties (role/title, location, description, etc.).
        max_age_days: Optional maximum age in days before rejection.
        reference_date: Optional reference date for age calculation.

    Returns:
        bool: True if the internship should be included, False otherwise.
    """
    title = job.get("role") or job.get("title") or ""
    location = job.get("location") or ""
    description = job.get("description") or ""

    # 1. Emiratisation exclusion
    if is_emiratisation_role(title, description, location):
        return False

    # 2. UAE Location match
    if not matches_target_location(location):
        return False

    # 3. Early Career / Internship / Student match
    if not matches_internship_or_early_grad_role(title, description):
        return False

    # 4. Optional Expiration check
    if max_age_days is not None:
        if is_job_expired(
            job.get("date_posted"),
            max_age_days=max_age_days,
            reference_date=reference_date,
        ):
            return False

    # 5. Tech / Product / Project Discipline match
    matches_tech = matches_target_role(title)
    title_lower = title.lower()
    matches_pm = any(
        re.search(p, title_lower, re.IGNORECASE) for p in PRODUCT_AND_PROJECT_PATTERNS
    )

    if not (matches_tech or matches_pm):
        # Fallback check on description if title is general like "Tamara Internship Program"
        if description and any(
            k in description.lower()
            for k in [
                "software",
                "engineering",
                "data science",
                "machine learning",
                "quantitative",
                "backend",
                "frontend",
                "product",
                "project",
            ]
        ):
            return True
        return False

    return True


