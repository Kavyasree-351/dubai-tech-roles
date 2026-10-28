"""Unit test suite for dubai-tech-roles pipeline.

Tests filtering logic, Emiratisation exclusions, builder rendering, and ATS fetchers.
"""

import json
from unittest.mock import MagicMock, patch
import pytest

from src.builder import (
    build_readme,
    deduplicate_and_sort,
    generate_markdown_table,
    load_listings,
    save_listings,
)
from src.fetchers import (
    _format_date,
    fetch_ashby_jobs,
    fetch_greenhouse_jobs,
    fetch_lever_jobs,
    fetch_smartrecruiters_jobs,
)
from src.filter import (
    categorize_tech_role,
    filter_internship_job,
    filter_job,
    is_emiratisation_role,
    matches_internship_or_early_grad_role,
    matches_target_location,
    matches_target_role,
)



# ==========================================
# 1. Emiratisation Exclusion Tests
# ==========================================
class TestEmiratisationFilter:
    @pytest.mark.parametrize(
        "title,desc,expected",
        [
            ("Software Engineer - Emiratisation", "", True),
            ("Software Engineer (Emiratization)", "", True),
            ("Backend Developer - Emirati Only", "", True),
            ("Junior Data Analyst", "This role is part of the National Program for talent", True),
            ("Data Scientist - UAE National", "", True),
            ("Graduate Tech Trainee - Nafis Scheme", "", True),
            ("Associate Engineer - Reserved for UAE Nationals", "", True),
            ("Senior Backend Engineer", "Build distributed cloud services with Go.", False),
            ("Machine Learning Engineer", "Deploy LLM systems at scale in Dubai.", False),
            ("Staff Data Scientist", "", False),
        ],
    )
    def test_is_emiratisation_role(self, title, desc, expected):
        assert is_emiratisation_role(title, desc) is expected


# ==========================================
# 2. Target Tech Roles Matching Tests
# ==========================================
class TestTargetRoleMatching:
    @pytest.mark.parametrize(
        "role_title,expected",
        [
            ("Software Engineer", True),
            ("Senior Software Engineer II", True),
            ("Staff Backend Engineer", True),
            ("Frontend Developer (React/Next.js)", True),
            ("Full Stack Engineer", True),
            ("Fullstack Developer", True),
            ("Machine Learning Engineer", True),
            ("Lead AI Engineer", True),
            ("Senior Data Scientist", True),
            ("Data Engineer - Core Pipelines", True),
            ("Quantitative Researcher - High Frequency", True),
            ("Quant Developer (C++)", True),
            ("DevOps Engineer", True),
            ("Site Reliability Engineer (SRE)", True),
            ("Platform Engineer", True),
            ("Solutions Architect", True),
            # Non-tech roles should NOT match
            ("HR Business Partner", False),
            ("Sales Executive", False),
            ("Executive Assistant", False),
            ("Head Chef", False),
            ("Customer Service Agent", False),
            ("Office Administrator", False),
            ("", False),
            (None, False),
        ],
    )
    def test_matches_target_role(self, role_title, expected):
        assert matches_target_role(role_title) is expected


# ==========================================
# 3. Target Location Matching Tests
# ==========================================
class TestTargetLocationMatching:
    @pytest.mark.parametrize(
        "location,expected",
        [
            ("Dubai, United Arab Emirates", True),
            ("Dubai", True),
            ("Abu Dhabi, UAE", True),
            ("DIFC, Dubai", True),
            ("Dubai Internet City", True),
            ("Dubai Silicon Oasis (DSO)", True),
            ("Sharjah, UAE", True),
            ("UAE", True),
            ("Remote", True),
            ("Remote - UAE", True),
            ("Dubai / Remote", True),
            # Excluded or non-UAE locations
            ("London, United Kingdom", False),
            ("New York, NY", False),
            ("Bangalore, India", False),
            ("Remote - US Only", False),
            ("Remote (Europe Only)", False),
            ("", False),
            (None, False),
        ],
    )
    def test_matches_target_location(self, location, expected):
        assert matches_target_location(location) is expected


