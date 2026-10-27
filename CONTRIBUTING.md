# Contributing to `dubai-tech-roles` 🇦🇪

Thank you for your interest in contributing to **dubai-tech-roles**! This repository tracks Software Engineering, AI, ML, Data Science, and Quantitative positions in Dubai and across the United Arab Emirates.

---

## Table of Contents
1. [Inclusion Criteria](#inclusion-criteria)
2. [Emiratisation Policy](#emiratisation-policy)
3. [Ways to Contribute](#ways-to-contribute)
   - [Add or Edit a Job Listing](#1-add-or-edit-a-job-listing-in-datalistingsjson)
   - [Add an Automated ATS Board](#2-add-an-automated-ats-board-in-srcfetcherspy)
   - [Improve Filtering Rules](#3-improve-filtering-rules-in-srcfilterpy)
4. [Data Schema (`data/listings.json`)](#data-schema)
5. [Local Development & Testing](#local-development--testing)
6. [Submitting a Pull Request](#submitting-a-pull-request)

---

## Inclusion Criteria

Every position listed must satisfy the following:
1. **Discipline**: Technical roles in Software Engineering (Frontend, Backend, Full Stack, Systems, Infrastructure, DevOps, SRE), AI/ML (Machine Learning Engineer, Data Scientist, AI Researcher, MLOps), or Quantitative Finance (Quant Developer, Quant Researcher).
2. **Location**: Located in Dubai, Abu Dhabi, DIFC, Dubai Internet City, DSO, Sharjah, UAE-wide, or Remote roles open to UAE-based developers.
3. **Application Link**: Direct link to the official company careers page or ATS (Greenhouse, Lever, SmartRecruiters, Workday, etc.). Third-party spam/aggregator links are not accepted.

---

## Emiratisation Policy

Positions reserved under UAE national workforce quota programs (e.g. marked as **Emiratisation**, **Emirati**, **UAE National Only**, or via **Nafis**) are intentionally excluded from this tracker.

- **Why?** National quota positions are legally restricted to UAE citizens and cannot be applied to by general, expatriate, or international applicants.
- **Where to find Emiratisation roles?** If you are a UAE citizen looking for dedicated national career programs, please consult the official UAE government platform at [Nafis (nafis.gov.ae)](https://nafis.gov.ae).

---

## Ways to Contribute

### 1. Add or Edit a Job Listing in `data/listings.json`
If you found an open role that hasn't been fetched yet:
1. Fork the repository and open `data/listings.json`.
2. Add a new object to the list matching the schema below.
3. Run `python main.py` to regenerate `README.md`.
4. Commit your changes and open a Pull Request.

### 2. Add an Automated ATS Board in `src/fetchers.py`
If a UAE tech employer uses Greenhouse, Lever, or SmartRecruiters, add their company to `DEFAULT_COMPANIES` in `src/fetchers.py`:

```python
{"name": "Company Name", "ats": "greenhouse", "token": "board_token"},
# or
{"name": "Company Name", "ats": "lever", "token": "board_token"},
# or
{"name": "Company Name", "ats": "smartrecruiters", "token": "company_token"},
```

### 3. Improve Filtering Rules in `src/filter.py`
Help refine regex patterns to capture new technical specializations or edge cases in location names.

---

## Data Schema

Each entry inside `data/listings.json` must adhere to this structure:

```json
{
  "job_id": "careem-sr-backend-eng-001",
  "company": "Careem",
  "role": "Senior Backend Engineer - Core Services",
  "location": "Dubai, UAE",
  "apply_url": "https://www.careem.com/careers/job/careem-sr-backend-eng-001",
  "date_posted": "2026-10-25",
  "source": "manual"
}
```

| Field | Type | Description |
| :--- | :--- | :--- |
| `job_id` | `string` | Unique identifier (e.g. `company-role-slug` or ATS identifier). |
| `company` | `string` | Name of the hiring company. |
| `role` | `string` | Official job title. |
| `location` | `string` | Primary location (must include Dubai, Abu Dhabi, UAE, or valid Remote). |
| `apply_url` | `string` | Direct link to application page. |
| `date_posted` | `string` | ISO format `YYYY-MM-DD`. |
| `source` | `string` | `"manual"`, `"greenhouse"`, `"lever"`, or `"smartrecruiters"`. |

---

## Local Development & Testing

1. **Clone your fork**:
   ```bash
   git clone https://github.com/<your-username>/dubai-tech-roles.git
   cd dubai-tech-roles
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run unit tests**:
   ```bash
   pytest -v
   ```

5. **Build README**:
   ```bash
   python main.py --build
   ```

6. **Test live fetching (optional)**:
   ```bash
   python main.py --fetch
   ```

---

## Submitting a Pull Request

- Provide a concise PR title: e.g. `feat(data): add Senior ML Engineer role at Kitopi` or `feat(ats): add Tabby to Greenhouse fetcher`.
- Ensure all tests pass (`pytest`).
- Avoid adding expired or duplicate positions.
- All contributions are released under the [MIT License](LICENSE).
