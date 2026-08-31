"""
AgroScan AI — Conversation Service
Maintains user conversation history without cross-user leakage.
"""

from typing import List, Dict, Any

class ConversationService:
    """Manages multi-turn message payload formatting and turn isolation."""

    @classmethod
    def sanitize_history(cls, raw_history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        clean_history = []
        for msg in (raw_history or [])[-8:]:
            role = "user" if msg.get("role") in ["user", "human", "sender_user"] else "assistant"
            content = str(msg.get("content", "")).strip()
            if content:
                clean_history.append({"role": role, "content": content})
        return clean_history
