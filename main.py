import json
from typing import Dict, Any
import csv


def convert_file_from_txt_to_dict(file_path: str) -> Dict[str, Any]:
    purchases = dict()

    with open(file_path, 'r', encoding='utf-8') as file:
        for row in file.readlines()[1:]:
            json_ = json.loads(row)
            purchases[json_['user_id']] = json_['category']

    return purchases


def print_first_items_from_dict(count: int, data: Dict[str, Any]) -> None:
    counter = 0

    for key, value in data.items():
        if counter == count:
            break

        print(key, value)
        counter += 1


def add_source_for_user_id_from_visit_log(file_path: str, purchases: Dict[str, Any]) -> None:
    with open('funnel.csv', mode='w', encoding='cp1251') as w_file:
        names = ['user_id', 'source', 'category']
        file_writer = csv.DictWriter(w_file, delimiter=',', lineterminator='\r', fieldnames=names)
        file_writer.writeheader()

        with open(file_path, 'r', encoding='utf-8') as file:
            for user_id, category in purchases.items():
                for row in file:
                    if user_id in row:
                        _, source = row.split(',')
                        break

                file_writer.writerow({"user_id": user_id, "source": source.strip(), 'category': category})


if __name__ == '__main__':
    purchases_log_path = './purchase_log.txt'
    purchases = convert_file_from_txt_to_dict(purchases_log_path)
    print_first_items_from_dict(count=2, data=purchases)

    visit_log_path = './visit_log.csv'
    add_source_for_user_id_from_visit_log(visit_log_path, purchases=purchases)
