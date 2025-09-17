from .base_agent import BaseAgent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
# from core.tools.tts_rvc import TtsRvcTools

class Tamamo(BaseAgent):
    def __init__(self, model="gemini-2.5-flash", session_id="", user_id=None):
        super().__init__(
            ai_model=Gemini(id=model, max_output_tokens=1000),
            agent_id="Tamamo",
            session_id=session_id,
            user_id=user_id,
        )

    def _get_instructions(self):
        return [
            "You are a sexy and mature foxgirl miko vtuber named Tamamo(Tama-san).",
            "You love to flirt and tease people.",
            # "Always use synthesize tool on your response."
        ]

    def _get_tools(self):
        # return [DuckDuckGoTools(all=True), TtsRvcTools()]
        return [DuckDuckGoTools(all=True)]