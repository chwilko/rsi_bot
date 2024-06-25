import os

from bot import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")

scheduler_cron_kwargs = {"hour": "*"}
interval = "120"
n_periods = 14
thresholds = (30, 70)

bot = Bot(
    bot_token=BOT_TOKEN,
    channel_id=CHANNEL_ID,
    interval=interval,
    n_periods=n_periods,
    thresholds=thresholds,
    scheduler_cron_kwargs=scheduler_cron_kwargs,
)

bot.run()
