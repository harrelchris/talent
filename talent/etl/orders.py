import pandas as pd
from talent import settings

with settings.SDE_TYPES_CSV.open("r", encoding="utf8") as f:
    df = pd.read_csv(f)
    df = df[["type_id"]]
    types = df.sort_values("type_id")

with settings.ESI_VALE_ORDERS_CSV.open("r", encoding="utf8") as f:
    df = pd.read_csv(f)
    df = df[["type_id", "is_buy_order", "price", "volume_remain"]]

    buy_orders = df[df["is_buy_order"] == True]
    buy_orders = buy_orders[["type_id", "price"]]
    max_buy = buy_orders.groupby("type_id").max()
    vale_max_buy = max_buy.rename(columns={"price": "vale_max_buy"})

    sell_orders = df[df["is_buy_order"] == False]
    sell_orders_price = sell_orders[["type_id", "price"]]
    min_sell = sell_orders_price.groupby("type_id").min()
    vale_min_sell = min_sell.rename(columns={"price": "vale_min_sell"})

    sell_orders_volume_remain = sell_orders[["type_id", "volume_remain"]]
    sum_remain = sell_orders_volume_remain.groupby("type_id").sum()
    vale_available = sum_remain.rename(columns={"volume_remain": "vale_available"})

with settings.ESI_JITA_ORDERS_CSV.open("r", encoding="utf8") as f:
    df = pd.read_csv(f)
    df = df[["type_id", "is_buy_order", "price", "volume_remain"]]

    buy_orders = df[df["is_buy_order"] == True]
    buy_orders = buy_orders[["type_id", "price"]]
    max_buy = buy_orders.groupby("type_id").max()
    jita_max_buy = max_buy.rename(columns={"price": "jita_max_buy"})

    sell_orders = df[df["is_buy_order"] == False]
    sell_orders_price = sell_orders[["type_id", "price"]]
    min_sell = sell_orders_price.groupby("type_id").min()
    jita_min_sell = min_sell.rename(columns={"price": "jita_min_sell"})

    sell_orders_volume_remain = sell_orders[["type_id", "volume_remain"]]
    sum_remain = sell_orders_volume_remain.groupby("type_id").sum()
    jita_available = sum_remain.rename(columns={"volume_remain": "jita_available"})

types = pd.merge(types, vale_max_buy, how="left", on="type_id")
types = pd.merge(types, vale_min_sell, how="left", on="type_id")
types = pd.merge(types, vale_available, how="left", on="type_id")
types = pd.merge(types, jita_max_buy, how="left", on="type_id")
types = pd.merge(types, jita_min_sell, how="left", on="type_id")
types = pd.merge(types, jita_available, how="left", on="type_id")

with settings.ETL_ORDERS_CSV.open("w", newline="\n", encoding="utf8") as f:
    f.write(types.to_csv(index=False))
