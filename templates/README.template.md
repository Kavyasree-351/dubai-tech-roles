<div align="center">

# 🇦🇪 Dubai & UAE Tech Roles

**A curated, production-ready directory tracking Software Engineering, AI, ML, Data Science, and Quantitative positions across Dubai and the United Arab Emirates — updated directly in this README every single day.**

[![Automated Scraper](https://github.com/Kavyasree-351/dubai-tech-roles/actions/workflows/fetch_jobs.yml/badge.svg)](https://github.com/Kavyasree-351/dubai-tech-roles/actions)
[![README Builder](https://github.com/Kavyasree-351/dubai-tech-roles/actions/workflows/generate_readme.yml/badge.svg)](https://github.com/Kavyasree-351/dubai-tech-roles/actions)
[![Active Roles](https://img.shields.io/badge/Active_Roles-{{TOTAL_ROLES}}-blue?style=flat-square&logo=target)](data/listings.json)
[![Last Updated](https://img.shields.io/badge/Last_Updated-{{LAST_UPDATED}}-brightgreen?style=flat-square&logo=clock)](data/listings.json)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

[**🔥 View Open Roles**](#-open-tech-roles-in-the-uae-updated-daily) • [**🔄 Daily Sync Architecture**](#-how-daily-updates-work) • [**🎯 Filtering Methodology**](#-filtering-methodology) • [**🤝 Contributing**](#-contributing)

</div>

---

### 📊 Quick Overview

| Metric | Status |
| :--- | :--- |
| **Total Active Tech Roles** | `{{TOTAL_ROLES}}` verified positions |
| **Last Synchronized** | `{{LAST_UPDATED}}` |
| **Monitored ATS Endpoints** | Greenhouse, Lever, SmartRecruiters + Community PRs |
| **Primary Hubs** | Dubai (DIFC, Internet City, DSO), Abu Dhabi (Hub71), UAE Remote |
| **Update Frequency** | **Every 6 Hours** (automated via GitHub Actions) |

---

## 💼 Open Tech Roles in the UAE (Updated Daily)

> **Tip:** Roles are sorted chronologically with the newest postings at the top. Click **[Apply ↗]** to view and apply on the official company careers page.

| Company | Role | Location | Apply Link | Date Posted |
| :--- | :--- | :--- | :--- | :--- |
{{TABLE_ROWS}}

---

## 🔄 How Daily Updates Work

This repository does **not** require manual updates to stay fresh. It runs an end-to-end automated pipeline every day:

1. **Scheduled Polling**: Every 6 hours, a GitHub Actions cron job triggers [`fetch_jobs.yml`](.github/workflows/fetch_jobs.yml).
2. **ATS Querying**: The bot queries official Applicant Tracking System (ATS) APIs (Greenhouse, Lever, SmartRecruiters) for top tech employers operating in Dubai and the UAE.
3. **Rigorous Filtering**: Each listing is validated against technical title patterns, location boundaries, and exclusion policies.
4. **README Synchronization**: The markdown table above is recompiled automatically and pushed back to `main`, ensuring you can find today's open roles directly from this README at any time.

---

## 🎯 Filtering Methodology

Every listing undergoes automated validation through [src/filter.py](src/filter.py) before inclusion:

1. **Target Technology Disciplines Only**:
   - Software Engineering (Backend, Frontend, Full Stack, Systems, Platform, DevOps, SRE).
   - Artificial Intelligence & Machine Learning (AI Engineer, ML Engineer, MLOps, LLM / GenAI).
   - Data Science & Data Engineering.
   - Quantitative Finance & Algorithmic Trading (Quant Researcher, Quant Developer, Trader).
2. **UAE Scoped Locations**:
   - Dubai, Abu Dhabi, DIFC, Dubai Internet City, DSO (Silicon Oasis), Sharjah, UAE-wide, or verified UAE-friendly Remote.
   - Positions restricted to non-UAE territories (e.g. "US Only", "Europe Only") are automatically rejected.
3. **Emiratisation Policy**:
   - Job listings restricted to UAE national quotas (e.g. containing terms like *Emiratisation*, *Emirati*, *National Program*, *Nafis*) are excluded.
   - While national workforce programs are crucial for citizen talent development, this repository serves open-market candidates globally looking to relocate or transition within the UAE tech ecosystem. For official Emiratisation listings, please visit [Nafis](https://nafis.gov.ae).

---

## 🤝 Contributing

Contributions from the developer community keep this database active and accurate!

- **Add or Update a Job**: Open a Pull Request adding an entry to [`data/listings.json`](data/listings.json).
- **Add a Company ATS**: Add your company's Greenhouse, Lever, or SmartRecruiters board token to [`src/fetchers.py`](src/fetchers.py).
- **Report Expired Listings**: Open an Issue or submit a PR removing inactive listings.

Check out our [Contribution Guidelines](CONTRIBUTING.md) for data schema details and local setup.

---

## ⚙️ Automation & CI/CD

- **6-Hour Scraper Workflow** ([`.github/workflows/fetch_jobs.yml`](.github/workflows/fetch_jobs.yml)): Queries official ATS APIs every 6 hours, filters tech roles, updates `data/listings.json`, and rebuilds `README.md`.
- **README Compilation on PR** ([`.github/workflows/generate_readme.yml`](.github/workflows/generate_readme.yml)): Rebuilds the markdown table on any merge or changes to data files.
