import db_api_ingestion
import db_csv_ingestion

import schedule
import time


# read from api and csv sources
def main():
    db_api_ingestion.main()
    db_csv_ingestion.main()

main()