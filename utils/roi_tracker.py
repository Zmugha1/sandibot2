"""
ROI tracker for Career & Business Fit Analysis.
Calculates time saved vs manual prep and stage velocity.
"""
from typing import Dict


class CareerFitROI:
    def __init__(self):
        self.baseline_prep_time = 55  # minutes (manual review)
        self.coach_hourly_rate = 150

    def calculate_time_saved(self, documents_uploaded: list, analysis_time_seconds: float) -> Dict:
        """Calculate ROI for using the tool vs manual prep"""

        # Manual time per document type
        manual_times = {
            'disc': 20,
            'you2': 10,
            'fathom': 15
        }

        total_manual = sum([manual_times.get(doc, 5) for doc in documents_uploaded])
        tool_time = analysis_time_seconds / 60

        time_saved = total_manual - tool_time

        return {
            'manual_prep_minutes': total_manual,
            'tool_time_minutes': round(tool_time, 1),
            'time_saved_minutes': round(time_saved, 1),
            'dollar_value_saved': round((time_saved / 60) * self.coach_hourly_rate, 2),
            'additional_clients_capacity': round(time_saved / 60, 1),
            'message': f"You saved {round(time_saved)} minutes. That's ${round((time_saved/60)*self.coach_hourly_rate, 0)} of your time back."
        }

    def track_stage_velocity(self, current_stage: str, days_in_stage: int, blockers_resolved: int) -> Dict:
        """Predict stage advancement based on analysis"""

        if blockers_resolved >= 2 and current_stage == "Serious Consideration":
            return {
                'recommendation': 'ADVANCE to Decision Prep',
                'reason': '2 major blockers (insurance, franchise selection) addressed',
                'expected_close_date': '2 weeks faster than manual process',
                'confidence': 'High'
            }
        elif blockers_resolved >= 1:
            return {
                'recommendation': 'STAY in Serious Consideration',
                'reason': f'{blockers_resolved}/3 blockers resolved',
                'next_action': 'Resolve remaining blocker to advance'
            }
        else:
            return {
                'recommendation': 'DEEPER Discovery needed',
                'reason': 'Blockers not yet identified/resolved'
            }
