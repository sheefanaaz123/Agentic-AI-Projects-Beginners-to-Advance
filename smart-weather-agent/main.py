
"""Streamlit UI for the Smart Weather & Travel Assistant."""

from datetime import date
import json

import streamlit as st
from pydantic import ValidationError

from agent import generate_travel_advice
from schemas import TravelRequest


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Weather & Travel Assistant",
    page_icon="🌦️",
    layout="wide",
)

st.title("🌦️ Smart Weather & Travel Assistant")

st.write(
    "Get weather-based packing suggestions, outdoor activity "
    "guidance, and travel safety considerations."
)


# --------------------------------------------------
# Input form
# --------------------------------------------------

with st.form("travel_form"):
    st.subheader("Plan your trip")

    city = st.text_input(
        "Destination",
        placeholder="e.g. Manali",
        max_chars=120,
    )

    travel_date = st.date_input(
        "Travel date",
        value=date.today(),
        min_value=date.today(),
    )

    interests_text = st.text_input(
        "Activities or interests",
        placeholder="e.g. sightseeing, hiking, photography",
    )

    submitted = st.form_submit_button(
        "Generate Travel Advice",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# Agent execution
# --------------------------------------------------

if submitted:
    interests = [
        item.strip()
        for item in interests_text.split(",")
        if item.strip()
    ]

    try:
        request = TravelRequest(
            city=city,
            travel_date=travel_date,
            interests=interests,
        )

    except ValidationError as exc:
        st.error("Please correct the following input errors.")
        st.code(str(exc))

    else:
        with st.spinner(
            "Fetching weather and generating travel advice..."
        ):
            try:
                report = generate_travel_advice(request)

            except Exception:
                # Keep internal exception details out of the UI.
                st.error(
                    "Unable to generate travel advice. "
                    "Check the API configuration and try again."
                )

            else:
                st.session_state["travel_report"] = (
                    report.model_dump(mode="json")
                )


# --------------------------------------------------
# Render the report
# --------------------------------------------------

report_data = st.session_state.get("travel_report")

if report_data:
    st.divider()

    st.header(
        f"Travel report: {report_data['destination']}"
    )

    st.caption(
        f"Travel date: {report_data['travel_date']}"
    )

    weather = report_data["weather"]

    st.subheader("Weather forecast")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Minimum temperature",
            (
                f"{weather['temperature_min_c']} °C"
                if weather["temperature_min_c"] is not None
                else "Unavailable"
            ),
        )

    with col2:
        st.metric(
            "Maximum temperature",
            (
                f"{weather['temperature_max_c']} °C"
                if weather["temperature_max_c"] is not None
                else "Unavailable"
            ),
        )

    with col3:
        st.metric(
            "Rain probability",
            (
                f"{weather['precipitation_probability_percent']}%"
                if weather[
                    "precipitation_probability_percent"
                ] is not None
                else "Unavailable"
            ),
        )

    st.write(
        "**Conditions:**",
        weather["weather_description"],
    )

    st.caption(
        f"Weather source: {weather['source']}"
    )

    st.divider()

    st.subheader("🧳 Packing list")

    for item in report_data["packing_list"]:
        st.checkbox(item, key=f"packing_{item}")

    st.subheader("🌄 Outdoor activity assessment")

    st.write(
        report_data["outdoor_activity_assessment"]
    )

    st.subheader("Activities to consider")

    for activity in report_data["suggested_activities"]:
        st.markdown(f"- {activity}")

    st.subheader("⚠️ Safety considerations")

    for item in report_data["safety_considerations"]:
        st.markdown(f"- {item}")

    st.subheader("Travel summary")

    st.write(report_data["overall_summary"])

    st.info(report_data["confidence_note"])

    with st.expander("View structured JSON"):
        st.json(report_data)

    st.download_button(
        label="Download travel report (JSON)",
        data=json.dumps(
            report_data,
            indent=2,
            ensure_ascii=False,
        ),
        file_name="travel_advice.json",
        mime="application/json",
    )