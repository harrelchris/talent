import concurrent.futures
import csv

import requests.exceptions
from requests_futures import sessions
from talent import settings
from talent import utils


def request_history(session, type_ids: list):
    url = "https://esi.evetech.net/latest/markets/10000003/history/?datasource=tranquility&type_id={type_id}"

    futures = []
    for type_id in type_ids:
        future = session.get(url.format(type_id=type_id))
        future.type_id = type_id
        futures.append(future)

    records = []
    errors = []
    for future in concurrent.futures.as_completed(futures):
        response = future.result()
        if not (200 <= response.status_code < 300):
            errors.append(future.type_id)
            continue
        try:
            history = response.json()
        except requests.exceptions.JSONDecodeError:
            continue
        for record in history:
            if not isinstance(record, dict):
                continue
            record["type_id"] = future.type_id
            records.append(record)
    return records, errors


def write_records(records: list):
    with settings.ESI_VALE_HISTORY_CSV.open("w", newline="\n", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(records[0].keys())
        writer.writerows([r.values() for r in records])


def main():
    session = sessions.FuturesSession()
    type_ids = list(utils.get_type_ids())

    records, errors = request_history(session=session, type_ids=type_ids)
    reattempted_records, errors = request_history(session=session, type_ids=errors)
    records.extend(reattempted_records)

    write_records(records)


if __name__ == "__main__":
    main()
