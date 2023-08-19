# MonitoringAlerting.py

from prometheus_client import CollectorRegistry, Counter, Gauge, push_to_gateway
from alerting import EmailAlert, TelegramAlert
from dashboards import GrafanaDashboard
from caching import RedisCache

cache = RedisCache()
registry = CollectorRegistry()

requests = Counter('requests', 'Number of requests', registry=registry)
drawdown = Gauge('drawdown', 'Max drawdown', registry=registry)


@cache.cached
def get_drawdown():
    return calculate_drawdown()


@app.route('/')
def index():
    requests.inc()
    return 'Hello'


@app.route('/metrics')
def export_metrics():
    push_to_gateway('prometheus:9090', job='bot', registry=registry)


@app.route('/dashboard')
def show_dashboard():
    dashboard = GrafanaDashboard(cache)
    return dashboard.render()


@app.route('/alerts')
def check_alerts():
    draw = get_drawdown()
    if draw > 0.1:
        TelegramAlert(f"Drawdown over 10%: {draw}").send()
        EmailAlert(f"Drawdown over 10%: {draw}").send()

    return 'OK'