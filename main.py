import os

from bot import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
# interval = "D"
# scheduler_cron_kwargs = {"hour": "*"}
scheduler_cron_kwargs = {"second": "*/2"}
interval = "60"
n_periods = 15
thresholds = (30, 60)

bot = Bot(
    bot_token=BOT_TOKEN,
    channel_id=CHANNEL_ID,
    interval=interval,
    n_periods=n_periods,
    thresholds=thresholds,
    scheduler_cron_kwargs=scheduler_cron_kwargs,
)

bot.run()
