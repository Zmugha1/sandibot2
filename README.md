# Sandi Bot 2 - Career & Business Fit Analysis

Career & Business Fit Analysis Module for The Entrepreneur's Source (TES) coaching. Analyzes DISC assessments, You 2.0 forms, and Fathom call notes to generate career matches and coaching strategies.

## Features

- **Document Parsers** (offline): Extract DISC scores, You 2.0 priorities/dangers, Fathom blockers
- **Career Matcher**: Maps High I/Low S profiles to KitchenWise, Sandler, Playful Pack with warnings
- **Coaching Script Generator**: Next-call scripts based on parsed data
- **ROI Tracker**: 55 min manual → ~5 min tool = $112 saved per client at $150/hr
- **Ollama Integration** (optional): Local LLM synthesis when `ollama serve` is running

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then navigate to **Career & Business Fit** in the sidebar.

## File Structure

```
sandibot2/
├── app.py                    # Main entry
├── pages/
│   └── 1_Career_Business_Fit.py
├── utils/
│   ├── parsers.py            # PDF/TXT extraction
│   ├── career_matcher.py     # DISC → Career mapping
│   ├── roi_tracker.py       # Time saved metrics
│   └── ai_synthesis.py      # Ollama (optional)
└── requirements.txt
```

## Andrea Kelleher Example

- **DISC**: Natural I=75, D=63, S=25, C=45 | Adapted I=62, D=58, S=28, C=66
- **You 2.0**: Lifestyle/Health insurance priority, age discrimination fear
- **Fathom**: Health insurance blocker, KitchenWise vs Playful Pack vs Sandler

**Result**: KitchenWise 94% match (hire installers), Playful Pack NOT recommended (Low S + safety).
