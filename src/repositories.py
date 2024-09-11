import os
import enum
import uuid
import random
from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

from faker import Faker
from src.models import Base, UserModel, MarketingCampaign
from src.utils import generate_document_id, get_random_gender

fake = Faker('en-US')

class Databases(enum.Enum):
    USERS = 'users'
    MARKETING = 'marketing'
    GDPR = 'gdpr'

def build_connection_string(database):
    selected_database = ""
    if database == Databases.USERS:
        selected_database = os.getenv('POSTGRES_USER_DB_NAME')
    if database == Databases.MARKETING:
        selected_database = os.getenv('POSTGRES_MARKETING_DB_NAME')
    if database == Databases.GDPR:
        selected_database = os.getenv('POSTGRES_GDPR_DB_NAME')

    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database_name = selected_database

    return f'postgresql://{user}:{password}@{host}:{port}/{database_name}'

def create_database_session(database):
    engine = create_engine(database)
    session = sessionmaker(bind=engine)
    return session()

def build_users_db_session():
    connection_string = build_connection_string(Databases.USERS)
    return create_database_session(connection_string)

def build_marketing_db_session():
    connection_string = build_connection_string(Databases.MARKETING)
    return create_database_session(connection_string)

def build_gdpr_db_session():
    connection_string = build_connection_string(Databases.GDPR)
    return create_database_session(connection_string)

def prepare_database(connection_string):
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)

def prepare_users_db():
    connection_string = build_connection_string(Databases.USERS)
    prepare_database(connection_string)

def prepare_marketing_db():
    connection_string = build_connection_string(Databases.MARKETING)
    prepare_database(connection_string)

def prepare_gdpr_db():
    connection_string = build_connection_string(Databases.GDPR)
    prepare_database(connection_string)


def populate_users_db():
    session = build_users_db_session()
    gen_number = os.getenv('NUMBER_OF_RECORDS_IN_USERS_TABLE')
    users = []
    for u in range(int(gen_number)):
        users.append(
            UserModel(
                id = uuid.uuid4(),
                name = fake.name(),
                email = fake.email(),
                birthdate = str(fake.date_of_birth()),
                document = generate_document_id(length=15, prefix="DOC-", suffix=""),
                gender = get_random_gender(),
                telephone = fake.phone_number(),
                is_active = fake.boolean(chance_of_getting_true=50),
                yearly_income = fake.random_int(min=50000, max=320000)
            )
        )

    try:
        session.bulk_save_objects(users)
        session.commit()
        session.close()
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

def populate_marketing_db():
    session = build_marketing_db_session()
    gen_number = os.getenv('NUMBER_OF_RECORDS_IN_MARKETING_TABLE')
    marketing_data = []
    for u in range(int(gen_number)):
        marketing_data.append(
            MarketingCampaign(
                id=str(uuid.uuid4()),
                name=fake.bs().title(),
                start_date=fake.date_this_year(),
                end_date=fake.date_this_year(),
                channel=random.choice(["email", "social media", "SMS", "search engine"]),
                budget=round(random.uniform(1000, 50000), 2),
                target_audience=random.choice(["Teens", "Adults", "Seniors"])
            )
        )

    try:
        session.bulk_save_objects(marketing_data)
        session.commit()
        session.close()
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

def get_users_from_db():
    session = build_users_db_session()
    try:
        users = session.query(UserModel).limit(50).all()
        session.close()
        return users
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

def get_marketing_data_from_db():
    session  = build_marketing_db_session()
    try:
        data = session.query(MarketingCampaign).limit(50).all()
        session.close()
        return data
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)