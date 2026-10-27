<div align="center">

# 🇦🇪 Dubai & UAE Tech Roles

**A curated, production-ready directory tracking Software Engineering, AI, ML, Data Science, and Quantitative positions across Dubai and the United Arab Emirates.**

[![Automated Scraper](https://github.com/dubai-tech-roles/actions/workflows/fetch_jobs.yml/badge.svg)](https://github.com/dubai-tech-roles/actions)
[![README Builder](https://github.com/dubai-tech-roles/actions/workflows/generate_readme.yml/badge.svg)](https://github.com/dubai-tech-roles/actions)
[![Active Roles](https://img.shields.io/badge/Active_Roles-3-blue?style=flat-square&logo=target)](data/listings.json)
[![Last Updated](https://img.shields.io/badge/Last_Updated-2026-10-27-brightgreen?style=flat-square&logo=clock)](data/listings.json)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[**Explore Listings**](#-open-tech-roles-in-the-uae) • [**Filtering Methodology**](#-filtering-methodology) • [**How to Contribute**](#-contributing) • [**Automated Scraper**](#-automation--cicd)

</div>

---

### 📊 Quick Overview

| Metric | Status |
| :--- | :--- |
| **Total Active Tech Roles** | `3` open positions |
| **Monitored ATS Endpoints** | Greenhouse, Lever, SmartRecruiters + Community PRs |
| **Last Synchronized** | `2026-10-27` |
| **Primary Hubs** | Dubai (DIFC, Internet City, DSO), Abu Dhabi (Hub71), UAE Remote |

---

## 🎯 Filtering Methodology

Every listing inside [`data/listings.json`](data/listings.json) undergoes automated validation before inclusion:

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

## 💼 Open Tech Roles in the UAE

| Company | Role | Location | Apply Link | Date Posted |
| :--- | :--- | :--- | :--- | :--- |
| **Careem** | Senior Backend Engineer - Core Services | Dubai, UAE | [Apply ↗](https://www.careem.com/careers/job/careem-sr-backend-eng-001) | 2026-10-25 |
| **Sarwa** | Staff Machine Learning Engineer - WealthTech | DIFC, Dubai, UAE | [Apply ↗](https://www.sarwa.co/careers/job/sarwa-staff-ml-eng-002) | 2026-10-24 |
| **Kitopi** | Lead Data Scientist - Kitchen Intelligence | Dubai Internet City, UAE | [Apply ↗](https://careers.kitopi.com/job/kitopi-lead-data-scientist-003) | 2026-10-23 |

---

## 🤝 Contributing

Contributions from the developer community keep this database active and accurate!

- **Add or Update a Job**: Open a Pull Request adding an entry to [`data/listings.json`](data/listings.json).
- **Add a Company ATS**: Add your company's Greenhouse, Lever, or SmartRecruiters board token to `src/fetchers.py`.
- **Report Expired Listings**: Open an Issue or submit a PR removing inactive listings.

Check out our [Contribution Guidelines](CONTRIBUTING.md) for data schema details and local setup.

---

## ⚙️ Automation & CI/CD

- **6-Hour Scraper Workflow** ([`.github/workflows/fetch_jobs.yml`](.github/workflows/fetch_jobs.yml)): Queries official ATS APIs every 6 hours, filters tech roles, updates `data/listings.json`, and rebuilds `README.md`.
- **README Compilation on PR** ([`.github/workflows/generate_readme.yml`](.github/workflows/generate_readme.yml)): Rebuilds the markdown table on any merge or changes to data files.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
