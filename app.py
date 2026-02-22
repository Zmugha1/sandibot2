"""
Sandi Bot - Career & Business Fit Analysis
Main entry point. Use the sidebar to navigate to Career & Business Fit.
"""
import streamlit as st

st.set_page_config(page_title="Sandi Bot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.title("🤖 Sandi Bot")
st.markdown("**Career & Business Fit Analysis** for The Entrepreneur's Source (TES) coaching.")
st.markdown("---")
st.info("👈 **Navigate to 'Career & Business Fit' in the sidebar** to upload client assessments and generate career matches.")
st.markdown("""
### What this does
- **DISC** → Parse TTI Success Insights reports
- **You 2.0** → Extract priorities, dangers, opportunities
- **Fathom** → Identify blockers from call notes
- **Output** → Career matches, coaching script, ROI metrics
""")
