import asyncio
from datetime import datetime
from models.log_class import LogCLassAll
from models.start_class import StartBot


from bot import *  # noqa: F403
    
async def main():
    LogCLassAll().info("Start logging")
    # await init_models()
    # await add_scheduler_default()
    bot = StartBot()
    await bot.run()
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LogCLassAll().error(f"script interrupted: {datetime.now()}")
    except Exception as e:
        LogCLassAll().error(f"Bug: \n {e}")