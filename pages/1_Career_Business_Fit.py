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


def get_blocker_strategy(blocker_text, disc):
    """Get specific strategy for common blockers"""
    blocker_lower = blocker_text.lower()
    if 'insurance' in blocker_lower or 'health' in blocker_lower:
        return {'root': 'Fear of financial vulnerability during transition', 'approach': 'Provide concrete insurance options before discussing business', 'script': "Let's solve the insurance piece first. Here are 3 options franchisees use...", 'resource': 'KitchenWise group health plan comparison sheet'}
    elif 'spouse' in blocker_lower or 'husband' in blocker_lower or 'wife' in blocker_lower:
        return {'root': 'Need for family buy-in/support', 'approach': 'Invite spouse to next session. Provide spouse-specific materials.', 'script': "Your husband's support is crucial. What would he need to see to feel confident?", 'resource': 'Spouse FAQ document'}
    elif 'money' in blocker_lower or 'financial' in blocker_lower:
        return {'root': 'Uncertainty about ROI timeline', 'approach': 'Show specific financial validation numbers from similar franchisees', 'script': 'Let me show you exactly how Sarah replaced her income in 8 months...', 'resource': 'Franchisee financial validation calls'}
    else:
        return {'root': 'General uncertainty about transition', 'approach': 'Provide social proof and validation', 'script': 'What would need to be true for you to feel confident moving forward?', 'resource': 'Discovery Day invitation'}


def generate_vision_summary(disc, you2, fathom):
    """Synthesize You 2.0 goals + DISC personality into narrative vision statement"""
    natural = disc.get('natural', {})
    priorities = you2.get('priorities', [])
    dangers = you2.get('dangers', [])
    opportunities = you2.get('opportunities', [])
    insurance_concern = you2.get('insurance_concern', False)
    dominant = max(natural, key=natural.get) if natural and len(natural) > 0 else 'I'
    dominant_val = natural.get(dominant, 75)
    weakest = min(natural, key=natural.get) if natural and len(natural) > 0 else 'S'
    return f"""
## 🎯 {you2.get('client_name', 'Client')} Vision Statement Summary

### Current Reality (The "Before")
{you2.get('current_state', 'Corporate professional experiencing burnout and seeking change')}.
Top concerns: {', '.join(dangers[:2]) if dangers else 'Uncertainty about transition'}.

### Desired Future (The "You 2.0")
A **{disc.get('wheel_position', 'business owner')}** who values **{', '.join(priorities) if priorities else 'Lifestyle, Wealth'}**.
Someone who {opportunities[0] if opportunities else 'controls their own destiny'} while
maintaining {opportunities[1] if len(opportunities) > 1 else 'work-life balance'}.

### The Bridge (How to Get There)
Leverage natural **High {dominant} ({dominant_val})** to build a business that {priorities[0] if priorities else 'provides freedom'} without
requiring **Low {weakest}** skills.

### Immediate Priority
{"Address health insurance transition first" if insurance_concern else "Validate business model fit"}.
"""