# ==========================================
# 4. End-to-End Filter Pipeline Tests
# ==========================================
class TestFilterJobPipeline:
    def test_valid_tech_job_in_dubai(self):
        job = {
            "role": "Senior Backend Engineer",
            "location": "Dubai, UAE",
            "description": "Building microservices.",
        }
        assert filter_job(job) is True

    def test_blocks_emiratisation_tech_job(self):
        job = {
            "role": "Software Engineer - Emiratisation",
            "location": "Dubai, UAE",
            "description": "Applicants must be UAE Nationals.",
        }
        assert filter_job(job) is False

    def test_blocks_non_tech_job_in_dubai(self):
        job = {
            "role": "Procurement Specialist",
            "location": "Dubai, UAE",
        }
        assert filter_job(job) is False

    def test_blocks_tech_job_outside_uae(self):
        job = {
            "role": "Senior Frontend Engineer",
            "location": "Berlin, Germany",
        }
        assert filter_job(job) is False


# ==========================================
# 5. Builder Engine Tests
# ==========================================
class TestBuilderEngine:
    def test_deduplicate_and_sort(self):
        raw = [
            {"job_id": "job-1", "company": "A", "role": "SWE", "date_posted": "2026-10-20"},
            {"job_id": "job-1", "company": "A", "role": "SWE", "date_posted": "2026-10-20"},  # duplicate
            {"job_id": "job-2", "company": "B", "role": "ML", "date_posted": "2026-10-25"},
            {"job_id": "job-3", "company": "C", "role": "Data", "date_posted": "2026-10-22"},
        ]
        result = deduplicate_and_sort(raw)
        assert len(result) == 3
        # Should be ordered newest first (2026-10-25, 2026-10-22, 2026-10-20)
        assert result[0]["job_id"] == "job-2"
        assert result[1]["job_id"] == "job-3"
        assert result[2]["job_id"] == "job-1"

    def test_generate_markdown_table(self):
        jobs = [
            {
                "job_id": "1",
                "company": "Careem",
                "role": "Backend Engineer",
                "location": "Dubai, UAE",
                "apply_url": "https://careem.com/job/1",
                "date_posted": "2026-10-25",
            }
        ]
        table = generate_markdown_table(jobs)
        assert "| **Careem** |" in table
        assert "Backend Engineer" in table
        assert "[Apply ↗](https://careem.com/job/1)" in table
        assert "2026-10-25" in table

    def test_build_readme_integration(self, tmp_path):
        template_file = tmp_path / "README.template.md"
        data_file = tmp_path / "listings.json"
        output_file = tmp_path / "README.md"

        template_file.write_text(
            "# Dubai Roles\nTotal: {{TOTAL_ROLES}}\nUpdated: {{LAST_UPDATED}}\n\n{{TABLE_ROWS}}\n",
            encoding="utf-8",
        )
        sample_data = [
            {
                "job_id": "test-1",
                "company": "Kitopi",
                "role": "Data Scientist",
                "location": "Dubai",
                "apply_url": "https://kitopi.com",
                "date_posted": "2026-10-20",
            }
        ]
        data_file.write_text(json.dumps(sample_data), encoding="utf-8")

        rendered = build_readme(
            template_path=str(template_file),
            data_path=str(data_file),
            output_path=str(output_file),
        )

        assert "Total: 1" in rendered
        assert "| **Kitopi** | Data Scientist |" in rendered
        assert output_file.exists()


