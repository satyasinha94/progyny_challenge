import logging
import schedule
import time
import threading
from db_base.db_base import Base, engine, DBSession
from portfolio.portfolio import should_we_build_portfolio, should_we_buy, log_total_portfolio_gain_loss

"""
Setting up basic logging to app.log file located in storage/logs/
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("storage/logs/app.log"),
        logging.StreamHandler()
    ]
)

"""
Initializing session
"""


session = DBSession()
Base.metadata.create_all(engine)


def run_threaded(job_func, job_func_arg):
    """
    This is for parallel execution of logging the purchases and the gain loss of each coin in the portfolio.
    """
    job_thread = threading.Thread(target=job_func(job_func_arg))
    job_thread.start()

should_we_build_portfolio(session)
should_we_buy(session)
schedule.every(1).hours.do(run_threaded, should_we_buy, job_func_arg=session)
schedule.every(1).hours.do(run_threaded, log_total_portfolio_gain_loss, job_func_arg=session)
while True:
    schedule.run_pending()
    time.sleep(1)