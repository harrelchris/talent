import csv
import pathlib
from talent import settings


def get_type_ids() -> set:
    types = load_csv(settings.SDE_TYPES_CSV)
    return set(types.keys())


def load_csv(path: pathlib.Path) -> dict:
    output = {}
    with path.open("r", encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            record = dict(zip(header, row))
            cast_ids(record)
            try:
                record_id = record.pop("id")
            except KeyError:
                record_id = record.pop("type_id")
            output[record_id] = record
    return output


def cast_ids(data: dict):
    for key, value in data.items():
        if "id" in key:
            try:
                data[key] = int(value)
            except ValueError:
                pass
