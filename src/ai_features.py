from __future__ import annotations

import os
import re
from dataclasses import dataclass


@dataclass
class OpportunityRisk:
    level: str
    reasons: list[str]


def summarize_meeting(transcript: str) -> str:
    if not transcript:
        return "No transcript provided."

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", transcript) if s.strip()]
    highlights = sentences[:3]
    next_step = next((s for s in sentences if "next" in s.lower() or "follow-up" in s.lower()), None)
    summary = " ".join(highlights)
    if next_step and next_step not in summary:
        summary = f"{summary} Next action: {next_step}"
    return summary


def draft_follow_up(account: str, meeting_summary: str, next_action: str) -> str:
    return (
        f"Subject: Follow-up from our discussion\n\n"
        f"Hi {account} team,\n\n"
        f"Thank you for the conversation. My understanding is: {meeting_summary}\n\n"
        f"As a next step, I will {next_action.lower()}.\n\n"
        f"Best,\n"
        f"Sales Team"
    )


def clean_crm_note(raw_note: str) -> str:
    if not raw_note:
        return "Summary: No note available.\nNext step: Confirm buyer context.\nRisk: Unknown."

    normalized = " ".join(raw_note.split())
    return (
        f"Summary: {normalized}\n"
        "Next step: Confirm owner, due date, and buyer decision criteria.\n"
        "Risk: Review for missing stakeholder, timing, or competitor details."
    )


def calculate_lead_score(row) -> int:
    score = 0
    score += min(float(row["deal_value"]) / 2500, 40)
    score += float(row["probability"]) * 30
    score += min(int(row["meetings_count"]) * 3, 15)
    score += min(int(row["email_opens"]), 10)
    score += min(int(row["decision_makers"]) * 2, 10)
    score -= min(int(row["last_activity_days"]) * 1.5, 25)
    if str(row["competitor_present"]).lower() == "yes":
        score -= 8
    return int(max(0, min(score, 100)))


def detect_risk(row) -> OpportunityRisk:
    reasons: list[str] = []
    if int(row["last_activity_days"]) > 14:
        reasons.append("No recent activity")
    if str(row["competitor_present"]).lower() == "yes":
        reasons.append("Competitor present")
    if str(row["crm_note_quality"]).lower() in {"missing", "messy"}:
        reasons.append("CRM notes need cleanup")
    if float(row["probability"]) < 0.35 and str(row["stage"]).lower() not in {"qualification", "discovery"}:
        reasons.append("Low probability for current stage")

    if len(reasons) >= 3:
        return OpportunityRisk("High", reasons)
    if reasons:
        return OpportunityRisk("Medium", reasons)
    return OpportunityRisk("Low", ["Healthy activity pattern"])


def estimate_sentiment(text: str) -> str:
    positive_terms = {"liked", "confirmed", "budget", "urgency", "available", "reduce", "wants"}
    negative_terms = {"concerns", "blocker", "competitor", "legal", "privacy", "slow", "risk"}
    words = set(re.findall(r"[a-zA-Z]+", text.lower()))
    score = len(words & positive_terms) - len(words & negative_terms)
    if score > 1:
        return "Positive"
    if score < 0:
        return "Cautious"
    return "Neutral"


def openai_completion(prompt: str) -> str | None:
    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
            temperature=0.2,
        )
        return response.output_text
    except Exception as exc:
        return f"OpenAI call unavailable: {exc}"
