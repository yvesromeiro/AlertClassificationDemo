from dotenv import load_dotenv

from src.repositories import prepare_users_db, prepare_marketing_db, populate_users_db, populate_marketing_db
from src.services import gen_users_csv


def main():
    load_dotenv()
    prepare_users_db()
    prepare_marketing_db()
    populate_users_db()
    populate_marketing_db()
    gen_users_csv()

if __name__ == "__main__":
    main()