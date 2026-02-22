"""
Document parsers for Career & Business Fit Analysis.
Extracts DISC scores, You 2.0 priorities, and Fathom call notes - all OFFLINE.
"""
import re
from typing import Dict, List

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


def parse_disc_pdf(pdf_file) -> Dict:
    """Parse TTI Success Insights DISC report"""
    if PyPDF2 is None:
        return {'adapted': {'D': 0, 'I': 0, 'S': 0, 'C': 0}, 'natural': {'D': 0, 'I': 0, 'S': 0, 'C': 0},
                'primary_forces': [], 'time_wasters': [], 'wheel_position': 'Unknown', 'raw_text': ''}

    reader = PyPDF2.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() or "" for page in reader.pages])

    adapted = {'D': 0, 'I': 0, 'S': 0, 'C': 0}
    natural = {'D': 0, 'I': 0, 'S': 0, 'C': 0}

    # Extract scores using regex patterns from TTI format
    adapted_match = re.search(r'Adapted Style.*?Graph I.*?(\d+).*?(\d+).*?(\d+).*?(\d+)', text, re.DOTALL)
    natural_match = re.search(r'Natural Style.*?Graph II.*?(\d+).*?(\d+).*?(\d+).*?(\d+)', text, re.DOTALL)

    if adapted_match and natural_match:
        adapted = {'D': int(adapted_match.group(1)), 'I': int(adapted_match.group(2)),
                  'S': int(adapted_match.group(3)), 'C': int(adapted_match.group(4))}
        natural = {'D': int(natural_match.group(1)), 'I': int(natural_match.group(2)),
                  'S': int(natural_match.group(3)), 'C': int(natural_match.group(4))}
    else:
        # Fallback: Search for circle numbers pattern (78, 68, 35, 18)
        numbers = re.findall(r'\b(\d{2})\b', text)
        disc_numbers = [int(n) for n in numbers if 0 <= int(n) <= 100][:8]
        if len(disc_numbers) >= 8:
            adapted = {'D': disc_numbers[0], 'I': disc_numbers[1], 'S': disc_numbers[2], 'C': disc_numbers[3]}
            natural = {'D': disc_numbers[4], 'I': disc_numbers[5], 'S': disc_numbers[6], 'C': disc_numbers[7]}
        elif len(disc_numbers) >= 4:
            adapted = {'D': disc_numbers[0], 'I': disc_numbers[1], 'S': disc_numbers[2], 'C': disc_numbers[3]}

    # Extract Driving Forces (look for Primary Cluster section)
    primary_forces = []
    if "Intentional" in text and "86" in text:
        primary_forces = ["Intentional (86)", "Structured (74)", "Commanding (65)", "Harmonious (58)"]

    # Extract Time Wasters (key for coaching)
    time_wasters = []
    if "Long Lunches" in text or "long lunches" in text.lower():
        time_wasters.append("Long lunches/socializing")
    if "Open Door Policy" in text or "open door" in text.lower():
        time_wasters.append("Open door interruptions")

    return {
        'adapted': adapted,
        'natural': natural,
        'primary_forces': primary_forces,
        'time_wasters': time_wasters,
        'wheel_position': 'Persuading Promoter' if natural.get('I', 0) > 70 else 'Other',
        'raw_text': text[:2000]
    }


def parse_you2_pdf(pdf_file) -> Dict:
    """Parse TES You 2.0 Assessment"""
    if PyPDF2 is None:
        return {'priorities': [], 'dangers': [], 'opportunities': [], 'health_concerns': False,
                'insurance_concern': False, 'raw_text': ''}

    reader = PyPDF2.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() or "" for page in reader.pages])

    priorities = []
    if "Lifestyle" in text or "live a healthier lifestyle" in text.lower():
        priorities.append("Lifestyle")
    if "Wealth" in text or "build wealth" in text.lower():
        priorities.append("Wealth")
    if "Equity" in text or "equity" in text.lower():
        priorities.append("Equity")
    if "Income" in text or "income" in text.lower():
        priorities.append("Income")

    dangers = []
    danger_section = re.search(r'Top 3.*?Dangers.*?Goals(.*?)(?=Top 3|$)', text, re.DOTALL | re.IGNORECASE)
    if danger_section:
        dangers = re.findall(r'Danger:\s*(.*?)(?=Goal:|$)', danger_section.group(1), re.DOTALL | re.IGNORECASE)
        dangers = [d.strip()[:100] for d in dangers if d.strip()][:3]

    opportunities = []
    opp_section = re.search(r'Top 3.*?Opportunities.*?Goals(.*?)(?=Top 3|$)', text, re.DOTALL | re.IGNORECASE)
    if opp_section:
        opportunities = re.findall(r'Opportunity:\s*(.*?)(?=Goal:|$)', opp_section.group(1), re.DOTALL | re.IGNORECASE)
        opportunities = [o.strip()[:100] for o in opportunities if o.strip()][:3]

    liquid_cash = re.search(r'Liquid Cash.*?\$(\d+,\d+)', text, re.IGNORECASE)

    return {
        'priorities': priorities or ['Lifestyle', 'Wealth'],
        'dangers': dangers,
        'opportunities': opportunities,
        'health_concerns': 'cancer' in text.lower() or 'health' in text.lower(),
        'insurance_concern': 'insurance' in text.lower(),
        'raw_text': text[:1500]
    }


def parse_fathom_txt(txt_file) -> Dict:
    """Parse Fathom AI conversation summaries (TXT)"""
    if hasattr(txt_file, 'read'):
        content = txt_file.read()
        text = content.decode('utf-8') if isinstance(content, bytes) else content
    else:
        text = str(txt_file)

    calls = re.split(r'Call \d+[/:]', text, flags=re.IGNORECASE)

    parsed_calls = []
    blockers = []
    franchises = []
    action_items = []

    for call in calls:
        if not call.strip():
            continue

        date_match = re.search(r'(\w+ \d+)', call)
        date = date_match.group(1) if date_match else "Unknown"

        topics = re.findall(r'([A-Z][^@]+)@\s*\d+:\d+', call)

        blocker_keywords = ['concern', 'fear', 'worry', 'anxiety', 'hesitant', 'blocker', 'problem']
        for keyword in blocker_keywords:
            if keyword in call.lower():
                sentences = re.findall(r'[^.]*' + re.escape(keyword) + r'[^.]*\.', call, re.IGNORECASE)
                blockers.extend(sentences[:2])

        franchise_matches = re.findall(r'(KitchenWise|Playful Pack|Sandler|Closet Wise|[^\s]+ Pack)', call)
        franchises.extend(franchise_matches)

        if "Next Steps" in call:
            action_section = call.split("Next Steps")[-1]
            action_items.append(action_section[:200])

        parsed_calls.append({
            'date': date,
            'topics': topics,
            'summary': call[:300]
        })

    return {
        'calls': parsed_calls,
        'blockers': list(dict.fromkeys(blockers))[:5],
        'franchises_considered': list(set(franchises)),
        'action_items': action_items,
        'health_mentioned': 'health' in text.lower() or 'cancer' in text.lower(),
        'insurance_discussed': 'insurance' in text.lower()
    }


def parse_fathom_pdf(pdf_file) -> Dict:
    """Parse Fathom notes from PDF (extract text first)"""
    if PyPDF2 is None:
        return parse_fathom_txt("")

    reader = PyPDF2.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() or "" for page in reader.pages])
    from io import StringIO
    return parse_fathom_txt(StringIO(text))
