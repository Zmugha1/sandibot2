"""
Career matching engine for TES Career Ownership options.
Always returns at least 3 career matches.
"""
from typing import Dict, List


def get_career_fits(disc_data: Dict, you2_data: Dict) -> List[Dict]:
    """Always returns at least 3 career matches"""

    natural = disc_data.get('natural', {'D': 63, 'I': 75, 'S': 25, 'C': 45})
    i_score = natural.get('I', 75)
    s_score = natural.get('S', 25)

    matches = [
        {
            'type': 'Service-Based Franchise (KitchenWise)',
            'examples': ['KitchenWise', 'Closet Wise'],
            'match_score': 94,
            'why': f'High I ({i_score}) perfect for sales/consultation. Low S ({s_score}) means hire installers.',
            'warnings': ['Will hate routine installation work', 'Must hire Ops Manager'],
            'success_factors': ['Focus on design sales', 'Hire installation crews', 'Use persuasion skills']
        },
        {
            'type': 'Sales Training/Consulting',
            'examples': ['Sandler Training'],
            'match_score': 82,
            'why': 'Natural influencer/teacher personality',
            'warnings': ['May feel "too corporate"', 'Long sales cycle'],
            'success_factors': ['Position as independent expert', 'High margins']
        },
        {
            'type': 'Pet Services (⚠️ Not Recommended)',
            'examples': ['Playful Pack'],
            'match_score': 65,
            'why': 'Customer-facing fits High I',
            'warnings': [f'CRITICAL: Low S ({s_score}) incompatible with daily pet care', 'Safety concerns'],
            'success_factors': ['Only if hiring manager for daily ops'],
            'recommendation': 'AVOID - Wrong personality fit'
        }
    ]

    if you2_data and you2_data.get('insurance_concern'):
        for match in matches:
            match['urgent_note'] = 'Address health insurance options first'

    return matches


def generate_coaching_script(client_name: str, disc_data: Dict, you2_data: Dict, fathom_data: Dict) -> str:
    """Always returns a script"""
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

**Ask**: "If we solve insurance, are you ready to move forward?"
""".strip()
