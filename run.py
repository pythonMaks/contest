import os
import django
import asyncio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contest.settings')
django.setup()

async def run_bot():
    from users.bots.tg_bot import main
    await main()

if __name__ == '__main__':
    asyncio.run(run_bot())