# 2OrderBook.py

import asyncio
import aiohttp

from exchanges import Binance, Coinbase
from analytics import get_volume_imbalance, plot_depth
from cache import DepthCache
from monitoring import logger


async def stream_order_books(symbols):
    binance = Binance()
    coinbase = Coinbase()

    depth_cache = DepthCache(symbols)

    binance_endpoint = await binance.get_depth_endpoint()
    coinbase_endpoint = await coinbase.get_depth_endpoint()

    async with aiohttp.ClientSession() as session:
        binance_task = asyncio.create_task(binance.depth_stream(session, binance_endpoint, handle_depth))
        coinbase_task = asyncio.create_task(coinbase.depth_stream(session, coinbase_endpoint, handle_depth))

        await asyncio.gather(binance_task, coinbase_task)


async def handle_depth(depth):
    symbol = depth['symbol']

    depth_cache.update(symbol, depth)

    imbalance = get_volume_imbalance(depth)

    logger.info(f"{symbol} bid-ask volume imbalance: {imbalance:.2f}")

    plot_depth(symbol, depth)


# Initialize
symbols = ['BTCUSDT', 'ETHUSD']
loop = asyncio.get_event_loop()
loop.run_until_complete(stream_order_books(symbols))