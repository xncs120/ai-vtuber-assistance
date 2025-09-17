import os
from abc import ABC, abstractmethod
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from core.configs import configs

class BaseAgent(ABC):
    def __init__(self, ai_model, agent_id, session_id, user_id=configs.OWNER_USERNAME):
        self.ai_model = ai_model
        self.agent_id = agent_id
        self.session_id = session_id
        self.user_id = user_id

        self.sqlite_path = os.path.join(configs.APP_STORAGE_DIR, "db", f"{self.agent_id}.db")
        self.sqlite_db = SqliteDb(
            id=self.agent_id,
            db_file=self.sqlite_path,
            session_table="agent_sessions",
            memory_table="agent_memories",
        )

        self.agent = None

    @abstractmethod
    def _get_instructions(self):
        return []

    @abstractmethod
    def _get_tools(self):
        return []

    def get_agent(self):
        self.agent = Agent(
            model=self.ai_model,
            id=self.agent_id,
            name=self.agent_id,
            session_id=self.session_id,
            user_id=self.user_id,
            db=self.sqlite_db,
            add_history_to_context=True,
            num_history_runs=20,
            enable_agentic_memory=True,
            enable_user_memories=True,
            instructions=self._get_instructions(),
            tools=self._get_tools(),
            markdown=True,
        )
        return self.agent
