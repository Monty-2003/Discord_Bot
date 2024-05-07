import db_api_ingestion
import db_csv_ingestion

def main():
    db_api_ingestion.main()
    db_csv_ingestion.main()

main()