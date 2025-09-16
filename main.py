import os
from agno.os import AgentOS
from core.agents.mao import Mao
from core.configs import configs
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

mao = Mao().get_agent()

agent_os = AgentOS(
    os_id="agentos",
    description="AgentOS",
    agents=[mao],
)

app = agent_os.get_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists('ui/dist'):
    app.mount("/", StaticFiles(directory="ui/dist", html=True), name="static")
    @app.get("/")
    async def serve_vue_app():
        return FileResponse("ui/dist/index.html")
else:
    print("Frontend ui build [ui/dist] does not exist, please use pnpm dev")

if __name__ == "__main__":
    agent_os.serve("main:app", reload=True)
