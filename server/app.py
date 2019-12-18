import asyncio

from services.utils import update_teams


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(update_teams())
    try:
        loop.run_forever()
    finally:
        loop.close()
