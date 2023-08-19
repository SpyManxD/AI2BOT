# 6Backtesting.py

from backtesting import Backtest, Strategy
from backtesting.lib import Trades

# Strategies
from strategies import MomentumStrategy, MeanReversionStrategy

# Portfolio construction
from portfolio import PortfolioOptimizer

# Risk management
from risk import VarOptimizer, DrawdownCalculator

# Automated reporting
from reporting import BacktestReport

# Hyperparameter optimization
from tuning import HyperparameterTuner

# Backtest
backtest = Backtest(portfolios, strategies, data)
results = backtest.run()

# Optimize portfolio
optimizer = PortfolioOptimizer()
portfolios = optimizer.optimize(results)

# Tune strategy params
tuner = HyperparameterTuner()
tuned_strategies = tuner.tune(strategies, data)

# Generate report
report = BacktestReport(results, portfolios, tuned_strategies)
report.render_pdf()

# Monte Carlo simulation
montecarlo = MonteCarlo(data, portfolios, tuned_strategies)
montecarlo.simulate()