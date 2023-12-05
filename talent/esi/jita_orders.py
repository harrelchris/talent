import concurrent.futures
import csv

import requests.exceptions
from requests_futures import sessions
from talent import settings
from talent import utils

session = sessions.FuturesSession()


def request_futures(type_ids: list) -> tuple:
    base_url = "https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&page=1&type_id={type_id}"  # noqa
    futures = []
    for type_id in type_ids:
        url = base_url.format(type_id=type_id)
        future = session.get(url=url)
        future.type_id = type_id
        futures.append(future)

    records = []
    errors = []
    for future in concurrent.futures.as_completed(futures):
        response = future.result()
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            errors.append(future.type_id)
            continue
        try:
            content = response.json()
        except requests.exceptions.JSONDecodeError:
            errors.append(future.type_id)
            continue
        if not isinstance(content, list):
            errors.append(future.type_id)
            continue
        for record_dict in content:
            if not isinstance(record_dict, dict):
                break
            if "error" in record_dict:
                errors.append(future.type_id)
                break
        else:
            records.extend(content)

    return records, errors


def main():
    type_ids = list(utils.get_type_ids())

    orders = []
    results, errors = request_futures(type_ids=type_ids)
    orders.extend(results)
    results, _ = request_futures(type_ids=errors)
    orders.extend(results)

    with settings.ESI_JITA_ORDERS_CSV.open("w", newline="\n", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(orders[0].keys())
        writer.writerows([r.values() for r in orders])


if __name__ == "__main__":
    main()
