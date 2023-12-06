import pandas as pd
from talent import settings


def main():
    with settings.SDE_TYPES_CSV.open("r", encoding="utf8") as f:
        df = pd.read_csv(f)
        type_ids = df[["type_id"]]

    with settings.ESI_VALE_HISTORY_CSV.open("r", encoding="utf8") as f:
        df = pd.read_csv(f)
        dates = df.date.drop_duplicates().sort_values(ascending=True).tail(7)
        week = df[df["date"].isin(dates)]

        lowest = week[["type_id", "lowest"]]
        lowest = lowest.groupby("type_id").min()

        average = week[["type_id", "average"]]
        average = average.groupby("type_id").mean()

        highest = week[["type_id", "highest"]]
        highest = highest.groupby("type_id").max()

        volume = week[["type_id", "volume"]]
        volume = volume.groupby("type_id").sum()

    types = pd.merge(type_ids, lowest, how="left", on="type_id")
    types = pd.merge(types, average, how="left", on="type_id")
    types = pd.merge(types, highest, how="left", on="type_id")
    types = pd.merge(types, volume, how="left", on="type_id")

    with settings.ETL_HISTORY_CSV.open("w", newline="\n", encoding="utf8") as f:
        f.write(types.to_csv(index=False))


if __name__ == "__main__":
    main()
