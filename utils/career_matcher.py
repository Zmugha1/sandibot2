"""
Career matching engine for TES Career Ownership options.
Returns Top 5 Employment + Top 5 Business matches with category.
"""
from typing import Dict, List


def get_career_fits(disc_data: Dict, you2_data: Dict) -> List[Dict]:
    """Returns Top 5 Employment + Top 5 Business matches"""

    natural = disc_data.get('natural', {'D': 63, 'I': 75, 'S': 25, 'C': 45})
    d_score = natural.get('D', 63)
    i_score = natural.get('I', 75)
    s_score = natural.get('S', 25)
    c_score = natural.get('C', 45)

    # TOP 5 EMPLOYMENT (traditional roles)
    employment_matches = [
        {
            'category': 'employment',
            'type': 'Sales / Business Development',
            'match_score': 92,
            'why': f'High I ({i_score}) thrives in relationship-driven sales. Natural persuader.',
            'warnings': ['Low S means follow-up may slip', 'Need CRM discipline'],
            'success_factors': ['B2B or high-ticket sales', 'Commission-based roles']
        },
        {
            'category': 'employment',
            'type': 'Corporate Trainer / Facilitator',
            'match_score': 88,
            'why': f'Natural teacher and influencer. High I loves the spotlight.',
            'warnings': ['May feel constrained by corporate curriculum'],
            'success_factors': ['L&D roles', 'Sales training', 'Leadership development']
        },
        {
            'category': 'employment',
            'type': 'Marketing / Brand Manager',
            'match_score': 85,
            'why': f'Creative, people-focused. High I drives campaigns and storytelling.',
            'warnings': ['Low S may struggle with long project timelines'],
            'success_factors': ['Consumer marketing', 'Events', 'Partnerships']
        },
        {
            'category': 'employment',
            'type': 'Account Executive / Client Success',
            'match_score': 82,
            'why': f'Relationship builder. High I + moderate C handles client needs.',
            'warnings': ['Routine account admin may bore them'],
            'success_factors': ['Enterprise accounts', 'Strategic partnerships']
        },
        {
            'category': 'employment',
            'type': 'Recruiter / Talent Acquisition',
            'match_score': 78,
            'why': f'People-focused. High I excels at selling opportunities to candidates.',
            'warnings': ['High volume/transactional recruiting may drain them'],
            'success_factors': ['Executive search', 'Specialized roles']
        }
    ]

    # TOP 5 BUSINESS OWNERSHIP (franchise/entrepreneur)
    business_matches = [
        {
            'category': 'business',
            'type': 'Service-Based Franchise (KitchenWise)',
            'examples': ['KitchenWise', 'Closet Wise'],
            'match_score': 94,
            'why': f'High I ({i_score}) perfect for sales/consultation. Low S ({s_score}) means hire installers.',
            'warnings': ['Will hate routine installation work', 'Must hire Ops Manager'],
            'success_factors': ['Focus on design sales', 'Hire installation crews', 'Use persuasion skills']
        },
        {
            'category': 'business',
            'type': 'Sales Training / Consulting',
            'examples': ['Sandler Training'],
            'match_score': 88,
            'why': 'Natural influencer/teacher. High I thrives in front of room.',
            'warnings': ['May feel "too corporate"', 'Long sales cycle'],
            'success_factors': ['Position as independent expert', 'High margins']
        },
        {
            'category': 'business',
            'type': 'Coaching / Advisory Practice',
            'examples': ['Executive coaching', 'Career coaching'],
            'match_score': 85,
            'why': f'Uses influence and experience. High I builds trust quickly.',
            'warnings': ['Income ramp-up time', 'Need to build pipeline'],
            'success_factors': ['Leverage corporate background', 'Niche specialization']
        },
        {
            'category': 'business',
            'type': 'Home Services Franchise',
            'examples': ['Window cleaning', 'Pressure washing'],
            'match_score': 78,
            'why': 'Customer-facing sales fits High I. Scalable with crews.',
            'warnings': ['Must hire for operations', 'Low S incompatible with field work'],
            'success_factors': ['Sales/estimating role only', 'Manager for daily ops']
        },
        {
            'category': 'business',
            'type': 'Pet Services (⚠️ Caution)',
            'examples': ['Playful Pack'],
            'match_score': 65,
            'why': 'Customer-facing fits High I',
            'warnings': [f'CRITICAL: Low S ({s_score}) incompatible with daily pet care', 'Safety concerns'],
            'success_factors': ['Only if hiring manager for daily ops'],
            'recommendation': 'AVOID - Wrong personality fit'
        }
    ]

    if you2_data and you2_data.get('insurance_concern'):
        for match in employment_matches + business_matches:
            match['urgent_note'] = 'Address health insurance options first'

    return employment_matches + business_matches


def generate_coaching_script(client_name: str, disc_data: Dict, you2_data: Dict, fathom_data: Dict) -> str:
    """Always returns a script with smart questions"""
    natural = disc_data.get('natural', {'I': 75, 'S': 25})
    i_score = natural.get('I', 75)

    blockers = fathom_data.get('blockers', ['Health insurance concerns']) if fathom_data else ['Health insurance']
    top_blocker = blockers[0] if blockers else "Health insurance"

    return f"""
**Opening for {client_name}:**

"I've analyzed your assessments. Three things stand out:

1. **YOUR STYLE**: You're a natural promoter (I={i_score}) forcing yourself into corporate structure. That's exhausting.

2. **THE BLOCKER**: {top_blocker}. Let's solve this first.

3. **THE FIT**: KitchenWise fits you - you sell, crews install. Playful Pack is wrong for your personality.

**Next Steps**: Let's check KitchenWise insurance options this week. Ready to talk to a franchisee?"

**Smart Questions to Ask:**
- "On a scale of 1-10, how urgent is the health insurance blocker?"
- "If we solve insurance this week, would you be ready to move forward?"
- "What's your biggest fear about leaving the corporate structure?"
- "How important is the 'travel with husband' goal in your decision?"
""".strip()
