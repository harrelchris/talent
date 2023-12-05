import csv
import settings
import utils

sde_categories = utils.load_csv(settings.SDE_CATEGORIES_CSV)
sde_groups = utils.load_csv(settings.SDE_GROUPS_CSV)
sde_market_groups = utils.load_csv(settings.SDE_MARKET_GROUPS_CSV)
sde_meta_groups = utils.load_csv(settings.SDE_META_GROUPS_CSV)
sde_meta_types = utils.load_csv(settings.SDE_META_TYPES_CSV)
sde_races = utils.load_csv(settings.SDE_RACES_CSV)
sde_types = utils.load_csv(settings.SDE_TYPES_CSV)


def get_group_name(group_id: int) -> str:
    group = sde_groups[group_id]
    return group["name"]


def get_market_group_name(market_group_id: int) -> str:
    market_group = sde_market_groups[market_group_id]
    return market_group["name"]


def get_race_name(race_id: int) -> str | None:
    if not race_id:
        return None
    race = sde_races[race_id]
    return race["name"]


def get_category_name(group_id: int) -> str:
    group = sde_groups[group_id]
    category_id = group["category_id"]
    category = sde_categories[category_id]
    return category["name"]


def get_meta_group_name(type_id: int) -> str | None:
    meta_type = sde_meta_types.get(type_id)
    if meta_type:
        meta_group_id = meta_type["meta_group_id"]
        meta_group = sde_meta_groups[meta_group_id]
        return meta_group["name"]
    else:
        return None


def main():
    records = []
    for type_id, values in sde_types.items():
        name = values["name"]
        group_id = values["group_id"]
        market_group_id = values["market_group_id"]
        race_id = values["race_id"]

        record = dict(
            type_id=type_id,
            name=name,
            group=get_group_name(group_id=group_id),
            market_group=get_market_group_name(market_group_id=market_group_id),
            race=get_race_name(race_id=race_id),
            category=get_category_name(group_id=group_id),
            meta_group=get_meta_group_name(type_id=type_id),
        )
        records.append(record)

    with settings.ETL_TYPES_CSV.open("w", newline="\n", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(records[0].keys())
        writer.writerows([r.values() for r in records])


if __name__ == "__main__":
    main()
