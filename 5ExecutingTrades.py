# 5ExecutingTrades.py

import asyncio
from cryptocmd import Binance, Coinbase
from cachetools import TTLCache
from monitoring import logger

cache = TTLCache(maxsize=10, ttl=60)


async def execute_order(exchange, order):
    if cache.get(order['id']):
        logger.info(f"Cached order: {order['id']}")
        return

    api_client = get_api_client(exchange)

    try:
        result = await api_client.place_order(order)
        cache[order['id']] = result
        logger.info(f"Order placed: {result}")

    except Exception as e:
        logger.error(f"Order failed: {e}")

    return result


async def rebalance_portfolio(weights):
    tasks = []
    for exchange, orders in weights.items():
        for order in orders:
            task = asyncio.create_task(execute_order(exchange, order))
            tasks.append(task)

    await asyncio.gather(*tasks)


# Usage
portfolio = {'Binance': [btc_order, eth_order],
             'Coinbase': [ltc_order, bch_order]}

loop = asyncio.get_event_loop()
loop.run_until_complete(rebalance_portfolio(portfolio))