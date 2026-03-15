from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import asyncio

from aioclock import AioClock, At, Depends, Every, Forever, Once
from aioclock.group import Group

import login as login
import send_telegram 
import signals_fetcher

group = Group()


@group.task(trigger=At(tz="UTC", hour=0, minute=0, second=0))
async def login_task():
    login.fyers_login()
    print("Logged in successfully!")

@group.task(trigger=At(tz="UTC", hour=0, minute=0, second=0))
async def place_order():
    signals_fetcher.fetch_signals()
    print("Signals fetched successfully!")








@asynccontextmanager
async def lifespan(aio_clock: AioClock) -> AsyncGenerator[AioClock]:
    # starting up
    print(
        "Welcome to the Async Chronicles! Did you know a group of unicorns is called a blessing? Well, now you do!"
    )
    yield aio_clock
    # shuting down
    print("Going offline. Remember, if your code is running, you better go catch it!")


# app.py
app = AioClock(lifespan=lifespan)
app.include_group(group)



# main.py
if __name__ == "__main__":
    asyncio.run(app.serve())
