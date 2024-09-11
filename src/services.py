import csv
import os
import json
import uuid
import smtplib

from sqlalchemy.exc import DBAPIError

from src.models import BaseClassification, UserInformation, ClassificationModel
from src.repositories import get_users_from_db, get_marketing_data_from_db, build_gdpr_db_session


def read_bases_classification():
    file_path = os.path.join("../data/input/", 'bases_classification.json')
    with open(file_path, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Invalid JSON format. Expected a list of dictionaries.")

    return [BaseClassification(**item) for item in data]

def read_csv_user_information():
    file_path = os.path.join("../data/input/", 'users_information.csv')
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        user_information_list = []
        for row in reader:
            user_information = UserInformation(
                row_id=int(row['row_id']),
                user_id=row['user_id'],
                user_state=row['user_state'],
                user_manager=row['user_manager']
            )
            user_information_list.append(user_information)
        return user_information_list

def gen_users_csv():
    classified_bases = read_bases_classification()
    users = get_users_from_db()
    marketing = get_marketing_data_from_db()
    save_dir = os.path.join("../data/input/", 'users_information.csv')

    with open(save_dir, 'w', newline='') as file:
            fieldnames = ['row_id', 'user_id', 'user_state', 'user_manager']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            row_id = 1

            for user in users:
                row_data = {
                    'row_id': row_id,
                    'user_id': user.id,
                    'user_state': user.is_active,
                    'user_manager': list(filter(lambda x: x.db_name == 'usersdb', classified_bases))[0].manager_email
                }
                writer.writerow(row_data)
                row_id += 1

            for data in marketing:
                row_data = {
                    'row_id': row_id,
                    'user_id': data.id,
                    'user_state': 'active',
                    'user_manager': list(filter(lambda x: x.db_name == 'marketingdb', classified_bases))[0].manager_email
                }
                writer.writerow(row_data)
                row_id += 1

def gen_classification_csv_database(classification_data):
    save_dir = os.path.join("../data/output/", 'classification_database.csv')

    with open(save_dir, 'w', newline='') as file:
        fieldnames = ['id', 'db_name', 'owner_email', 'manager_email', 'classification']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for data in classification_data:
            row_data = {
                'id': data.id,
                'db_name': data.db_name,
                'owner_email': data.owner_email,
                'manager_email': data.manager_email,
                'classification': data.classification
            }
            writer.writerow(row_data)

def read_files_and_gen_databases_classification():
    classified_bases = read_bases_classification()
    csv_data = read_csv_user_information()
    session = build_gdpr_db_session()

    info_classification = []

    for data in csv_data:
        info = ClassificationModel(
            id = uuid.uuid4(),
            db_name = list(filter(lambda x: x.manager_email == data.user_manager, classified_bases))[0].db_name,
            owner_email = list(filter(lambda x: x.manager_email == data.user_manager, classified_bases))[0].owner_email,
            manager_email = list(filter(lambda x: x.manager_email == data.user_manager, classified_bases))[0].manager_email,
            classification = list(filter(lambda x: x.manager_email == data.user_manager, classified_bases))[0].classification
        )
        info_classification.append(info)

    send_email('lucas_docker@example.com', 'Sera que funciona', 'Voce ganhou no tigrinho e a PF vai atras de vc')

    try:
        session.bulk_save_objects(info_classification)
        session.commit()
        session.close()
        gen_classification_csv_database(info_classification)
    except DBAPIError as e:
        print(e)
    except Exception as e:
        print(e)

def send_email(to, subject, body):
    smtp_server = 'localhost'
    smtp_port = 1025

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail('seu_email@example.com', to, f'Subject: {subject}\n\n{body}')