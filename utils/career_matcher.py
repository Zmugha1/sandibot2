"""
Career matching engine for TES Career Ownership options.
Maps DISC + You 2.0 to franchise recommendations with scores and warnings.
"""
from typing import Dict, List


def get_career_fits(disc_data: Dict, you2_data: Dict) -> List[Dict]:
    """
    Map DISC + You 2.0 to TES Career Ownership options
    Returns: List of career matches with scores and warnings
    """
    natural = disc_data.get('natural', {})
    adapted = disc_data.get('adapted', {})
    d = natural.get('D', 50)
    i = natural.get('I', 50)
    s = natural.get('S', 50)
    c = natural.get('C', 50)
    adapted_c = adapted.get('C', 50)

    matches = []

    # High I (Influence) + Moderate D = Sales/Leadership roles
    if i > 70 and d > 55:
        matches.append({
            'type': 'Service-Based Franchise',
            'examples': ['KitchenWise', 'Closet Wise'],
            'match_score': 94,
            'why': f'High I ({i}) perfect for customer consultation/sales. Adapted C ({adapted_c}) handles details.',
            'warnings': ['Low S (25) means will hate routine installation work'],
            'success_factors': ['Hire installer crews', 'Focus on design consultation only', 'Use High I for sales'],
            'ilwe_fit': 'Lifestyle (flexible hours), Income (commission-based)',
            'time_to_replace_income': '6-12 months'
        })

        matches.append({
            'type': 'Sales Training/Consulting',
            'examples': ['Sandler Training'],
            'match_score': 82,
            'why': 'Natural teacher/influencer. High I thrives in front of room.',
            'warnings': ['May feel "too corporate" per You 2.0', 'Low S means poor follow-up with clients'],
            'success_factors': ['Position as independent expert', 'Hire admin for scheduling/details'],
            'ilwe_fit': 'Wealth (high margins), Lifestyle (flexible)',
            'time_to_replace_income': '12-18 months'
        })

    # Low S (Steadiness) disqualifies routine-heavy businesses
    if s < 30:
        matches.append({
            'type': 'Pet Care/Daycare',
            'examples': ['Playful Pack'],
            'match_score': 65,
            'why': 'Customer-facing aspect fits High I',
            'warnings': ['⚠️ CRITICAL: Low S (25) incompatible with daily pet care routine', 'Safety concerns noted in Fathom'],
            'success_factors': ['Must hire manager for daily ops', 'Focus only on business development/marketing'],
            'ilwe_fit': 'Equity (scalable), but Lifestyle suffers initially',
            'recommendation': 'NOT RECOMMENDED without ops partner'
        })

    # Sort by match score
    matches.sort(key=lambda x: x['match_score'], reverse=True)

    # Add specific coaching notes based on You 2.0
    if you2_data.get('health_concerns'):
        for match in matches:
            match['coaching_note'] = "Address health insurance FIRST before discussing business model"

    if you2_data.get('insurance_concern'):
        for match in matches:
            match['blocker_priority'] = 1
            match['blocker_text'] = "Health insurance transition anxiety"

    return matches


def generate_coaching_script(client_name: str, disc_data: Dict, you2_data: Dict, fathom_data: Dict) -> str:
    """Generate next-call script based on parsed data"""
    natural = disc_data.get('natural', {})
    adapted = disc_data.get('adapted', {})
    i_score = natural.get('I', 50)
    c_score = adapted.get('C', 66)
    s_score = natural.get('S', 25)

    script = f"""
**Opening for {client_name}:**

"I've completed your Career Ownership analysis, and three things jumped out:

1. **THE REAL YOU**: You're naturally a Promoter/Influencer (I={i_score}) who's been 
   forcing herself into corporate analytics (C={c_score} adapted). That's exhausting.

2. **THE BLOCKER**: Health insurance is your #1 priority right now. Let's solve that 
   before we talk business models. [Reference specific insurance option].

3. **THE MATCH**: KitchenWise fits your High I for sales, but your Low S ({s_score}) means 
   you'll hate the installation work. The solution: You sell/design, hire crew for install.

Playful Pack sounds fun, but you'd be miserable in 6 months—the daily pet routine would 
   drain you. Trust the DISC on this.

**My recommendation**: Let's validate KitchenWise's group health insurance option this week. 
Are you ready to talk to their franchisee about how she handles coverage?"
"""

    return script.strip()