# ==========================================
# 6. ATS Fetcher Tests (Mocked)
# ==========================================
class TestFetchers:
    def test_format_date_variations(self):
        # Epoch ms (e.g. Lever: 1729814400000 = 2024-10-25)
        formatted_epoch = _format_date(1729814400000)
        assert len(formatted_epoch) == 10
        assert formatted_epoch.startswith("2024-10-")

        # ISO String
        assert _format_date("2026-10-27T12:00:00Z") == "2026-10-27"
        # None fallback
        assert len(_format_date(None)) == 10

    @patch("requests.Session")
    def test_fetch_greenhouse_jobs(self, mock_session_cls):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "jobs": [
                {
                    "id": 101,
                    "title": "Senior Software Engineer",
                    "location": {"name": "Dubai, UAE"},
                    "absolute_url": "https://boards.greenhouse.io/test/jobs/101",
                    "updated_at": "2026-10-25T10:00:00Z",
                    "content": "Python and AWS.",
                },
                {
                    "id": 102,
                    "title": "Senior Software Engineer (Emiratisation)",
                    "location": {"name": "Dubai, UAE"},
                    "absolute_url": "https://boards.greenhouse.io/test/jobs/102",
                    "updated_at": "2026-10-25T10:00:00Z",
                    "content": "For UAE nationals.",
                },
                {
                    "id": 103,
                    "title": "Office Manager",
                    "location": {"name": "Dubai, UAE"},
                    "absolute_url": "https://boards.greenhouse.io/test/jobs/103",
                    "updated_at": "2026-10-25T10:00:00Z",
                },
            ]
        }
        mock_session.get.return_value = mock_resp

        jobs = fetch_greenhouse_jobs("Careem", "careem", session=mock_session)
        assert len(jobs) == 1
        assert jobs[0]["role"] == "Senior Software Engineer"
        assert jobs[0]["company"] == "Careem"

    @patch("requests.Session")
    def test_fetch_lever_jobs(self, mock_session_cls):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [
            {
                "id": "lev-1",
                "text": "Machine Learning Engineer",
                "categories": {"location": "Dubai, UAE"},
                "hostedUrl": "https://jobs.lever.co/sarwa/lev-1",
                "createdAt": 1729814400000,
                "descriptionPlain": "PyTorch and Transformers.",
            },
            {
                "id": "lev-2",
                "text": "Marketing Specialist",
                "categories": {"location": "Dubai, UAE"},
                "hostedUrl": "https://jobs.lever.co/sarwa/lev-2",
                "createdAt": 1729814400000,
            },
        ]
        mock_session.get.return_value = mock_resp

        jobs = fetch_lever_jobs("Sarwa", "sarwa", session=mock_session)
        assert len(jobs) == 1
        assert jobs[0]["role"] == "Machine Learning Engineer"

    @patch("requests.Session")
    def test_fetch_smartrecruiters_jobs(self, mock_session_cls):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "content": [
                {
                    "id": "sr-1",
                    "name": "Staff Data Engineer",
                    "location": {"city": "Dubai", "region": "Dubai", "country": "ae"},
                    "releasedDate": "2026-10-26T00:00:00Z",
                },
                {
                    "id": "sr-2",
                    "name": "Receptionist",
                    "location": {"city": "Dubai", "country": "ae"},
                    "releasedDate": "2026-10-26T00:00:00Z",
                },
            ]
        }
        mock_session.get.return_value = mock_resp

        jobs = fetch_smartrecruiters_jobs("PropertyFinder", "PropertyFinder", session=mock_session)
        assert len(jobs) == 1
        assert jobs[0]["role"] == "Staff Data Engineer"

    @patch("requests.Session")
    def test_fetch_ashby_jobs(self, mock_session_cls):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "jobs": [
                {
                    "id": "ash-1",
                    "title": "Backend Engineer",
                    "location": "Dubai",
                    "publishedAt": "2026-10-26T00:00:00Z",
                    "jobUrl": "https://jobs.ashbyhq.com/ziina/ash-1",
                    "descriptionPlain": "Building APIs",
                },
                {
                    "id": "ash-2",
                    "title": "Chef",
                    "location": "Dubai",
                    "publishedAt": "2026-10-26T00:00:00Z",
                    "jobUrl": "https://jobs.ashbyhq.com/ziina/ash-2",
                    "descriptionPlain": "Cooking",
                },
            ]
        }
        mock_session.get.return_value = mock_resp

        jobs = fetch_ashby_jobs("Ziina", "ziina", session=mock_session)
        assert len(jobs) == 1
        assert jobs[0]["role"] == "Backend Engineer"
        assert jobs[0]["source"] == "ashby"


