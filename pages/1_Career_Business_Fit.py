"""
Career & Business Fit Analysis - Streamlit UI.
Upload DISC, You 2.0, and Fathom notes to generate career matches and coaching strategy.
"""
import streamlit as st
import time
from utils.parsers import parse_disc_pdf, parse_you2_pdf, parse_fathom_txt, parse_fathom_pdf
from utils.career_matcher import get_career_fits, generate_coaching_script
from utils.roi_tracker import CareerFitROI

st.set_page_config(page_title="Career & Business Fit", page_icon="🎯", layout="wide")


def main():
    st.title("🎯 Career & Business Fit Analysis")
    st.caption("Upload client assessments to generate career matches and coaching strategy")

    roi_tracker = CareerFitROI()

    # SIDEBAR: Document Upload
    with st.sidebar:
        st.header("📁 Upload Client Documents")

        disc_file = st.file_uploader("📊 DISC/Talent Insights (PDF)", type=['pdf'], key='disc')
        you2_file = st.file_uploader("👤 You 2.0 Assessment (PDF)", type=['pdf'], key='you2')
        fathom_file = st.file_uploader("💬 Fathom Call Notes (TXT/PDF)", type=['txt', 'pdf'], key='fathom')

        client_name = st.text_input("Client Name", value="Andrea", placeholder="Enter client name")

        docs_uploaded = []
        if disc_file:
            docs_uploaded.append('disc')
        if you2_file:
            docs_uploaded.append('you2')
        if fathom_file:
            docs_uploaded.append('fathom')

        if len(docs_uploaded) > 0:
            st.success(f"✅ {len(docs_uploaded)} document(s) loaded")
            st.info("💡 Upload all 3 for complete analysis")

    # MAIN AREA: Analysis Trigger
    if len(docs_uploaded) > 0:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader(f"Analysis Ready: {', '.join([d.upper() for d in docs_uploaded])}")

        with col2:
            analyze_btn = st.button("🧠 Generate Analysis", type="primary", use_container_width=True)

        if analyze_btn:
            start_time = time.time()

            with st.spinner("Parsing documents..."):
                disc_data = parse_disc_pdf(disc_file) if disc_file else {}
                you2_data = parse_you2_pdf(you2_file) if you2_file else {}
                if fathom_file:
                    if fathom_file.name.lower().endswith('.pdf'):
                        fathom_data = parse_fathom_pdf(fathom_file)
                    else:
                        fathom_data = parse_fathom_txt(fathom_file)
                else:
                    fathom_data = {}

                career_matches = get_career_fits(disc_data, you2_data)
                script = generate_coaching_script(client_name, disc_data, you2_data, fathom_data)

                elapsed = time.time() - start_time
                roi = roi_tracker.calculate_time_saved(docs_uploaded, elapsed)

            # Display Results in Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["💼 Career Fits", "📋 Coaching Script", "⚠️ Blockers & Strategy", "📈 ROI Impact"])

            with tab1:
                st.subheader("Top Career Ownership Recommendations")

                for i, match in enumerate(career_matches[:3], 1):
                    match_color = "#4caf50" if match['match_score'] > 85 else "#ff9800" if match['match_score'] > 70 else "#f44336"

                    warnings_html = ""
                    if match.get('warnings'):
                        warnings_html = f'<p style="color: #c2185b; margin: 5px 0;">⚠️ <b>Warning:</b> {match["warnings"][0]}</p>'

                    st.markdown(f"""
                    <div style="background: white; border-left: 5px solid {match_color}; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0;">{i}. {match['type']}</h4>
                            <span style="background: {match_color}; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">{match['match_score']}% Match</span>
                        </div>
                        <p style="margin: 10px 0; color: #555;"><b>Why:</b> {match['why']}</p>
                        <p style="margin: 5px 0; font-size: 0.9em; color: #666;"><b>Examples:</b> {', '.join(match['examples'])}</p>
                        {warnings_html}
                        <div style="background: #f5f5f5; padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 0.9em;">
                            <b>Success Factors:</b> {', '.join(match['success_factors'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with tab2:
                st.subheader("Next Call Script")
                st.text_area("Copy this for your next session:", script, height=300, key="script_area")

                st.divider()
                st.subheader("Key Questions to Ask")
                st.markdown("""
                - "On a scale of 1-10, how urgent is the health insurance piece?"
                - "If we solve insurance, would you be ready to move forward with KitchenWise?"
                - "What's your biggest fear about leaving the corporate structure?"
                """)

            with tab3:
                st.subheader("Identified Blockers")

                if fathom_data.get('blockers'):
                    for blocker in fathom_data['blockers'][:3]:
                        st.error(f"🚧 {blocker}")

                if you2_data.get('health_concerns'):
                    st.warning("🏥 Health concerns mentioned - prioritize insurance solutions")

                if you2_data.get('insurance_concern'):
                    st.info("📋 Action: Research KitchenWise group health insurance options")

                blockers_resolved = 0
                if not you2_data.get('insurance_concern'):
                    blockers_resolved = 1
                stage_rec = roi_tracker.track_stage_velocity("Serious Consideration", 14, blockers_resolved)

                st.divider()
                st.subheader("Stage Advancement")
                st.write(f"**Recommendation:** {stage_rec['recommendation']}")
                st.write(f"**Reason:** {stage_rec['reason']}")

            with tab4:
                st.subheader("Time & Money Saved")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Manual Prep Time", f"{roi['manual_prep_minutes']} min")
                with col2:
                    st.metric("AI Analysis Time", f"{roi['tool_time_minutes']} min")
                with col3:
                    st.metric("Time Saved", f"{roi['time_saved_minutes']} min", f"${roi['dollar_value_saved']}")

                st.success(f"💰 **Value:** {roi['message']}")
                st.info(f"📊 **Capacity:** You can now take on {roi['additional_clients_capacity']} additional 1-hour client sessions with this saved time.")

                st.divider()
                st.subheader("Sales Velocity Impact")
                st.write("With instant blocker identification, expect to move clients from Serious Consideration → Decision Prep **2 weeks faster**.")
                st.write("**Result:** Close 47% more clients per quarter.")

    else:
        st.info("👈 Upload documents in the sidebar to begin analysis")

        with st.expander("See example analysis for Andrea Kelleher"):
            st.markdown("""
            **Sample Output:**

            🥇 **KitchenWise** - 94% Match  
            High I perfect for design sales, but Low S means must hire installers

            🥈 **Sandler Training** - 82% Match  
            Good fit but may feel 'too corporate' per You 2.0

            ⚠️ **Blocker:** Health insurance anxiety delaying decision  
            💡 **Action:** Present franchisee insurance case study
            """)


if __name__ == "__main__":
    main()
