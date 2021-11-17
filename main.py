import asyncio
from pytgcalls import idle
from helper.syntax import call_py, bot

async def video_bot():
    print("[INFO]: STARTING BOT CLIENT")
    await bot.start()
    print("[INFO]: STARTING PYTGCALLS CLIENT")
    await call_py.start()
    await idle()
    print("[INFO]: STOPPING BOT")
    await bot.stop()

loop = asyncio.get_event_loop()
loop.run_until_complete(video_bot())
