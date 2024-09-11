import csv
import os

from src.repositories import get_users_from_db

def gen_users_csv():
    users = get_users_from_db()
    user_manager = 'lucas@example.com'
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
                    'user_manager': user_manager
                }
                writer.writerow(row_data)
                row_id += 1