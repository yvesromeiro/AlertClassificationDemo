from dotenv import load_dotenv

from src.repositories import prepare_users_db, prepare_marketing_db, populate_users_db, populate_marketing_db, \
    prepare_gdpr_db
from src.services import gen_users_csv, read_files_and_gen_databases_classification


def main():
    load_dotenv()
    prepare_users_db()
    prepare_marketing_db()
    prepare_gdpr_db()
    populate_users_db()
    populate_marketing_db()
    gen_users_csv()
    read_files_and_gen_databases_classification()
    print('Processed successfully!')

if __name__ == "__main__":
    main()