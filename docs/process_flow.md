# Pain Points And Process Flow

## Pain Points

| Pain Point | Business Impact | AI Feature |
| --- | --- | --- |
| Reps manually summarize meetings. | Less selling time and delayed follow-up. | Meeting summarizer. |
| Leads are not prioritized consistently. | High-value opportunities may be missed. | Lead scoring. |
| Managers lack visibility into stale or risky deals. | Forecast risk and missed coaching moments. | Opportunity risk detection. |
| CRM notes are inconsistent. | Poor handoffs and unreliable reporting. | CRM note cleanup. |
| Follow-up emails take too long to write. | Slower response time and weaker buyer experience. | Email drafting assistant. |

## Current Process

```mermaid
flowchart LR
    A["Sales meeting"] --> B["Rep writes manual notes"]
    B --> C["Rep updates CRM when time allows"]
    C --> D["Manager reviews inconsistent CRM data"]
    D --> E["Follow-up may be delayed"]
    E --> F["Opportunity progresses or stalls"]
```

## Future AI-Assisted Process

```mermaid
flowchart LR
    A["Sales meeting"] --> B["Transcript or notes captured"]
    B --> C["AI summarizes meeting and extracts next steps"]
    C --> D["AI updates structured CRM note draft"]
    D --> E["Lead score and risk flag refreshed"]
    E --> F["Rep reviews follow-up email draft"]
    F --> G["Manager monitors KPI dashboard"]
```
