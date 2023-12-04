import csv
import http.client
import io
import sys
import urllib.request
from talent import settings


class Category:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/invCategories.csv"
        self.path = settings.SDE_CATEGORIES_CSV
        self.has_header = True
        self.header = None

    def handle_record(self, data: dict) -> dict:
        return dict(
            id=data["categoryID"],
            name=data["categoryName"],
        )


class Group:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/invGroups.csv"
        self.path = settings.SDE_GROUPS_CSV
        self.has_header = True
        self.header = None

    def handle_record(self, data: dict) -> dict:
        return dict(
            id=data["groupID"],
            name=data["groupName"],
            category_id=data["categoryID"],
        )


class MarketGroup:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/invMarketGroups.csv"
        self.path = settings.SDE_MARKET_GROUPS_CSV
        self.has_header = True
        self.header = None

    def handle_record(self, data: dict) -> dict:
        return dict(
            id=data["marketGroupID"],
            name=data["marketGroupName"],
        )


class MetaGroup:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/invMetaGroups.csv"
        self.path = settings.SDE_META_GROUPS_CSV
        self.has_header = True
        self.header = None

    def handle_record(self, data: dict) -> dict:
        return dict(
            id=data["metaGroupID"],
            name=data["metaGroupName"],
        )


class MetaType:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/invMetaTypes.csv"
        self.path = settings.SDE_META_TYPES_CSV
        self.has_header = True
        self.header = None

    def handle_record(self, data: dict) -> dict:
        return dict(
            id=data["typeID"],
            meta_group_id=data["metaGroupID"],
        )


class Race:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/chrRaces.csv"
        self.path = settings.SDE_RACES_CSV
        self.has_header = True
        self.header = None

    def handle_record(self, data: dict) -> dict:
        return dict(
            id=data["raceID"],
            name=data["raceName"],
        )


class Type:
    def __init__(self):
        self.url = "https://www.fuzzwork.co.uk/dump/latest/invTypes-nodescription.csv"
        self.path = settings.SDE_TYPES_CSV
        self.has_header = False
        self.header = [
            "type_id",
            "group_id",
            "type_name",
            "mass",
            "volume",
            "capacity",
            "portion_size",
            "race_id",
            "base_price",
            "published",
            "market_group_id",
            "icon_id",
            "sound_id",
            "graphic_id",
        ]

    def handle_record(self, data: dict) -> dict:
        if data["published"] == "0":
            return dict()
        if data["market_group_id"] == "\\N":
            return dict()
        if data["race_id"] == "\\N":
            data["race_id"] = None
        return dict(
            type_id=int(data["type_id"]),
            name=data["type_name"],
            group_id=data["group_id"],
            race_id=data["race_id"],
            market_group_id=data["market_group_id"],
        )


def download_tables():
    tables = [
        Category,
        Group,
        MarketGroup,
        MetaGroup,
        MetaType,
        Race,
        Type,
    ]

    for Table in tables:
        table = Table()
        request: http.client.HTTPResponse = urllib.request.urlopen(url=table.url)
        response: bytes = request.read()
        content: str = response.decode()
        file = io.StringIO(content)
        reader = csv.reader(file)
        if table.has_header:
            header = next(reader)
        else:
            header = table.header

        records = []
        for line in reader:
            data: dict = dict(zip(header, line))
            record = table.handle_record(data=data)
            if record:
                records.append(record)

        with table.path.open(mode="w", newline="\n", encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(records[0].keys())
            writer.writerows([r.values() for r in records])


def main():
    response: http.client.HTTPResponse = urllib.request.urlopen(
        url="https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2.md5"
    )
    content: bytes = response.read()
    remote_md5: str = content.decode(encoding="utf8")
    with settings.SDE_LOCAL_MD5.open(mode="r", encoding="utf8") as f:
        local_md5 = f.read()
        if remote_md5 == local_md5:
            sys.exit(0)

    download_tables()

    with settings.SDE_LOCAL_MD5.open(mode="w", encoding="utf8") as f:
        f.write(remote_md5)


if __name__ == "__main__":
    main()
