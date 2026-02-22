"""
Career & Business Fit Analysis - TES Career Ownership Intelligence
Premium UI with document gating, visual flow, and full feature set.
"""
import streamlit as st
import time
import sys
import os
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Career & Business Fit", page_icon="🎯", layout="wide")

# TES Premium styling
st.markdown("""
<style>
    /* Purple gradient button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 20px 40px !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    .tes-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)


def check_document_completeness():
    has_disc = 'disc_bytes' in st.session_state
    has_you2 = 'you2_bytes' in st.session_state
    has_fathom = 'fathom_bytes' in st.session_state

    uploaded_count = sum([has_disc, has_you2, has_fathom])

    status = {'complete': uploaded_count == 3, 'count': uploaded_count, 'missing': []}

    if not has_disc:
        status['missing'].append("DISC Profile (Personality)")
    if not has_you2:
        status['missing'].append("You 2.0 (Goals & Values)")
    if not has_fathom:
        status['missing'].append("Fathom Notes (Conversations)")

    return status


def render_analysis_flow():
    """Visual diagram showing how 3 documents → Career Intelligence"""
    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        margin: 25px 0;
        border: 1px solid #e9ecef;
    ">
        <h4 style="margin: 0 0 20px 0; color: #333;">📊 How Your Documents Combine</h4>
        <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); flex: 1; min-width: 120px; border-top: 4px solid #667eea;">
                <strong>📊 DISC</strong>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">Personality Style<br>Natural vs Adapted</p>
            </div>
            <span style="font-size: 24px; color: #667eea;">→</span>
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); flex: 1; min-width: 120px; border-top: 4px solid #667eea;">
                <strong>👤 You 2.0</strong>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">ILWE Priorities<br>Dangers & Opportunities</p>
            </div>
            <span style="font-size: 24px; color: #667eea;">→</span>
            <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); flex: 1; min-width: 120px; border-top: 4px solid #667eea;">
                <strong>💬 Fathom</strong>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #666;">Conversation History<br>Blockers & Fears</p>
            </div>
            <span style="font-size: 24px; color: #667eea;">→</span>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; flex: 1; min-width: 120px;">
                <strong>🎯 Career Intelligence</strong>
                <p style="margin: 8px 0 0 0; font-size: 13px;">Top 5 Employment<br>Top 5 Business<br>Coaching Strategy<br>ROI Metrics</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_match_card(match, rank, color_scheme="blue"):
    """Individual match card"""
    colors = {"blue": {"border": "#1976d2"}, "green": {"border": "#388e3c"}}
    c = colors.get(color_scheme, colors["blue"])
    score = match.get('match_score', 0)
    score_color = "#4caf50" if score >= 85 else "#ff9800" if score >= 70 else "#f44336"
    warnings_html = f'<p style="margin: 5px 0; font-size: 12px; color: #c2185b;">⚠️ {match["warnings"][0]}</p>' if match.get('warnings') else ''
    st.markdown(f"""
    <div style="
        background: white;
        border-left: 4px solid {c['border']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin: 0; font-size: 16px;">#{rank} {match.get('type', 'Unknown')}</h4>
            <span style="background: {score_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 14px; font-weight: bold;">{score}%</span>
        </div>
        <p style="margin: 8px 0; font-size: 13px; color: #555;"><b>Why:</b> {match.get('why', 'No match reason')}</p>
        {warnings_html}
    </div>
    """, unsafe_allow_html=True)


def render_vision_tab(you2_data):
    """Vision Statement synthesis"""
    st.subheader("🎯 Vision Statement Synthesis")
    if you2_data:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Where They Are Now")
            st.info(you2_data.get('current_state', 'Corporate employee feeling stuck'))
            st.markdown("### Where They Want to Go")
            st.success(you2_data.get('vision_summary', 'Career Ownership with flexibility'))
        with col2:
            st.markdown("### ILWE Priorities")
            for p in you2_data.get('priorities', ['Lifestyle', 'Wealth']):
                st.write(f"• {p}")
            st.markdown("### Top 3 Dangers")
            for d in you2_data.get('dangers', ['Age discrimination', 'Health concerns']):
                st.warning(f"⚠️ {d}")
    else:
        st.info("Upload You 2.0 for vision synthesis")


def render_coaching_strategy_tab(disc_data, you2_data, fathom_data):
    """Full coaching playbook"""
    st.subheader("🎓 Personalized Coaching Strategy")
    natural = disc_data.get('natural', {}) if disc_data else {}
    if natural.get('I', 0) > 70:
        comm_style = "High I (Influencer): Lead with enthusiasm, use stories, allow them to talk"
    elif natural.get('D', 0) > 70:
        comm_style = "High D (Dominance): Lead with results, be direct, respect their time"
    else:
        comm_style = "Balanced approach needed"
    st.markdown(f"**Communication Style:** {comm_style}")
    st.markdown("### 🚧 Blocker Resolution Plan")
    blockers = fathom_data.get('blockers', []) if fathom_data else []
    for i, blocker in enumerate(blockers[:3], 1):
        st.markdown(f"**{i}. {blocker}**")
        st.markdown("- **Impact:** High (preventing stage advancement)")
        st.markdown("- **Strategy:** Address specific concern before next stage")
        st.markdown("- **Resources:** [Link to franchisee insurance case study]")


def render_roi_tab(analysis_time_seconds):
    """ROI metrics"""
    st.subheader("📈 ROI: Time & Money Saved")
    manual_time = 55
    tool_time = analysis_time_seconds / 60
    time_saved = manual_time - tool_time
    hourly_rate = 150
    money_saved = (time_saved / 60) * hourly_rate
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Manual Analysis", f"{manual_time} min")
    with col2:
        st.metric("AI Analysis", f"{tool_time:.1f} min")
    with col3:
        st.metric("Time Saved", f"{time_saved:.0f} min", f"${money_saved:.0f} value")
    with col4:
        st.metric("Stage Velocity", "2x faster", "to Decision Prep")
    st.success(f"""💰 **Value Delivered:** This analysis saved {time_saved:.0f} minutes of prep time.
    At your ${hourly_rate}/hour rate, that's ${money_saved:.0f} of billable time recovered.
    **With this efficiency, you can take on 4 additional clients per month.**""")


def run_full_analysis():
    """Execute analysis and store results"""
    from utils.parsers import parse_disc_pdf, parse_you2_pdf, parse_fathom_txt, parse_fathom_pdf
    from utils.career_matcher import get_career_fits, generate_coaching_script

    start_time = time.time()
    disc_data = {}
    you2_data = {}
    fathom_data = {}

    if 'disc_bytes' in st.session_state:
        st.session_state.disc_bytes.seek(0)
        disc_data = parse_disc_pdf(st.session_state.disc_bytes)
    if 'you2_bytes' in st.session_state:
        st.session_state.you2_bytes.seek(0)
        you2_data = parse_you2_pdf(st.session_state.you2_bytes)
    if 'fathom_bytes' in st.session_state:
        st.session_state.fathom_bytes.seek(0)
        fathom_name = st.session_state.get('fathom_name', '')
        fathom_data = parse_fathom_pdf(st.session_state.fathom_bytes) if fathom_name.lower().endswith('.pdf') else parse_fathom_txt(st.session_state.fathom_bytes)

    career_matches = get_career_fits(disc_data, you2_data)
    script = generate_coaching_script("Andrea", disc_data, you2_data, fathom_data)
    elapsed = time.time() - start_time

    st.session_state.analysis_results = {
        'disc': disc_data,
        'you2': you2_data,
        'fathom': fathom_data,
        'career_matches': career_matches,
        'script': script,
        'elapsed': elapsed
    }


def main():
    st.title("🎯 Career & Business Fit Analysis")
    st.caption("The Entrepreneur's Source — Career Ownership Intelligence")

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    # SIDEBAR: Document Upload
    with st.sidebar:
        st.header("📁 Client File Upload")
        st.markdown("*Upload all 3 for complete analysis*")

        disc = st.file_uploader("1️⃣ DISC Profile (PDF)", type=['pdf'], key='disc')
        if disc:
            st.session_state.disc_bytes = BytesIO(disc.read())
            st.session_state.disc_name = disc.name
            st.success("✅ DISC loaded")

        you2 = st.file_uploader("2️⃣ You 2.0 Assessment (PDF)", type=['pdf'], key='you2')
        if you2:
            st.session_state.you2_bytes = BytesIO(you2.read())
            st.session_state.you2_name = you2.name
            st.success("✅ You 2.0 loaded")

        fathom = st.file_uploader("3️⃣ Fathom Call Notes (TXT/PDF)", type=['txt', 'pdf'], key='fathom')
        if fathom:
            st.session_state.fathom_bytes = BytesIO(fathom.read())
            st.session_state.fathom_name = fathom.name
            st.success("✅ Fathom loaded")

        status = check_document_completeness()

        st.markdown("---")
        if status['complete']:
            st.success("✅ All documents uploaded — Ready for complete analysis")
            if st.button("🚀 Generate Complete Career Analysis", type="primary", use_container_width=True, key="analyze_btn"):
                with st.spinner("Analyzing documents..."):
                    run_full_analysis()
                st.balloons()
                st.rerun()
        else:
            st.info(f"📊 Upload Progress: {status['count']}/3 documents")
            for missing in status['missing']:
                st.warning(f"⬜ {missing}")
            st.markdown("""
            <div style="
                background: #e0e0e0;
                color: #999;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                font-size: 14px;
                border: 2px dashed #ccc;
            ">
                ⬆️ Upload all 3 documents above to enable analysis
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Upload {3 - status['count']} more document(s)")

    # MAIN AREA
    if not st.session_state.get('analysis_results'):
        render_analysis_flow()
        if not status['complete']:
            st.info("👆 Upload all 3 documents in the sidebar to see how they combine into career intelligence")
    else:
        results = st.session_state.analysis_results

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💼 Top 5 Career/Business",
            "🎯 Vision Statement",
            "📋 Coaching Strategy",
            "❓ Smart Questions",
            "📈 ROI Metrics"
        ])

        with tab1:
            employment_matches = [m for m in results['career_matches'] if m.get('category') == 'employment'][:5]
            business_matches = [m for m in results['career_matches'] if m.get('category') == 'business'][:5]

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #1976d2;">
                    <h3 style="margin: 0; color: #1976d2;">💼 TOP 5 CAREER (Employment)</h3>
                    <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">Traditional roles that fit personality</p>
                </div>
                """, unsafe_allow_html=True)
                for i, match in enumerate(employment_matches, 1):
                    render_match_card(match, i, color_scheme="blue")
            with col2:
                st.markdown("""
                <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #388e3c;">
                    <h3 style="margin: 0; color: #388e3c;">🏢 TOP 5 BUSINESS (Ownership)</h3>
                    <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">Franchise/entrepreneur options for Career Ownership</p>
                </div>
                """, unsafe_allow_html=True)
                for i, match in enumerate(business_matches, 1):
                    render_match_card(match, i, color_scheme="green")

        with tab2:
            render_vision_tab(results['you2'])

        with tab3:
            render_coaching_strategy_tab(results['disc'], results['you2'], results['fathom'])

        with tab4:
            st.subheader("Next Call Script & Smart Questions")
            st.text_area("Copy for your session:", results['script'], height=400)

        with tab5:
            render_roi_tab(results['elapsed'])


if __name__ == "__main__":
    main()
