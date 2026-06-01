# AI Sales Assistant

Purpose: show how AI improves commercial team productivity by helping sales teams save time, prioritize leads, improve follow-up, and increase conversion.

## Scenario

You are advising a B2B sales organization where reps manually summarize meetings, leads are not consistently prioritized, managers lack pipeline visibility, and CRM notes vary in quality.

## Deliverables

- [Executive summary](docs/executive_summary.md)
- [AI use case canvas](docs/ai_use_case_canvas.md)
- [Stakeholder map](docs/stakeholder_map.md)
- [Pain points and process flow](docs/process_flow.md)
- [KPI baseline](docs/kpi_baseline.md)
- [Architecture diagram](docs/architecture.md)
- [Public data source options](docs/data_sources.md)
- Streamlit KPI dashboard and AI feature demo in [src/app.py](src/app.py)

## AI Features In Scope

- Meeting summarizer
- Lead scoring
- Email drafting assistant
- Opportunity risk detection
- CRM note cleanup

The app uses deterministic demo logic by default. If `OPENAI_API_KEY` is set, the text-generation features can call the OpenAI API.

## Quick Start

```bash
cd "ai-sales-assistant"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

Optional:

```bash
export OPENAI_API_KEY="your_key_here"
```

## Project Story

The project demonstrates a practical AI sales copilot: CRM data flows into Python, AI features generate summaries and recommendations, and the dashboard tracks conversion, time saved, response time, AI usage, and pipeline health.
