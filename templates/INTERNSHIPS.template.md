<div align="center">

# 🎓 🇦🇪 Dubai & UAE Tech Internships & Early Careers

**A curated, production-ready directory tracking Software Engineering, AI/ML, Data Science, and Quantitative Finance internships & early career opportunities across Dubai and the United Arab Emirates — updated directly in this document every single day.**

[![Automated Scraper](https://github.com/Kavyasree-351/dubai-tech-roles/actions/workflows/fetch_jobs.yml/badge.svg)](https://github.com/Kavyasree-351/dubai-tech-roles/actions)
[![README Builder](https://github.com/Kavyasree-351/dubai-tech-roles/actions/workflows/generate_readme.yml/badge.svg)](https://github.com/Kavyasree-351/dubai-tech-roles/actions)
[![Active Roles](https://img.shields.io/badge/Active_Internships-{{TOTAL_ROLES}}-purple?style=flat-square&logo=target)](data/internships.json)
[![Last Updated](https://img.shields.io/badge/Last_Updated-{{LAST_UPDATED}}-brightgreen?style=flat-square&logo=clock)](data/internships.json)
[![Target Audience](https://img.shields.io/badge/Target-Students_%26_Early_Grads-orange?style=flat-square&logo=google-classroom)](INTERNSHIPS.md)
[![Full Directory](https://img.shields.io/badge/All_Tech_Roles-README.md-blue?style=flat-square&logo=readme)](README.md)

[**🔥 View Open Internships**](#-open-tech-internships--graduate-roles-updated-daily) • [**🎯 Eligibility & Rules**](#-eligibility--filtering-methodology) • [**🔄 Daily Sync Architecture**](#-how-daily-updates-work) • [**🤝 Contributing**](#-contributing)

</div>

---

### 📊 Quick Overview

| Metric | Status |
| :--- | :--- |
| **Active Intern & Graduate Roles** | `{{TOTAL_ROLES}}` verified positions |
| **Target Candidate Profile** | Students (Undergraduate, Master's, PhD) & Fresh Graduates (0–2 YOE) |
| **Core Disciplines** | Software Engineering, AI/ML, Data Science & Analytics, Quantitative Trading |
| **Geographic Scope** | Dubai (DIFC, Internet City, DSO), Abu Dhabi (ADGM, Hub71), UAE Remote |
| **Emiratisation Policy** | Excluded (Open-market positions for all qualified domestic and international applicants) |
| **Last Synchronized** | `{{LAST_UPDATED}}` |
| **Update Frequency** | **Every 6 Hours** (Automated via GitHub Actions) |

---

## 💼 Open Tech Internships & Graduate Roles (Updated Daily)

> **Tip:** Roles are sorted chronologically with the newest postings at the top. Click **[Apply ↗]** to view the full job specification and apply directly on the official employer careers portal.

| Company | Role | Discipline | Location | Apply Link | Date Posted |
| :--- | :--- | :--- | :--- | :--- | :--- |
{{TABLE_ROWS}}

---

## 🎯 Eligibility & Filtering Methodology

Every listing undergoes automated validation through [src/filter.py](src/filter.py) prior to inclusion:

1. **Target Technology Disciplines Only**:
   - **Software Engineering**: Backend, Frontend, Full Stack, Systems, Platform, DevOps, SRE, Mobile, Cloud, Security.
   - **Artificial Intelligence & Machine Learning**: AI Engineer, ML Engineer, MLOps, LLM / GenAI, AI Research.
   - **Data Science & Data Engineering**: Data Scientist, Data Engineer, Data Analyst, Analytics Engineer.
   - **Quantitative Finance & Algorithmic Trading**: Quant Researcher, Quant Developer, Quantitative Trader.

2. **UAE Scoped Locations**:
   - Explicitly restricted to Dubai, Abu Dhabi, DIFC, Dubai Internet City, DSO (Silicon Oasis), Sharjah, UAE-wide, or verified UAE-friendly Remote.
   - Positions restricted to non-UAE territories (e.g., "US Only", "Europe Only", "Canada Only", "India Only") are automatically rejected.

3. **Strict Internship & Early Graduate Scope**:
   - Verified for student, intern, co-op, apprentice, trainee, new graduate, or accelerator cohort status.
   - Senior, Lead, Staff, Principal, and Director level openings are strictly excluded.

4. **Emiratisation Policy**:
   - Listings restricted to UAE national quotas (containing terms like *Emiratisation*, *Emirati*, *National Program*, *Nafis*) are excluded.
   - While national workforce programs are crucial for citizen talent development, this directory serves open-market students and graduates globally looking to start or transition their tech career within the UAE. For official UAE national programs, please visit [Nafis](https://nafis.gov.ae).

---

## 🔄 How Daily Updates Work

This repository runs an autonomous synchronization pipeline every 6 hours:

1. **Scheduled Polling**: GitHub Actions triggers [`.github/workflows/fetch_jobs.yml`](.github/workflows/fetch_jobs.yml).
2. **ATS Querying**: The scraper queries live ATS API endpoints (Greenhouse, Ashby, Lever, SmartRecruiters) for top technology employers and trading firms operating in the UAE.
3. **Rigorous Filtering**: Each candidate role is checked against technical keyword patterns, student/intern eligibility criteria, and exclusion lists.
4. **Table Recompilation**: The markdown table above and [`data/internships.json`](data/internships.json) are updated automatically.

---

## 🤝 Contributing

Found an open internship or graduate tech role in the UAE that isn't listed here yet? Community additions are warmly welcomed!

- **Add a Position**: Open a Pull Request adding your entry to [`data/internships.json`](data/internships.json).
- **Add a Company ATS Token**: Submit an ATS board token in [`src/fetchers.py`](src/fetchers.py).
- **Report Expired Postings**: Open an Issue or submit a PR removing inactive listings.

Check out our [Contribution Guidelines](CONTRIBUTING.md) for details on schema and local testing.

---

## ⚙️ Automation & CI/CD

- **6-Hour Scraper Workflow** ([`.github/workflows/fetch_jobs.yml`](.github/workflows/fetch_jobs.yml)): Queries ATS endpoints, filters early-career roles, updates `data/internships.json`, and rebuilds `INTERNSHIPS.md`.
- **Markdown Compilation on PR** ([`.github/workflows/generate_readme.yml`](.github/workflows/generate_readme.yml)): Rebuilds markdown tables whenever data files or templates are updated.
