# main.py

from app import CryptoTradingApp
from config import settings

app = CryptoTradingApp(settings)

try:
  app.run()
except KeyboardInterrupt:
  app.shutdown()