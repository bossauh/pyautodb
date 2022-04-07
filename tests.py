import asyncio
from tests import TestDatabase
from colorama import init
init()


async def main():
    await TestDatabase().run()


asyncio.run(main())
