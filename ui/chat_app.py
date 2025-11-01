import json
import os
import sys
import time

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.langgraph_orchestrator import run_orchestrator

st.set_page_config(
    page_title="Social Support AI Application",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Social Support Application")
st.markdown(
    "Upload your documents below and our system will automatically check your information, "
    "assess eligibility for financial or economic support, and provide recommendations."
)

uploaded_files = st.file_uploader(
    "📎 Upload your PDF documents here", type=["pdf"], accept_multiple_files=True
)

st.markdown("---")

if st.button("🚀 Start Processing"):
    if uploaded_files:
        # Save uploaded PDFs temporarily
        file_paths = []
        for f in uploaded_files:
            temp_path = f"temp_{f.name}"
            with open(temp_path, "wb") as out_file:
                out_file.write(f.read())
            file_paths.append(temp_path)

        # -----------------------------
        # Status Bar & Progress Bar
        # -----------------------------
        status_bar = st.container()
        status_cols = status_bar.columns(4)
        stage_labels = ["Data Extraction", "Validation", "Eligibility Check", "AI Recommendation"]

        # Placeholders for each stage
        stage_placeholders = [col.empty() for col in status_cols]

        # Progress bar
        progress = st.progress(0)


        # Function to update stage status and progress
        def update_stage(index, done=False):
            icon = "✅" if done else "⏳"
            stage_placeholders[index].markdown(f"{icon} {stage_labels[index]}")
            progress.progress(int(((index + 1) / len(stage_labels)) * 100))


        # -----------------------------
        # Workflow Stages
        # -----------------------------
        update_stage(0, done=False)
        results = run_orchestrator(file_paths)
        update_stage(0, done=True)
        time.sleep(0.5)

        update_stage(1, done=False)
        time.sleep(0.5)
        update_stage(1, done=True)

        update_stage(2, done=False)
        time.sleep(0.5)
        update_stage(2, done=True)

        update_stage(3, done=False)
        time.sleep(0.5)
        update_stage(3, done=True)

        st.success("🎉 Your application has been processed successfully!")

        # AI Recommendation - user-friendly wording
        with st.expander("🧠 View AI Recommendations"):
            decision_raw = results.get("decision", {})
            recommendation_text = decision_raw.get("recommendation", "{}")

            parsed = None
            if isinstance(recommendation_text, dict):
                parsed = recommendation_text
            elif isinstance(recommendation_text, str):
                # Remove 'json\n' prefix if present
                if recommendation_text.lower().startswith("json"):
                    recommendation_text = recommendation_text.split("\n", 1)[-1]
                try:
                    parsed = json.loads(recommendation_text.strip())
                except json.JSONDecodeError:
                    try:
                        parsed = json.loads(recommendation_text.replace("\n", ""))
                    except Exception:
                        st.warning("⚠️ Could not interpret AI recommendations. Showing raw response:")
                        st.text(recommendation_text)

            if parsed:
                decision_value = parsed.get('financial_support_decision', 'N/A')
                color = "green" if decision_value.lower() == "approve" else "red"
                st.markdown(f"### Decision: <span style='color:{color}'>{decision_value}</span>",
                            unsafe_allow_html=True)

                reasoning_text = parsed.get('reasoning', 'No reasoning provided.')
                st.markdown(f"**Reason:** {reasoning_text}")

                suggestions = parsed.get("economic_enablement_suggestions", [])
                if suggestions:
                    st.markdown("**Recommended Actions / Opportunities:**")
                    for s in suggestions:
                        st.markdown(f"- {s}")
                else:
                    st.markdown("**Recommended Actions / Opportunities:** None")

        st.markdown("---")

    else:
        st.warning("⚠️ Please upload at least one PDF to start processing.")
