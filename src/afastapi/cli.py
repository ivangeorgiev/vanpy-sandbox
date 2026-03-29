# from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import click

# from pybkkpr.config import get_settings
# from pybkkpr.models.account import ApplicationAccount, ApplicationAccountUser
# from pybkkpr.models.auth import User
# from pybkkpr.models.broker import Broker, BrokerAccount
# from pybkkpr.models.currency import Currency, CurrencyExchangeRate
# from sqlalchemy.orm import Session
# from .database import SessionLocal, init_db
# from .services import ExchangeRateService


@click.group()
@click.version_option()
def cli():
    """Asynchronous FastAPI soundbox"""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", default=8080, help="Port to run the server on")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development")
@click.option("--workers", default=1, help="Number of worker processes to run")
def server(host, port, reload, workers):
    import uvicorn

    uvicorn.run(
        "afastapi.api.app:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
    )


@cli.command()
@click.option(
    "--test",
    type=click.Choice(["sync", "async", "to-thread"], case_sensitive=False),
    help="Which locust test to run",
)
def locust(test):
    from locust.main import main as locust_main

    locustfile_base_dir = Path(__file__).parent / "locust"
    locust_args = ["locust"]

    if test == "to-thread":
        locust_args.append("-f")
        locust_args.append(str(locustfile_base_dir / "locustfile_tothread.py"))

    if test == "sync":
        locust_args.append("-f")
        locust_args.append(str(locustfile_base_dir / "locustfile_sync.py"))

    if test == "async":
        locust_args.append("-f")
        locust_args.append(str(locustfile_base_dir / "locustfile_async.py"))

    if len(locust_args) < 2:
        locust_args.append("-f")
        locust_args.append(str(locustfile_base_dir / "locustfile.py"))

    with patch("sys.argv", locust_args):
        locust_main()

    # import subprocess
    # subprocess.run(["locust", "-f", "locustfile.py", "--headless", "-u", "100", "-r", "10", "--run-time", "1m"])


def main():
    cli()


if __name__ == "__main__":
    main()
