import requests
from agno.agent.agent import Agent, RunResponse
from agno.media import Audio, File, Image, Video
from agno.utils.log import log_info, log_warning
from os import getenv
from typing import Optional, Union

try:
    import discord
except (ImportError, ModuleNotFoundError):
    print("`discord.py` not installed. Please install using `pip install discord.py`")

class RequiresConfirmationView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.primary)
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        self.value = True
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.clear_items()
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        self.value = False
        button.disabled = True
        await interaction.response.edit_message(view=self)
        self.clear_items()
        self.stop()

    async def on_timeout(self):
        log_warning("Agent Timeout Error")

class DiscordClient:
    def __init__(self, agent: Optional[Agent] = None, agent_prefix: str = "!"):
        self.agent = agent
        self.agent_prefix = agent_prefix
        self.intents = discord.Intents.all()
        self.client = discord.Client(intents=self.intents)

        self._setup_events()

    def _setup_events(self):
        @self.client.event
        async def on_message(context):
            if context.author == self.client.user:
                return

            message_image = None
            message_video = None
            message_audio = None
            message_file = None
            media_url = None
            message_text = context.content
            message_url = context.jump_url
            message_user = context.author.name
            message_user_id = context.author.id
            replied_message = None

            message_prefix = message_text.split(' ', 1)[0]
            if message_prefix.lower() == self.agent_prefix.lower():
                message_text = message_text.replace(f"{message_prefix} ", "", 1)
            else:
                return

            if context.reference and context.reference.message_id:
                replied_message = await context.channel.fetch_message(context.reference.message_id)
                message_text = f"{replied_message.content}\n{message_text}"

            if context.attachments:
                media = context.attachments[0]
                media_type = media.content_type
                media_url = media.url
                if media_type.startswith("image/"):
                    message_image = media_url
                elif media_type.startswith("video/"):
                    req = requests.get(media_url)
                    video = req.content
                    message_video = video
                elif media_type.startswith("application/"):
                    req = requests.get(media_url)
                    document = req.content
                    message_file = document
                elif media_type.startswith("audio/"):
                    message_audio = media_url

            log_info(f"processing message:{message_text} \n with media: {media_url} \n url:{message_url}")
            if isinstance(context.channel, discord.Thread):
                thread = context.channel
            elif isinstance(context.channel, discord.channel.DMChannel):
                thread = context.channel
            elif isinstance(context.channel, discord.TextChannel):
                if "open thread" in message_text:
                    thread = await context.create_thread(name=f"{message_user}'s thread")
                else:
                    thread = context.channel
            else:
                log_info(f"received {context.content} but not in a supported channel")
                return

            async with thread.typing():
                if self.agent:
                    self.agent.additional_context = f"Discord username: {message_user}"
                    agent_response: RunResponse = await self.agent.arun(
                        message_text,
                        user_id=message_user_id,
                        session_id=str(thread.id),
                        images=[Image(url=message_image)] if message_image else None,
                        videos=[Video(content=message_video)] if message_video else None,
                        audio=[Audio(url=message_audio)] if message_audio else None,
                        files=[File(content=message_file)] if message_file else None,
                    )

                    if isinstance(agent_response, RunResponse):
                        agent_response = await self._handle_hitl(agent_response, thread)
                    
                    await self._send_message(thread=thread, message=str(agent_response.content), replied_message=replied_message)

    async def _handle_hitl(self, run_response: RunResponse, thread: Union[discord.Thread, discord.TextChannel]) -> RunResponse:
        if run_response.is_paused:
            for tool in run_response.tools_requiring_confirmation:
                view = RequiresConfirmationView()
                await thread.send(f"Tool requiring confirmation: {tool.tool_name}", view=view)
                await view.wait()
                tool.confirmed = view.value if view.value is not None else False

            if self.agent:
                run_response = await self.agent.acontinue_run(run_response=run_response)

        return run_response

    async def _send_message(self, thread: discord.channel, message: str, replied_message = None):
        if replied_message:
            return await replied_message.reply(message)

        return await thread.send(message)

    def serve(self):
        try:
            token = getenv("DISCORD_TOKEN")
            if not token:
                raise ValueError("DISCORD_TOKEN NOT SET")
            return self.client.run(token)
        except Exception as e:
            raise ValueError(f"Failed to run Discord client: {str(e)}")
