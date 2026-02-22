"""
Ollama integration for local LLM synthesis.
Optional - rule-based analysis works without it.
"""
import streamlit as st
from typing import Optional

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    ollama = None


def synthesize_with_ollama(disc_text: str, you2_text: str, fathom_text: str) -> str:
    """Use local Llama 3.1 to synthesize insights (air-gapped)"""
    if not OLLAMA_AVAILABLE or ollama is None:
        return "Ollama not installed. Install with: pip install ollama"

    prompt = f"""
You are a career coach analyzing client data for The Entrepreneur's Source.

DISC Profile: {disc_text[:1000]}

You 2.0 Assessment: {you2_text[:800]}

Recent Conversation Notes: {fathom_text[:1000]}

Provide:
1. The single biggest blocker preventing this client from moving forward
2. Which franchise option best fits their personality (and why)
3. One specific question to ask on the next call

Keep response under 150 words.
"""

    try:
        response = ollama.generate(
            model='llama3.1:8b',
            prompt=prompt,
            options={'temperature': 0.3, 'num_predict': 200}
        )
        return response.get('response', 'No response')
    except Exception as e:
        return f"Ollama offline: {str(e)}"


def check_ollama_status() -> bool:
    """Check if Ollama is running locally"""
    if not OLLAMA_AVAILABLE:
        st.sidebar.warning("⚠️ Ollama not installed. pip install ollama")
        return False
    try:
        ollama.list()
        return True
    except Exception:
        st.sidebar.error("⚠️ Ollama not running. Start with: `ollama serve`")
        return False
