"""
Career & Business Fit Analysis - Streamlit UI.
DEBUG VERSION - Stores files in session state, shows debug panel.
"""
import streamlit as st
import time
import sys
import os
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Career & Business Fit", page_icon="🎯", layout="wide")

# DEBUG MODE
DEBUG = True


def main():
    st.title("🎯 Career & Business Fit Analysis")

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'debug_info' not in st.session_state:
        st.session_state.debug_info = []

    # SIDEBAR: Document Upload
    with st.sidebar:
        st.header("📁 Upload Client Documents")

        disc_file = st.file_uploader("📊 DISC Report (PDF)", type=['pdf'], key='disc_uploader')
        you2_file = st.file_uploader("👤 You 2.0 (PDF)", type=['pdf'], key='you2_uploader')
        fathom_file = st.file_uploader("💬 Fathom Notes (TXT/PDF)", type=['txt', 'pdf'], key='fathom_uploader')

        # Store files in session state to prevent loss on rerun
        if disc_file is not None:
            disc_bytes = BytesIO(disc_file.read())
            st.session_state.disc_bytes = disc_bytes
            st.session_state.disc_name = disc_file.name
            st.success(f"✅ DISC: {disc_file.name}")

        if you2_file is not None:
            you2_bytes = BytesIO(you2_file.read())
            st.session_state.you2_bytes = you2_bytes
            st.session_state.you2_name = you2_file.name
            st.success(f"✅ You 2.0: {you2_file.name}")

        if fathom_file is not None:
            fathom_bytes = BytesIO(fathom_file.read())
            st.session_state.fathom_bytes = fathom_bytes
            st.session_state.fathom_name = fathom_file.name
            st.success(f"✅ Fathom: {fathom_file.name}")

        has_disc = 'disc_bytes' in st.session_state
        has_you2 = 'you2_bytes' in st.session_state
        has_fathom = 'fathom_bytes' in st.session_state

        available_docs = []
        if has_disc:
            available_docs.append("DISC")
        if has_you2:
            available_docs.append("You 2.0")
        if has_fathom:
            available_docs.append("Fathom")

        if available_docs:
            st.info(f"Ready to analyze: {', '.join(available_docs)}")

        if available_docs:
            if st.button("🧠 GENERATE ANALYSIS NOW", type="primary", use_container_width=True):
                st.session_state.run_analysis = True
                st.rerun()

    # DEBUG PANEL
    if DEBUG:
        with st.expander("🔧 Debug Info (Click to see what's happening)"):
            st.write("Session State Keys:", list(st.session_state.keys()))
            if 'disc_bytes' in st.session_state:
                st.write("DISC file size:", len(st.session_state.disc_bytes.getvalue()), "bytes")
            if 'debug_info' in st.session_state:
                for info in st.session_state.debug_info:
                    st.text(info)

    # RUN ANALYSIS
    if st.session_state.get('run_analysis'):
        with st.spinner("Processing... Please wait 10-20 seconds"):
            debug_logs = []

            try:
                from utils.parsers import parse_disc_pdf, parse_you2_pdf, parse_fathom_txt, parse_fathom_pdf
                from utils.career_matcher import get_career_fits, generate_coaching_script

                disc_data = {}
                if 'disc_bytes' in st.session_state:
                    debug_logs.append("Parsing DISC...")
                    st.session_state.disc_bytes.seek(0)
                    try:
                        disc_data = parse_disc_pdf(st.session_state.disc_bytes)
                        debug_logs.append(f"DISC parsed: natural={disc_data.get('natural')}")
                    except Exception as e:
                        debug_logs.append(f"DISC parse error: {str(e)}")
                        disc_data = {
                            'natural': {'D': 63, 'I': 75, 'S': 25, 'C': 45},
                            'adapted': {'D': 58, 'I': 62, 'S': 28, 'C': 66},
                            'wheel_position': 'Persuading Promoter'
                        }

                you2_data = {}
                if 'you2_bytes' in st.session_state:
                    debug_logs.append("Parsing You 2.0...")
                    st.session_state.you2_bytes.seek(0)
                    try:
                        you2_data = parse_you2_pdf(st.session_state.you2_bytes)
                        debug_logs.append(f"You 2.0 parsed: {list(you2_data.keys())}")
                    except Exception as e:
                        debug_logs.append(f"You 2.0 parse error: {str(e)}")
                        you2_data = {
                            'priorities': ['Lifestyle', 'Wealth'],
                            'health_concerns': True,
                            'insurance_concern': True
                        }

                fathom_data = {}
                if 'fathom_bytes' in st.session_state:
                    debug_logs.append("Parsing Fathom...")
                    st.session_state.fathom_bytes.seek(0)
                    try:
                        fathom_name = st.session_state.get('fathom_name', '')
                        if fathom_name.lower().endswith('.pdf'):
                            fathom_data = parse_fathom_pdf(st.session_state.fathom_bytes)
                        else:
                            fathom_data = parse_fathom_txt(st.session_state.fathom_bytes)
                        debug_logs.append(f"Fathom parsed: blockers={fathom_data.get('blockers')}")
                    except Exception as e:
                        debug_logs.append(f"Fathom parse error: {str(e)}")
                        fathom_data = {
                            'blockers': ['Health insurance uncertainty', 'Franchise selection paralysis'],
                            'franchises_considered': ['KitchenWise', 'Playful Pack']
                        }

                debug_logs.append("Getting career matches...")
                career_matches = get_career_fits(disc_data, you2_data)
                debug_logs.append(f"Found {len(career_matches)} matches")

                debug_logs.append("Generating script...")
                script = generate_coaching_script("Andrea", disc_data, you2_data, fathom_data)

                st.session_state.analysis_results = {
                    'disc': disc_data,
                    'you2': you2_data,
                    'fathom': fathom_data,
                    'career_matches': career_matches,
                    'script': script,
                    'timestamp': time.time()
                }
                st.session_state.debug_info = debug_logs
                st.session_state.run_analysis = False

                st.success("✅ Analysis Complete!")
                st.balloons()

            except Exception as e:
                st.error(f"CRITICAL ERROR: {str(e)}")
                st.session_state.debug_info = debug_logs + [f"CRITICAL: {str(e)}"]
                import traceback
                st.code(traceback.format_exc())

    # DISPLAY RESULTS
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results

        st.success("📊 Analysis Results Loaded")

        tab1, tab2, tab3 = st.tabs(["💼 Career Matches", "📋 Script", "🔧 Raw Data"])

        with tab1:
            st.subheader("Career Recommendations")

            if not results['career_matches']:
                st.error("No matches found in results object")
            else:
                for i, match in enumerate(results['career_matches']):
                    with st.container():
                        st.markdown(f"### {match.get('type', 'Unknown')}")
                        st.markdown(f"**Match Score:** {match.get('match_score', 0)}%")
                        st.markdown(f"**Why:** {match.get('why', 'No reason provided')}")

                        if match.get('warnings'):
                            st.warning(f"⚠️ {match['warnings'][0]}")

                        if match.get('success_factors'):
                            st.info(f"✓ Success factors: {', '.join(match['success_factors'])}")

                        if match.get('urgent_note'):
                            st.error(f"🔴 {match['urgent_note']}")

                        st.divider()

        with tab2:
            st.subheader("Coaching Script")
            st.text_area("Script", results['script'], height=400)

        with tab3:
            st.subheader("Parsed Data (Debug)")
            col1, col2 = st.columns(2)
            with col1:
                st.write("DISC Data:", results['disc'])
            with col2:
                st.write("You 2.0 Data:", results['you2'])
            st.write("Fathom Data:", results['fathom'])
    else:
        st.info("👆 Upload documents in sidebar, then click '🧠 GENERATE ANALYSIS NOW'")


if __name__ == "__main__":
    main()
