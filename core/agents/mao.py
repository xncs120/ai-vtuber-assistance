from .base_agent import BaseAgent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools

class Mao(BaseAgent):
    def __init__(self, model="gemini-2.5-flash", session_id="", user_id=None):
        super().__init__(
            ai_model=Gemini(id=model, max_output_tokens=1000),
            agent_id="Mao",
            session_id=session_id,
            user_id=user_id,
        )

    def _get_instructions(self):
        return ["You are Mao, a magical girl vtuber."]

    def _get_tools(self):
        return [DuckDuckGoTools(all=True)]
