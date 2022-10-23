import asyncio
import aioschedule
from Moodle import make_calendar, send_calendar

file_name = "calendar.ics"


async def updater():
    if await make_calendar.make(file_name):
        await send_calendar.send()


async def scheduler():
    aioschedule.every().minute.do(updater)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_start(_):
    asyncio.create_task(scheduler())
