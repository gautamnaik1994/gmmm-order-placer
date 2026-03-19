from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import asyncio
import logging

from aioclock import AioClock, At, Depends, Every, Forever, Once
from aioclock.group import Group

import login as login
import send_telegram 
import order_placer
from logging_setup import configure_logging


from typing import TypedDict


logger = logging.getLogger(__name__)

class UtcTime(TypedDict):
    hour: int
    minute: int

def ist_to_utc(ist_hour: int, ist_minutes: int) -> UtcTime:
    utc_hour = ist_hour - 5
    utc_minutes = ist_minutes - 30

    if utc_minutes < 0:
        utc_minutes += 60
        utc_hour -= 1

    if utc_hour < 0:
        utc_hour += 24

    return {
        "hour": utc_hour,
        "minute": utc_minutes,
    }


group = Group()

utc_time = ist_to_utc(8, 30)
@group.task(trigger=At(tz="UTC", hour=utc_time["hour"], minute=utc_time["minute"], second=0))
async def health_check():
    send_telegram.send_message("✅ Health check successful!")
    logger.info("Health check successful!")


utc_time = ist_to_utc(8, 45)
@group.task(trigger=At(tz="UTC", hour=utc_time["hour"], minute=utc_time["minute"], second=0))
async def login_task():
    login.fyers_login()
    send_telegram.send_message("✅ Login successful!")
    logger.info("Logged in successfully!")


utc_time = ist_to_utc(8, 50)
@group.task(trigger=At(tz="UTC", hour=utc_time["hour"], minute=utc_time["minute"], second=0))
async def place_order():
    order_placer.fetch_orders()
    order_placer.place_orders()
    send_telegram.send_message("✅ Signals fetched successfully!")
    logger.info("Signals fetched successfully!")

@group.task(trigger=At(tz="UTC", hour=9, minute=45, second=0, at="every friday"))
async def place_order_friday():
    order_placer.fetch_orders()
    order_placer.place_orders()
    # order_placer.fetch_and_place_orders()
    send_telegram.send_message("✅ Order placed successfully!")
    logger.info("Order placed successfully!")




@asynccontextmanager
async def lifespan(aio_clock: AioClock) -> AsyncGenerator[AioClock]:
    logger.info("Starting up. Remember, if your code is running, you better go catch it!")
    send_telegram.send_message("🚀 Bot is starting up!")
    yield aio_clock
    logger.info("Going offline. Remember, if your code is running, you better go catch it!")
    send_telegram.send_message("🛑 Bot is going offline!")


# app.py
app = AioClock(lifespan=lifespan)
app.include_group(group)



# main.py
if __name__ == "__main__":
    configure_logging()
    try:
        asyncio.run(app.serve())
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
