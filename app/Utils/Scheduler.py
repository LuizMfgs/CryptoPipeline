import schedule
import time

from Pipeline import run_pipeline


schedule.every(1).minutes.do(
    run_pipeline
)
print("Scheduler started")
while True:

    schedule.run_pending()

    time.sleep(60)
