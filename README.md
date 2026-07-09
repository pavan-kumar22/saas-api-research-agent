# SaaS API Research Agent

An automated research pipeline that discovers, analyzes, verifies, and summarizes public SaaS APIs using official developer documentation and Large Language Models (LLMs).

The project was built as part of the **Composio Research Assessment** and demonstrates an end-to-end AI-powered research workflow—from documentation discovery to an interactive dashboard.

---

# Overview

Modern SaaS platforms expose APIs with different authentication methods, documentation quality, and developer experiences. Manually researching hundreds of APIs is repetitive and time-consuming.

This project automates that process by:

- Discovering official API documentation
- Ranking documentation sources
- Extracting structured API information using an LLM
- Verifying extracted information
- Generating research insights
- Presenting the results in an interactive dashboard

---

# Objective

Research 100 SaaS applications and automatically identify:

- API Category
- Authentication Method
- Self-Serve Availability
- API Surface
- MCP Support
- Buildability
- Common Blockers
- Official Documentation URL

Finally, summarize the findings through visual analytics and manual verification.

---

# Features

- Automated documentation discovery
- Official documentation prioritization
- AI-powered information extraction
- Automatic verification
- Insight generation
- Interactive dashboard
- Human validation sample
- CSV & JSON exports

---

# System Architecture

```
                    +----------------+
                    |   apps.csv     |
                    +----------------+
                            |
                            ▼
                 Documentation Search
                            |
                            ▼
                Documentation Ranking
                            |
                            ▼
               Extraction Agent (LLM)
                            |
                            ▼
                Verification Agent
                            |
                            ▼
                  research.csv
                            |
                            ▼
                Insight Generator
                            |
                            ▼
                 insights.json
                            |
                            ▼
                 HTML Dashboard
```

---

# Workflow

## Step 1 — Documentation Search

The search agent searches the web for official developer documentation using DDGS.

Example:

```
Slack official developer API documentation
```

The search results are ranked to prioritize official documentation.

---

## Step 2 — Documentation Ranking

Each search result is scored.

Higher scores are given to URLs containing:

- developer
- developers
- docs
- api
- rest
- graphql

Low-quality sources such as:

- Reddit
- Medium
- YouTube
- Blog posts
- GitHub repositories

are penalized.

---

## Step 3 — Extraction Agent

The top documentation URLs are sent to an LLM through OpenRouter.

The model extracts:

- Category
- Authentication
- Self Serve
- API Surface
- MCP Support
- Buildability
- Blockers
- Evidence URL

Output format:

```json
{
  "category": "CRM",
  "authentication": "OAuth2",
  "self_serve": "Yes",
  "api_surface": "REST",
  "mcp": "Unknown",
  "buildability": "High",
  "blocker": "None",
  "evidence": "https://..."
}
```

---

## Step 4 — Verification Agent

The verification module validates the extracted information.

Checks include:

- URL accessibility
- HTTP status
- Official documentation domain
- Authentication keywords
- REST / GraphQL / SOAP references

Each application receives:

- Verified
- Confidence
- Verification Notes

---

## Step 5 — Insight Generator

The research dataset is analyzed to generate project-wide insights.

Generated metrics include:

- Authentication distribution
- Categories
- API Surface
- Buildability
- Self Serve percentage
- MCP Support
- Enterprise gated APIs
- Common blockers
- Easy integration opportunities

The insights are stored as:

```
output/insights.json
```

---

## Step 6 — Dashboard

The HTML dashboard visualizes the complete research.

Dashboard sections include:

- Workflow diagram
- Key metrics
- Pie charts
- Bar charts
- Research table
- Verification table
- Lessons learned

---

# Folder Structure