# ==========================================
# 6. Intern & Early Graduate Filter Tests
# ==========================================
class TestInternshipFilter:
    @pytest.mark.parametrize(
        "title,expected",
        [
            ("Software Engineer: Intern/New Grad", True),
            ("Software Engineering Intern", True),
            ("Graduate Software Engineer", True),
            ("Junior Data Scientist", True),
            ("Commercial Graduate Scheme, Junior Data Scientist", True),
            ("AI Research & Quantitative Analyst Trainee", True),
            ("Binance Accelerator Program - Data Scientist, Analytics", True),
            ("Technology Graduate Trainee", True),
            ("Data Science Intern", True),
            ("Software Engineer Apprentice", True),
            ("Associate Product Manager", True),
            ("APM", True),
            ("Product Management Intern", True),
            ("Associate Project Manager", True),
            ("Project Management Intern", True),
            ("Technical Project Coordinator Intern", True),
            # Non-intern standard roles should return False
            ("Software Engineer", False),
            ("Backend Engineer", False),
            ("Data Scientist", False),
            ("Quantitative Researcher", False),
            ("Product Manager", False),
            ("Project Manager", False),
            # Senior/lead roles should return False even if keywords resemble
            ("Senior Backend Engineer", False),
            ("Lead Data Scientist", False),
            ("Principal AI Architect", False),
            ("Staff Machine Learning Engineer", False),
            ("Director of Engineering", False),
            ("Senior Product Manager", False),
            ("Lead Project Manager", False),
        ],
    )
    def test_matches_internship_or_early_grad_role(self, title, expected):
        assert matches_internship_or_early_grad_role(title) is expected

    @pytest.mark.parametrize(
        "title,expected_category",
        [
            ("Quantitative Developer Intern", "Quantitative Finance"),
            ("Algo Trader Trainee", "Quantitative Finance"),
            ("AI Research Intern", "AI & Machine Learning"),
            ("Machine Learning Engineer - Graduate Scheme", "AI & Machine Learning"),
            ("Data Science Intern", "Data Science & Engineering"),
            ("Junior Data Engineer", "Data Science & Engineering"),
            ("Software Engineer: Intern/New Grad", "Software Engineering"),
            ("Full Stack Developer Intern", "Software Engineering"),
            ("DevOps Engineer Trainee", "Software Engineering"),
            ("Product Management Intern", "Product Management"),
            ("Associate Product Manager", "Product Management"),
            ("APM - Early Career", "Product Management"),
            ("Associate Project Manager", "Associate Project Management"),
            ("Project Management Intern", "Associate Project Management"),
            ("Technical Project Coordinator Intern", "Associate Project Management"),
        ],
    )
    def test_categorize_tech_role(self, title, expected_category):
        assert categorize_tech_role(title) == expected_category

    def test_filter_internship_job_valid(self):
        job = {
            "role": "Software Engineer: Intern/New Grad",
            "location": "Dubai, UAE",
            "description": "Develop high-scale cloud backend services.",
        }
        assert filter_internship_job(job) is True

    def test_filter_internship_job_valid_pm(self):
        job = {
            "role": "Associate Product Manager",
            "location": "Dubai, UAE",
            "description": "Drive product roadmaps for fintech solutions.",
        }
        assert filter_internship_job(job) is True

    def test_filter_internship_job_valid_project(self):
        job = {
            "role": "Project Management Intern",
            "location": "Dubai, UAE",
            "description": "Coordinate agile engineering delivery sprints.",
        }
        assert filter_internship_job(job) is True


    def test_filter_internship_job_blocks_emiratisation(self):
        job = {
            "role": "Software Engineering Intern - Emiratisation Scheme",
            "location": "Dubai, UAE",
            "description": "National career development program.",
        }
        assert filter_internship_job(job) is False

    def test_filter_internship_job_blocks_non_tech(self):
        job = {
            "role": "Marketing Intern",
            "location": "Dubai, UAE",
            "description": "Social media and branding campaigns.",
        }
        assert filter_internship_job(job) is False

    def test_filter_internship_job_blocks_non_uae(self):
        job = {
            "role": "Software Engineer Intern",
            "location": "London, United Kingdom",
            "description": "Work in our UK development center.",
        }
        assert filter_internship_job(job) is False

    def test_filter_internship_job_blocks_experienced_role(self):
        job = {
            "role": "Senior Software Engineer",
            "location": "Dubai, UAE",
            "description": "Lead distributed microservices.",
        }
        assert filter_internship_job(job) is False

    def test_markdown_table_with_discipline(self):
        jobs = [
            {
                "company": "Asula Labs",
                "role": "Software Engineer: Intern/New Grad",
                "category": "Software Engineering",
                "location": "Dubai, UAE",
                "apply_url": "https://jobs.ashbyhq.com/asula",
                "date_posted": "2026-10-28",
            }
        ]
        table = generate_markdown_table(jobs, include_category=True)
        assert "| **Asula Labs** | Software Engineer: Intern/New Grad | `Software Engineering` | Dubai, UAE | [Apply ↗](https://jobs.ashbyhq.com/asula) | 2026-10-28 |" in table

