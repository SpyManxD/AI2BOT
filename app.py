# app.py

from services import BinanceStreamer, DataProcessor, ModelTrainer, TradeExecutor
from schedulers import RetrainScheduler
from monitoring import MetricsLogger


class CryptoTradingApp:

    def __init__(self, config):
        self.config = config
        self.streamer = BinanceStreamer(config)
        self.processor = DataProcessor(config)
        self.model = ModelTrainer(config)
        self.executor = TradeExecutor(config)
        self.scheduler = RetrainScheduler(config)
        self.monitor = MetricsLogger(config)

    def run(self):
        self.streamer.start()
        while True:
            data = self.streamer.get_data()
            processed = self.processor.execute(data)

            signals = self.model.predict(processed)
            self.executor.execute(signals)

            self.monitor.log()
            self.scheduler.run_pending()

    def shutdown(self):
        self.streamer.stop()
        print("App stopped successfully!")