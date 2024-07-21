import schedule
import time
import parser

def run_scheduler(cfg):
    update_interval = cfg.get_update_interval()
    schedule.every(update_interval).minutes.do(parser.update_products_info, cfg)
    while True:
        schedule.run_pending()
        time.sleep(5)
