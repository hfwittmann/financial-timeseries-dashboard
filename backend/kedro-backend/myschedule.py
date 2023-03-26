import schedule
import time
import subprocess
import sys


def job():
    print("I'm working...")
    subprocess.run(
        ["kedro", "run"],
        cwd="/app",
    )


# schedule.every(10).seconds.do(job)
schedule.every().day.at("09:00").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
