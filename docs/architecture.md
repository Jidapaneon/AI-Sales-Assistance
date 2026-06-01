# Architecture Diagram

```mermaid
flowchart LR
    A["CRM / Sales Pipeline Data"] --> B["Python Data Processing"]
    C["Meeting Notes / Transcripts"] --> B
    B --> D["AI Feature Layer"]
    D --> E["Meeting Summary"]
    D --> F["Lead Score"]
    D --> G["Email Draft"]
    D --> H["Risk Detection"]
    D --> I["CRM Note Cleanup"]
    E --> J["Streamlit KPI Dashboard"]
    F --> J
    G --> J
    H --> J
    I --> J
    J --> K["Sales Rep Actions"]
    J --> L["Manager Visibility"]
```

## Component View

| Component | Role |
| --- | --- |
| CRM data | Opportunity, account, activity, deal stage, and outcome information. |
| Python/API layer | Cleans data, calculates KPIs, calls AI functions, and prepares dashboard tables. |
| LLM layer | Generates summaries, follow-up recommendations, email drafts, sentiment, and note cleanup. |
| Dashboard | Shows conversion, time saved, AI usage, pipeline risk, and priority opportunities. |
| Human review | Sales reps approve summaries and email drafts before CRM or customer use. |
