import logging
from time import process_time, time
from typing import Dict, Optional, Tuple, Union

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from bot.bybit_kline_data_fetcher import BybitKlineDataFetcher
from bot.rsi_counter import relative_strength_index

bot_logger = logging.getLogger(__name__)


class Bot:
    def __init__(
        self,
        bot_token: str,
        channel_id: Union[int, str],
        interval: str,
        n_periods: int,
        scheduler_cron_kwargs: Optional[Dict],
        thresholds: Tuple[int, int] = (30, 70),
    ) -> None:
        """Class implements a Discord bot . 
        The bot is designed to analyze data from [bybit]
        (https://www.bybit.com/trade/usdt/SOLUSDT).
        It calculates the relative strength index (RSI)
        and if the index is not within the specified range,
        it sends information about it on the specified channel on discord.

        Args:
            bot_token (str): discord bot token
            channel_id (Union[int, str]): The id of the channel on discord
                for sending messages by the bot.
            interval (str): RSI period. See supported periods in ReadPriceHelper.INTERVALS.
            n_periods (int): Number of periods to count the RSI.
            scheduler_cron_kwargs (Optional[Dict]): Kwargs for the scheduler
                from the APScheduler library in cron mode. Defaults to {"minute": "*"}
            thresholds (Tuple[int, int], optional): Thresholds for RSI indicator.
                Order does not matter. Defaults to (30, 70).

        Raises:
            AttributeError: Error will be raised if n_periods <= 1.
        """
        if n_periods <= 1:
            raise AttributeError("The number of periods must be greater than 1.")
        self.bot_token = bot_token
        self.channel_id = int(channel_id)
        self.interval = interval
        self.n_periods = n_periods
        self.lower_threshold = min(thresholds)
        self.upper_threshold = max(thresholds)
        self.scheduler_cron_kwargs = scheduler_cron_kwargs or {"minute": "*"}

    def _check_rsi(self):
        """Method with bot logic.
        This method get data, count relative_strength_index and
        decide about send message.
        """
        start = process_time()
        helper = BybitKlineDataFetcher(interval=self.interval)
        now = int(time() * 1000)
        data = helper.get_intervals_by_periods(end=now, periods=self.n_periods)
        rsi = round(
            relative_strength_index(
                data=data, close_key="closePrice", order_key="startTime"
            ),
            5,
        )
        if rsi <= self.lower_threshold:
            message = f"RSI: {rsi} smaller than {self.lower_threshold}"
        elif rsi >= self.upper_threshold:
            message = f"RSI: {rsi} greater than {self.upper_threshold}"
        else:
            bot_logger.info(msg=f"check_rsi end. RSI: {rsi} is in the interval.")
            return

        self._send_message(message)
        end = process_time()
        bot_logger.info(msg=f"check_rsi end. Message sent in {end - start} seconds.")

    def _send_message(self, message: str):
        """Method use discord API to send message via bot

        Args:
            message (str): message to send via bot
        """
        url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }
        data = {"content": message}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            bot_logger.error(f"HTTP error: {err}")
        except Exception as err:
            bot_logger.error(f"Error in send message: {err}")

    def run(self):
        """Run bot with scheduler"""
        scheduler = BlockingScheduler()

        scheduler.add_job(
            self._check_rsi,
            "cron",
            id="check_rsi",
            **self.scheduler_cron_kwargs,
        )
        scheduler.start()

    def run_simple(self):
        """Run the bot once"""
        self._check_rsi()
