import asyncio
from cryptocmd import Binance, Coinbase
from cachetools import TTLCache
from monitoring import logger

cache = TTLCache(maxsize=10, ttl=60)

def get_api_client(exchange):
    # Return the appropriate API client for the given exchange
    if exchange == 'Binance':
        return Binance(API_KEY)
    elif exchange == 'Coinbase':
        return Coinbase(API_KEY)
    else:
        raise ValueError(f"Unknown exchange: {exchange}")

async def execute_order(exchange, order):
    if cache.get(order['id']):
        logger.info(f"Cached order: {order['id']}")
        return

    api_client = get_api_client(exchange)

    result = None
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

# Usage (replace with actual order objects)
btc_order, eth_order, ltc_order, bch_order = {}, {}, {}, {}
portfolio = {'Binance': [btc_order, eth_order],
             'Coinbase': [ltc_order, bch_order]}

loop = asyncio.get_event_loop()
loop.run_until_complete(rebalance_portfolio(portfolio))
