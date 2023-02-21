
import csv
import json


def convert_file(csv_file, json_file, model):

    '''Преобразование изCSV  в JSON'''

    result = []
    with open(csv_file, 'r', encoding='utf-8') as csv_f:
        csv_reade = csv.DictReader(csv_f)
        for row in csv_reade:
            record = {"model": model, "pk": row["id"]}
            del row["id"]
            if 'age' in row:
                row['age'] = int(row['age'])
            if 'price' in row:
                row['price'] = int(row['price'])
            if 'lat' in row:
                row['lat'] = float(row['lat'])
            if 'lng' in row:
                row['lng'] = float(row['lng'])
            if 'is_published' in row:
                if row['is_published'] == "TRUE":
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if "location_id" in row:
                row["location"] = [row["location_id"]]
                del row["location_id"]
            record["fields"] = row
            result.append(record)

    with open(json_file, 'w', encoding='utf-8') as json_f:
        json_f.write(json.dumps(result, ensure_ascii=False))


convert_file('../data/ad.csv', '../data/ad.json', 'ads.Ad')
convert_file('../data/category.csv', '../data/category.json', 'ads.Category')
convert_file('../data/location.csv', '../data/location.json', 'users.Location')
convert_file('../data/user.csv', '../data/user.json', 'users.User')

