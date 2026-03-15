from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import asyncio

from aioclock import AioClock, At, Depends, Every, Forever, Once
from aioclock.group import Group

import login as login
import send_telegram 
import order_placer

group = Group()


@group.task(trigger=At(tz="UTC", hour=3, minute=15, second=0))
async def login_task():
    login.fyers_login()
    send_telegram.send_message("Login successful!")
    print("Logged in successfully!")

@group.task(trigger=At(tz="UTC", hour=3, minute=45, second=0))
async def place_order():
    # order_placer.fetch_signals()
    send_telegram.send_message("Signals fetched successfully!")
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
