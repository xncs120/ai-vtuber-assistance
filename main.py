import asyncio
import os
from core.agents.mao import Mao
from core.agents.tamamo import Tamamo
from core.agents.vivy import Vivy
from core.configs import configs

mao = Mao().get_agent()
tamamo = Tamamo().get_agent()
vivy = Vivy().get_agent()

processes = []
serves = [item.strip() for item in configs.APP_SERVES.split(",") if item.strip()]

for serve in serves:
    if serve == "api":
        from agno.os import AgentOS
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import FileResponse
        from fastapi.staticfiles import StaticFiles

        agent_os = AgentOS(
            os_id="agentos",
            description="AgentOS",
            agents=[mao, tamamo],
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

        processes.append(asyncio.to_thread(agent_os.serve, app="main:app", reload=False))

    if serve == "discord":
        from core.facades.discord_client import DiscordClient
        discord_agent = DiscordClient(agent=vivy, agent_prefix="vv")
        processes.append(asyncio.to_thread(discord_agent.serve))

async def main():
    await asyncio.gather(*processes)

if __name__ == "__main__":
    asyncio.run(main())
