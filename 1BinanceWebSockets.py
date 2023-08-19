# 1BinanceWebSockets.py
import asyncio
import aiohttp
from cryptocmd import Binance, Coinbase

from utils import WebSocketHandler, PortfolioManager
from processed import process_stream_data
from monitoring import logger, MetricsCollector

api_keys = {
  'binance': API_KEY,
  'coinbase': COINBASE_KEY
}

portfolio = PortfolioManager()
metrics = MetricsCollector()

async def start_sockets(symbols):

  ws_handler = WebSocketHandler()

  binance = Binance(api_keys['binance'])
  coinbase = Coinbase(api_keys['coinbase'])

  binance_ws = await binance.get_ws_endpoint()
  coinbase_ws = await coinbase.get_ws_endpoint()

  await ws_handler.connect(binance_ws)
  await ws_handler.connect(coinbase_ws)

  for symbol in symbols:
    await ws_handler.subscribe(symbol)

  while True:
    msg = await ws_handler.receive()
    await process_stream_data(msg)
    portfolio.update(msg)
    metrics.track_performance(msg)

if __name__ == "__main__":

  symbols = ['BTCUSDT', 'ETHUSDT']

  loop = asyncio.get_event_loop()
  loop.run_until_complete(start_sockets(symbols))