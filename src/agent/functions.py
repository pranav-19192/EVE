from livekit.agents import Agent
from livekit.agents import function_tool, RunContext
from .prompts import SYSTEM_PROMPT

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions = SYSTEM_PROMPT,
        )

    