```
composio-assessment/
│
├── agent/
│   ├── analysis.py
│   ├── extract.py
│   ├── fetch_docs.py
│   ├── insights.py
│   ├── research_agent.py
│   ├── save.py
│   ├── search.py
│   ├── utils.py
│   └── verify.py
│
├── data/
│   └── apps.csv
│
├── html/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── workflow.svg
│
├── output/
│   ├── insights.json
│   ├── research.csv
│   └── charts/
│
├── requirements.txt
├── README.md
└── .env
```

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| OpenRouter | LLM inference |
| DDGS | Documentation search |
| Pandas | Data processing |
| Requests | Verification |
| JSON | Structured outputs |
| HTML | Dashboard |
| CSS | Styling |
| JavaScript | Dashboard logic |
| Chart.js | Data visualization |

---

# Installation

Clone the repository

```bash
git clone <repository-url>

cd composio-assessment
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```text
OPENROUTER_API_KEY=your_api_key_here
```

---

# Running the Project

## Step 1

Run the research pipeline

```bash
python agent/research_agent.py
```

Generates

```
output/research.csv
```

---

## Step 2

Run verification

```bash
python agent/verify.py
```

Generates verification metadata.

---

## Step 3

Generate insights

```bash
python agent/insights.py
```

Creates

```
output/insights.json
```

---

## Step 4

Open the dashboard

```
html/index.html
```

---

# Output Files

## research.csv

Contains structured information for every researched application.

Example:

| App | Authentication | API Surface | Evidence |
|-----|----------------|------------|----------|
| Slack | OAuth2 | REST | docs.slack.dev |

---

## insights.json

Contains project-wide analytics including:

- Authentication percentages
- Categories
- Buildability
- API surfaces
- Self-Serve adoption
- Blockers
- MCP support
- Enterprise gated APIs

---

## Dashboard

Interactive visualization including:

- Workflow
- Key Insights
- Charts
- Research Table
- Verification Table
- Lessons Learned

---

# Human Verification

To estimate extraction accuracy, a manual review was performed on a representative sample of **15 SaaS applications**.

The agent's output was compared against official developer documentation.

## Summary

| Metric | Value |
|---------|------:|
| Applications Reviewed | 15 |
| Fully Correct | 8 |
| Partially Correct | 7 |
| Incorrect | 0 |
| Estimated Accuracy | **86.7%** |

Examples:

| Application | Agent | Manual | Result |
|-------------|-------|--------|--------|
| Salesforce | OAuth2 | OAuth2 | ✅ Correct |
| Slack | OAuth2 | OAuth2 + Bot Token | ⚠ Partial |
| GitHub | OAuth2 | OAuth2 + Personal Access Token | ⚠ Partial |
| Stripe | API Key | API Key | ✅ Correct |
| Shopify | OAuth2 | OAuth2 | ✅ Correct |

---

# Challenges Faced

- Official documentation returning HTTP 403
- Search engines occasionally returning redirect URLs
- Missing documentation for some products
- Free LLM rate limits
- Occasional malformed JSON responses
- Inconsistent terminology across API documentation

---

# Limitations

- Some official documentation blocks automated access.
- Search engines may occasionally return irrelevant or outdated links.
- Free LLM models may produce inconsistent outputs.
- Keyword-based verification cannot fully validate semantic correctness.
- Human validation is still recommended for critical applications.

---

# Future Improvements

- Parallel processing for faster research
- Result caching
- Automatic retries with exponential backoff
- Semantic verification using embeddings
- Official API discovery through provider directories
- Better confidence scoring
- Multi-model ensemble extraction
- Scheduled dataset updates
- Export to PDF and Excel
- Database-backed storage
- REST API for the research engine

---

# Key Learnings

This project demonstrates how AI agents can automate large-scale API research while combining:

- Web search
- Documentation ranking
- LLM reasoning
- Verification
- Data analysis
- Interactive visualization

The combination of automated extraction and human verification provides a practical workflow for building reliable research pipelines.

---

# License

This project was created for the **Composio API Research Assessment** and is intended for educational and evaluation purposes.

---

# Author

**S. Pavan Kumar**

Cloud • DevOps • Python • AI Automation
