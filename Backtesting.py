# Import required components (you need to define these in separate files)
from strategies import MomentumStrategy, MeanReversionStrategy
from portfolio import PortfolioOptimizer
from risk import VarOptimizer, DrawdownCalculator
from reporting import BacktestReport
from tuning import HyperparameterTuner
from montecarlo import MonteCarlo

class Backtesting:
    def __init__(self, portfolios, strategies, data):
        self.portfolios = portfolios
        self.strategies = strategies
        self.data = data

    def run(self):
        # Run backtest
        backtest = Backtest(self.portfolios, self.strategies, self.data)
        results = backtest.run()

        # Optimize portfolio
        optimizer = PortfolioOptimizer()
        portfolios = optimizer.optimize(results)

        # Tune strategy params
        tuner = HyperparameterTuner()
        tuned_strategies = tuner.tune(self.strategies, self.data)

        # Generate report
        report = BacktestReport(results, portfolios, tuned_strategies)
        report.render_pdf()

        # Monte Carlo simulation
        montecarlo = MonteCarlo(self.data, portfolios, tuned_strategies)
        montecarlo.simulate()

        return results

# Example usage
backtesting = Backtesting(portfolios, strategies, data)
results = backtesting.run()