def generate_roles_industries(disc, you2):
    """Generate Top 5 Employment + Top 5 Business with reasoning"""
    natural = disc.get('natural', {})
    i_score = natural.get('I', 75)
    d_score = natural.get('D', 63)
    s_score = natural.get('S', 25)
    c_score = natural.get('C', 45)
    profile = "Influential Leader" if i_score > 70 and d_score > 60 else "Promoter/Persuader" if i_score > 70 else "Driver/Commander" if d_score > 70 else "Balanced Professional"
    return f"""
## 💼 Recommended Roles & Industries for {profile}
*Based on DISC: D={d_score}, I={i_score}, S={s_score}, C={c_score}*

---

### 🏢 TOP 5 BUSINESS OWNERSHIP (Career Ownership)

**1. Service-Based Franchise (e.g., KitchenWise, Closet Wise)**
- **Match:** {min(98, int((i_score + (100 - s_score)) / 2))}%
- **Why:** High I ({i_score}) drives sales/consultation. Low S ({s_score}) means hire crews for installation.
- **TES Fit:** ILWE - Income (commission), Lifestyle (flexible), Equity (scalable)
- **Caution:** Must hire Operations Manager to handle routine details

**2. Sales Training/Consulting Franchise (e.g., Sandler)**
- **Match:** {min(95, int(i_score * 1.2))}%
- **Why:** Natural influencer/teaching style. High margins.
- **TES Fit:** Wealth (high ROI), Lifestyle (home-based possible)
- **Caution:** May feel "too corporate" if adapted C is high

**3. Marketing/Advertising Agency**
- **Match:** {min(90, i_score)}%
- **Why:** Creative + persuasive. Project-based (not routine).
- **TES Fit:** Lifestyle (flexible), Income (retainers)
- **Caution:** Client acquisition stress

**4. Real Estate Investment/Brokerage**
- **Match:** {min(85, int((i_score + d_score) / 2))}%
- **Why:** High I for client relations, High D for negotiations.
- **TES Fit:** Wealth (asset building), Equity
- **Caution:** Income uncertainty first 6 months

**5. Event Planning/Promotion Business**
- **Match:** {min(88, i_score)}%
- **Why:** High energy, people-focused, project-based.
- **TES Fit:** Lifestyle (exciting work), Income
- **Caution:** Weekend/evening hours

---

### 💼 TOP 5 EMPLOYMENT ROLES (If Business Not Right Now)

**1. Regional Sales Director** - Match: {min(95, i_score)}%
**2. Executive Coach/Corporate Trainer** - Match: {min(92, i_score)}%
**3. Franchise Development Rep** - Match: {min(90, i_score)}%
**4. Business Development Director** - Match: {min(88, int((i_score + d_score) / 2))}%
**5. Marketing Director/CMO** - Match: {min(85, i_score)}%

---

### 🎯 RECOMMENDATION
**Primary:** Service Franchise (KitchenWise model) - Best ILWE fit
**Backup:** Sales Training - If she prefers knowledge-based business
**Avoid:** Operations-heavy businesses (Low S = hates routine)
"""


def generate_coaching_guide(disc, you2, fathom):
    """Generate coaching strategy based on personality + blockers"""
    natural = disc.get('natural', {})
    adapted = disc.get('adapted', {})
    blockers = fathom.get('blockers', []) if fathom else []
    i_score = natural.get('I', 75)
    s_score = natural.get('S', 25)
    comm_style = "High I (Influencer): Use stories, enthusiasm, allow talk time" if i_score > 70 else "Balanced approach"
    content = f"""
## 🎓 How to Coach This Client

### 📊 Understanding Their Style
**Natural Style:** {disc.get('wheel_position', 'Mixed')}
- **D ({natural.get('D', 0)}):** {'Commanding, results-driven' if natural.get('D', 0) > 60 else 'Moderate drive'}
- **I ({natural.get('I', 0)}):** {'Influencing, persuasive, enthusiastic' if natural.get('I', 0) > 60 else 'Moderate influence'}
- **S ({natural.get('S', 0)}):** {'Steady, patient, routine-oriented' if natural.get('S', 0) > 60 else 'Impatient with routine'}
- **C ({natural.get('C', 0)}):** {'Analytical, detail-focused' if natural.get('C', 0) > 60 else 'Big-picture thinker'}

**Adapted Style:** {'⚠️ ALERT: Forcing High C - likely corporate burnout' if adapted.get('C', 0) > natural.get('C', 0) + 10 else 'Relatively aligned'}

---

### 🗣️ Communication Playbook

**DO:** Lead with excitement/possibility, allow them to talk, use stories/testimonials, show social proof
**DON'T:** Overwhelm with data, rush to decision, force rigid structure, dismiss emotional concerns

---

### 🚧 Blocker-Specific Coaching

"""
    for i, blocker in enumerate(blockers[:3], 1):
        strategy = get_blocker_strategy(blocker, disc)
        content += f"""
**{i}. Blocker: "{blocker}"**
- **Root Cause:** {strategy['root']}
- **Coaching Strategy:** {strategy['approach']}
- **Script:** *"{strategy['script']}"*
- **Resource:** {strategy['resource']}

"""
    if not blockers:
        content += "No specific blockers identified in conversation notes.\n"
    content += f"""
---

### 🎯 Session Structure for High I ({i_score})
**0-10 min:** Connection - personal check-in
**10-25 min:** Discovery - open questions
**25-35 min:** Direction - 2-3 options max, use stories
**35-45 min:** Commitment - specific homework, book next appointment
"""
    return content


