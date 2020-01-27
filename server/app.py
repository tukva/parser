import asyncio

from services.utils import create_teams, create_real_teams


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(create_teams())
    loop.create_task(create_real_teams())
    try:
        loop.run_forever()
    finally:
        loop.close()
