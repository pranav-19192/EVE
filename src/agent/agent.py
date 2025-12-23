from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import(
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    room_io
)
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from .functions import Assistant

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

# Initialise the server and prewarm function
server = AgentServer()
def prewarm(proc: JobProcess):
    proc.userdata['vad'] = silero.VAD.load()
server.setup_fnc = prewarm

@server.rtc_session()
async def agent(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name
    }

    session = AgentSession(
        stt = inference.STT(
            model="cartesia/ink-whisper",
            language="en"
        ),
        llm=inference.LLM(
            model="google/gemini-2.5-flash",
            extra_kwargs={
                'max_completion_tokens': 1024
            }
        ),
        tts=inference.TTS(
            model="cartesia/sonic-3", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata['vad'],
        preemptive_generation=True,
    )

    await session.start(
        agent = Assistant(),
        room = ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
            ),
        )
    )

    await ctx.connect()

    session.say("Hello, how are you doing today?")

if __name__ == '__main__':
    cli.run_app(server)