import os
import sys

import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.langgraph_orchestrator import run_orchestrator

st.title("Social Support Application AI Workflow")

uploaded_files = st.file_uploader(
    "Upload Applicant PDFs", type=["pdf"], accept_multiple_files=True
)

if st.button("Process Application"):
    if uploaded_files:
        # Save uploaded PDFs to temp folder to pass paths
        file_paths = []
        for f in uploaded_files:
            temp_path = f"temp_{f.name}"
            with open(temp_path, "wb") as out_file:
                out_file.write(f.read())
            file_paths.append(temp_path)

        results = run_orchestrator(file_paths)

        st.subheader("Extracted Data")
        st.json(results["extracted_data"])

        st.subheader("Validation Results")
        st.json(results["validation"])

        st.subheader("Eligibility Assessment")
        st.json(results["eligibility"])

        st.subheader("Decision Recommendation")
        st.json(results["decision"])
    else:
        st.warning("Please upload at least one PDF.")
