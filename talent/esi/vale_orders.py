import concurrent.futures
import csv

import evesso
from requests_futures import sessions
from talent import settings

session = sessions.FuturesSession()

sso = evesso.SSO(
    client_id=settings.CLIENT_ID,
    callback_url=settings.CALLBACK_URL,
    scope=settings.SCOPE,
    jwt_file_path=settings.JWT_PATH,
)
sso_header = sso.get_header()

url = "https://esi.evetech.net/latest/markets/structures/1035466617946/?datasource=tranquility&page={page}"
request = session.head(url.format(page=1), headers=sso_header)
response = request.result()
page_count = int(response.headers.get("X-Pages", 0))

urls = [url.format(page=page) for page in range(1, page_count + 1)]
futures = [session.get(url=url, headers=sso_header) for url in urls]

records = []
for future in concurrent.futures.as_completed(futures):
    response = future.result()
    content = response.json()
    records.extend(content)

with settings.ESI_VALE_ORDERS_CSV.open("w", newline="\n", encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(records[0].keys())
    writer.writerows([r.values() for r in records])
