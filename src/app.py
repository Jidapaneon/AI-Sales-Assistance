from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from ai_features import (
    calculate_lead_score,
    clean_crm_note,
    detect_risk,
    draft_follow_up,
    estimate_sentiment,
    openai_completion,
    summarize_meeting,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    opportunities = pd.read_csv(DATA_DIR / "sample_crm_opportunities.csv")
    transcripts = pd.read_csv(DATA_DIR / "sample_meeting_transcripts.csv")
    opportunities["lead_score"] = opportunities.apply(calculate_lead_score, axis=1)
    risks = opportunities.apply(detect_risk, axis=1)
    opportunities["risk_level"] = [risk.level for risk in risks]
    opportunities["risk_reasons"] = [", ".join(risk.reasons) for risk in risks]
    opportunities["is_stale"] = opportunities["last_activity_days"] > 14
    return opportunities, transcripts


def kpi_cards(df: pd.DataFrame) -> None:
    closed = df[df["outcome"].isin(["Won", "Lost"])]
    conversion = (closed["outcome"].eq("Won").mean() * 100) if not closed.empty else 0
    avg_response_time = 18 - 6.5
    admin_hours_saved = 8 - 4.5
    ai_usage = 72

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Lead Conversion", f"{conversion:.1f}%", "+6 pts target")
    col2.metric("Avg Response Time", f"{avg_response_time:.1f} hrs", "-6.5 hrs")
    col3.metric("Admin Time Saved", f"{admin_hours_saved:.1f} hrs/rep/wk")
    col4.metric("AI Usage", f"{ai_usage}%")


def main() -> None:
    st.set_page_config(page_title="AI Sales Assistant", layout="wide")
    st.title("AI Sales Assistant")
    st.caption("Commercial productivity demo: prioritize leads, summarize meetings, improve follow-up, and track KPI impact.")

    opportunities, transcripts = load_data()

    tab_dashboard, tab_ai, tab_business = st.tabs(["KPI Dashboard", "AI Features", "Business Case"])

    with tab_dashboard:
        kpi_cards(opportunities)

        left, right = st.columns((1.2, 1))
        with left:
            st.subheader("Prioritized Opportunities")
            st.dataframe(
                opportunities[
                    [
                        "opportunity_id",
                        "account",
                        "stage",
                        "deal_value",
                        "probability",
                        "lead_score",
                        "risk_level",
                        "risk_reasons",
                        "rep",
                    ]
                ].sort_values("lead_score", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

        with right:
            st.subheader("Pipeline Health")
            fig = px.scatter(
                opportunities,
                x="probability",
                y="deal_value",
                size="lead_score",
                color="risk_level",
                hover_name="account",
                category_orders={"risk_level": ["Low", "Medium", "High"]},
            )
            st.plotly_chart(fig, use_container_width=True)

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.subheader("Pipeline By Stage")
            stage_fig = px.bar(
                opportunities.groupby("stage", as_index=False)["deal_value"].sum(),
                x="stage",
                y="deal_value",
                text_auto=".2s",
            )
            st.plotly_chart(stage_fig, use_container_width=True)
        with chart_col2:
            st.subheader("Risk By Rep")
            risk_fig = px.histogram(opportunities, x="rep", color="risk_level", barmode="group")
            st.plotly_chart(risk_fig, use_container_width=True)

    with tab_ai:
        selected_id = st.selectbox("Choose an opportunity", transcripts["opportunity_id"])
        transcript = transcripts.loc[transcripts["opportunity_id"] == selected_id, "meeting_transcript"].iloc[0]
        opp = opportunities.loc[opportunities["opportunity_id"] == selected_id].iloc[0]

        st.subheader("Meeting Transcript")
        st.write(transcript)

        default_summary = summarize_meeting(transcript)
        ai_prompt = (
            "You are an AI sales assistant. Summarize this B2B sales meeting in 4 bullets: "
            "customer need, buying signals, risks, and next action.\n\n"
            f"Transcript: {transcript}"
        )
        llm_summary = openai_completion(ai_prompt)
        summary = llm_summary or default_summary

        left, right = st.columns(2)
        with left:
            st.subheader("AI Meeting Summary")
            st.write(summary)
            st.subheader("Sentiment")
            st.info(estimate_sentiment(transcript))
        with right:
            st.subheader("Follow-Up Email Draft")
            st.text_area(
                "Draft",
                draft_follow_up(str(opp["account"]), summary, "send the requested business case and confirm the next meeting date"),
                height=260,
            )

        st.subheader("CRM Note Cleanup")
        raw_note = st.text_area("Paste raw CRM note", transcript, height=120)
        st.code(clean_crm_note(raw_note), language="text")

    with tab_business:
        st.subheader("Use Case Canvas")
        st.markdown(
            """
| Section | Content |
| --- | --- |
| Problem | Sales reps waste time on admin and managers lack pipeline visibility. |
| AI Solution | Sales copilot for summaries, scoring, follow-up, risk detection, and CRM hygiene. |
| KPI | Conversion lift, response time reduction, admin hours saved, AI usage, pipeline health. |
| Risk | Hallucinated summaries, biased scoring, privacy exposure, poor data quality. |
| Control | Human review, confidence labels, audit trail, source-linked CRM records. |
            """
        )
        st.subheader("Architecture")
        st.markdown("CRM data + meeting notes -> Python/API layer -> AI features -> Streamlit dashboard -> rep and manager actions")
        st.subheader("Pilot Recommendation")
        st.write(
            "Start with one sales team for one quarter. Measure baseline KPIs for four weeks, enable AI features, then compare response time, conversion, CRM note quality, and admin hours."
        )


if __name__ == "__main__":
    main()
