import db_api_ingestion
import db_csv_ingestion

import schedule
import time


# read from api and csv sources
def main():
    db_api_ingestion.main()
    db_csv_ingestion.main()

# do this every day to keep real-time data
schedule.every(1).days.do(main)


while True:
    schedule.run_pending()
    time.sleep(1)