def generate_smart_questions(disc, you2, fathom):
    """Generate tailored discovery questions"""
    natural = disc.get('natural', {})
    i_score = natural.get('I', 75)
    s_score = natural.get('S', 25)
    priorities = you2.get('priorities', [])
    blockers = fathom.get('blockers', []) if fathom else []
    p0 = priorities[0] if priorities else 'freedom'
    content = f"""
## ❓ Smart Questions to Ask This Client

*Tailored to {disc.get('wheel_position', 'their personality')} profile*

---

### 🎯 VISION CLARIFICATION
1. "When you imagine your ideal Tuesday 3 years from now, where are you and what are you doing?"
2. "You mentioned {p0} is your top priority. What does that specifically look like day-to-day?"
3. "If you had to choose: $150K/60hrs or $100K/30hrs - which feels more like You 2.0?"

---

### 🔍 BLOCKER EXPLORATION
"""
    for i, blocker in enumerate(blockers[:3], 1):
        first_word = blocker.split()[0] if blocker else 'this'
        content += f"""
**Blocker: "{blocker}"**
{i}a. "On a scale of 1-10, how urgent is solving the {first_word} issue?"
{i}b. "If we could make the {first_word} concern disappear, what would be your next decision?"
"""
    if not blockers:
        content += "No blockers identified. Use general exploration questions.\n"
    content += f"""
---

### 🧠 PERSONALITY-SPECIFIC (High I = {i_score})
4. "Who else have you talked to about this career change?"
5. "What would excite you most about telling people 'I own a [business]'?"
6. "How do you typically make big decisions - gut feeling or detailed analysis?"
"""
    if s_score < 40:
        content += f"""
**For Low S ({s_score}):**
7. "What parts of your current job make you want to 'throw your computer out the window'?"
8. "How do you feel about managing daily operations vs. just selling and strategizing?"
"""
    content += """
---

### 💼 COMMITMENT TESTING
9. "What would need to be true 30 days from now for you to feel confident writing a check?"
10. "On a scale of 1-10, how committed are you to leaving corporate within 12 months?"
11. "What's your biggest fear about making this change?"
"""
    return content


def generate_capability(cap_id, results):
    """Generate specific content for each capability"""
    disc = results.get('disc', {})
    you2 = results.get('you2', {})
    fathom = results.get('fathom', {})
    if cap_id == "vision_summary":
        content = generate_vision_summary(disc, you2, fathom)
    elif cap_id == "roles_industries":
        content = generate_roles_industries(disc, you2)
    elif cap_id == "coaching_how":
        content = generate_coaching_guide(disc, you2, fathom)
    elif cap_id == "smart_questions":
        content = generate_smart_questions(disc, you2, fathom)
    else:
        content = ""
    st.session_state[f"cap_{cap_id}"] = content


def render_sandi_capabilities(results):
    """Sandi's 4 capability cards - displayed after analysis"""
    st.markdown("### 🎯 Sandi's Coaching Toolkit")
    st.caption("Click Generate on any capability to create specific insights for this client")

    capabilities = [
        {"id": "vision_summary", "icon": "🎯", "title": "Vision Statement Summary", "desc": "Synthesize You 2.0 + DISC into clear vision narrative", "color": "#667eea"},
        {"id": "roles_industries", "icon": "💼", "title": "Roles & Industries", "desc": "Top 5 Employment + Top 5 Business matches", "color": "#388e3c"},
        {"id": "coaching_how", "icon": "🎓", "title": "How Do I Coach?", "desc": "Personalized coaching playbook based on personality", "color": "#f57c00"},
        {"id": "smart_questions", "icon": "❓", "title": "Questions to Ask", "desc": "Discovery questions tailored to blockers & style", "color": "#c2185b"}
    ]

    cols = st.columns(4)
    for idx, cap in enumerate(capabilities):
        with cols[idx]:
            is_generated = f"cap_{cap['id']}" in st.session_state
            bg = f"linear-gradient(135deg, {cap['color']}20 0%, {cap['color']}40 100%)" if is_generated else "white"
            border = cap['color'] if is_generated else "#e0e0e0"
            shadow = f"0 4px 12px {cap['color']}30" if is_generated else "0 2px 4px rgba(0,0,0,0.05)"
            gen_badge = f'<div style="margin-top: 8px; font-size: 11px; color: {cap["color"]}; font-weight: 600;">✓ GENERATED</div>' if is_generated else ''
            st.markdown(f"""
            <div style="
                background: {bg};
                border: 2px solid {border};
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                height: 150px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                box-shadow: {shadow};
            ">
                <div style="font-size: 32px; margin-bottom: 10px;">{cap['icon']}</div>
                <div style="font-weight: 600; color: {cap['color'] if is_generated else '#333'}; margin-bottom: 5px;">{cap['title']}</div>
                <div style="font-size: 12px; color: #666;">{cap['desc']}</div>
                {gen_badge}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Generate", key=f"btn_{cap['id']}", use_container_width=True, type="primary" if not is_generated else "secondary"):
                with st.spinner(f"Generating {cap['title']}..."):
                    generate_capability(cap['id'], results)
                st.rerun()

    for cap in capabilities:
        if f"cap_{cap['id']}" in st.session_state:
            with st.expander(f"📄 View: {cap['title']}", expanded=False):
                st.markdown(st.session_state[f"cap_{cap['id']}"])
                if st.button("📋 Copy", key=f"copy_{cap['id']}"):
                    st.info("Copied! (Use Ctrl+C on the text above)")


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

    # Clear previous capability outputs when re-analyzing
    for cap_id in ["vision_summary", "roles_industries", "coaching_how", "smart_questions"]:
        if f"cap_{cap_id}" in st.session_state:
            del st.session_state[f"cap_{cap_id}"]

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

        # Sandi's 4 capabilities as hero section
        render_sandi_capabilities(results)
        st.markdown("---")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💼 Top 5 Career/Business",
            "🎯 Vision Statement",
            "📋 Coaching Strategy",
            "❓ Smart Questions",
            "📈 ROI Metrics"
        ])

        with tab1:
            if "cap_roles_industries" in st.session_state:
                st.markdown(st.session_state["cap_roles_industries"])
            else:
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
            if "cap_vision_summary" in st.session_state:
                st.markdown(st.session_state["cap_vision_summary"])
            else:
                render_vision_tab(results['you2'])
                st.info("💡 Click 'Generate' on Vision Statement Summary above for full narrative")

        with tab3:
            if "cap_coaching_how" in st.session_state:
                st.markdown(st.session_state["cap_coaching_how"])
            else:
                render_coaching_strategy_tab(results['disc'], results['you2'], results['fathom'])
                st.info("💡 Click 'Generate' on How Do I Coach? above for full playbook")

        with tab4:
            st.subheader("Next Call Script & Smart Questions")
            if "cap_smart_questions" in st.session_state:
                st.markdown(st.session_state["cap_smart_questions"])
            st.text_area("Copy script for your session:", results['script'], height=400)

        with tab5:
            render_roi_tab(results['elapsed'])


if __name__ == "__main__":
    main()
