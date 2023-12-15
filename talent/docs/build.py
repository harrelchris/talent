import datetime
import jinja2
import pandas as pd
import pathlib
from talent import settings

DIR_TEMPLATES = pathlib.Path(__file__).parent / "templates"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath=DIR_TEMPLATES),
    lstrip_blocks=True,
    trim_blocks=True,
)

with settings.ETL_TYPES_CSV.open("r", encoding="utf8") as file:
    df_types = pd.read_csv(file)
with settings.ETL_HISTORY_CSV.open("r", encoding="utf8") as file:
    df_history = pd.read_csv(file)
with settings.ETL_ORDERS_CSV.open("r", encoding="utf8") as file:
    df_orders = pd.read_csv(file)


def build_outbound_arbitrage():
    df_orders["margin"] = (df_orders["jita_max_buy"] - df_orders["vale_min_sell"]) / df_orders["vale_min_sell"] * 100
    df_orders["difference"] = df_orders["jita_max_buy"] - df_orders["vale_min_sell"]
    df_history["value"] = df_orders["vale_available"] * (df_orders["jita_max_buy"] - df_orders["vale_min_sell"])

    df = pd.merge(df_types, df_orders, how="left", on="type_id")
    df = pd.merge(df, df_history, how="left", on="type_id")

    df = df[df["margin"] >= 3.7]  # Sales tax is 3.6%
    df = df[[
        "name",
        "category",
        "group",
        "meta_group",
        "vale_min_sell",
        "jita_max_buy",
        "difference",
        "margin",
    ]]
    df = df.sort_values(by=["difference"], ascending=False)

    df["vale_min_sell"] = df["vale_min_sell"].apply("{:,.2f}".format)
    df["jita_max_buy"] = df["jita_max_buy"].apply("{:,.2f}".format)
    df["margin"] = df["margin"].apply("{:,.1f}%".format)
    df["difference"] = df["difference"].apply("{:,.2f}".format)
    df = df.rename(
        columns={
            "jita_max_buy": "jita_buy",
            "vale_min_sell": "vale_sell",
            "meta_group": "meta",
        },
    )
    df = df.fillna("")
    return df


def build_inbound_arbitrage():
    df_orders["margin"] = (df_orders["vale_max_buy"] - df_orders["jita_min_sell"]) / df_orders["jita_min_sell"] * 100
    df_orders["difference"] = df_orders["vale_max_buy"] - df_orders["jita_min_sell"]

    df = pd.merge(df_types, df_orders, how="left", on="type_id")
    df = pd.merge(df, df_history, how="left", on="type_id")

    df = df[df["margin"] >= 3.7]  # Sales tax is 3.6%
    df = df[[
        "name",
        "category",
        "group",
        "meta_group",
        "vale_max_buy",
        "jita_min_sell",
        "difference",
        "margin",
    ]]
    df = df.sort_values(by=["difference"], ascending=False)

    df["vale_max_buy"] = df["vale_max_buy"].apply("{:,.2f}".format)
    df["jita_min_sell"] = df["jita_min_sell"].apply("{:,.2f}".format)
    df["margin"] = df["margin"].apply("{:,.1f}%".format)
    df["difference"] = df["difference"].apply("{:,.2f}".format)
    df = df.rename(
        columns={
            "vale_max_buy": "vale_buy",
            "jita_sell": "vale_sell",
            "meta_group": "meta",
        }
    )
    df = df.fillna("")
    return df


def build_under_stocked():
    df = pd.merge(df_types, df_orders, how="left", on="type_id")
    df = pd.merge(df, df_history, how="left", on="type_id")
    df["level"] = df["vale_available"] / df["volume"] * 100

    df = df[df["volume"] >= 1]
    df = df[df["level"] < 100]
    df = df[[
        "name",
        "category",
        "group",
        "meta_group",
        "level",
        "volume",
        "vale_available",
        "average",
    ]]
    df = df.sort_values(by=["level"], ascending=False)

    df["level"] = df["level"].apply("{:,.1f}%".format)
    df["volume"] = df["volume"].apply("{:,.0f}".format)
    df["vale_available"] = df["vale_available"].apply("{:,.0f}".format)
    df["average"] = df["average"].apply("{:,.2f}".format)
    df = df.rename(columns={"vale_available": "available", "meta_group": "meta"})
    df = df.fillna("")
    return df


def build_excessive_markup():
    df = pd.merge(df_types, df_orders, how="left", on="type_id")
    df = pd.merge(df, df_history, how="left", on="type_id")
    df["markup"] = (df_orders["vale_min_sell"] - df_orders["jita_min_sell"]) / df_orders["jita_min_sell"] * 100
    df["difference"] = df_orders["vale_min_sell"] - df_orders["jita_min_sell"]

    df = df[df["markup"] >= 25]
    df = df[df["average"] >= 1]
    df = df[df["volume"] >= 1]
    df = df[[
        "name",
        "category",
        "group",
        "meta_group",
        "vale_min_sell",
        "jita_min_sell",
        "difference",
        "markup",
        "volume",
    ]]
    df = df.sort_values(by=["markup"], ascending=False)

    df["vale_min_sell"] = df["vale_min_sell"].apply("{:,.2f}".format)
    df["jita_min_sell"] = df["jita_min_sell"].apply("{:,.2f}".format)
    df["difference"] = df["difference"].apply("{:,.2f}".format)
    df["markup"] = df["markup"].apply("{:,.1f}%".format)
    df["volume"] = df["volume"].apply("{:,.0f}".format)
    df = df.rename(
        columns={
            "jita_min_sell": "jita_sell",
            "vale_min_sell": "vale_sell",
            "meta_group": "meta",
        }
    )
    df = df.fillna("")
    return df


def write_table_view(df: pd.DataFrame, title: str, description: str, left_columns: tuple, paging: bool = False):
    template = env.get_template("table.html")
    path = settings.DIR_DOCS / f'{title.lower().replace(" ", "_")}.html'

    df.style.format(precision=3, thousands=",", decimal=".")
    df = df.fillna("")

    with path.open("w", encoding="utf8") as f:
        html = template.render(
            title=title,
            description=description,
            left_columns=left_columns,
            headers=[c.replace("_", " ").title() for c in df.columns],
            records=df.to_records(
                index=False,
            ),
            paging=paging,
            updated_at=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        )
        f.write(html)


def main():
    df = build_outbound_arbitrage()
    title = "Outbound Arbitrage"
    description = "Items that can be bought in Vale and immediately sold in Jita for profit."
    left_columns = 1, 2, 3, 4
    write_table_view(
        df=df,
        title=title,
        description=description,
        left_columns=left_columns,
    )

    df = build_inbound_arbitrage()
    title = "Inbound Arbitrage"
    description = "Items that can be bought in Jita and immediately sold in Vale for profit."
    left_columns = (1, 2, 3, 4)
    write_table_view(
        df=df,
        title=title,
        description=description,
        left_columns=left_columns,
    )

    df = build_under_stocked()
    title = "Under Stocked"
    description = "Items with fewer than 7 days of supply."
    left_columns = (1, 2, 3, 4)
    write_table_view(
        df=df,
        title=title,
        description=description,
        left_columns=left_columns,
        paging=True,
    )

    df = build_excessive_markup()
    title = "Excessive Markup"
    description = "Items with greater than 25% markup."
    left_columns = (1, 2, 3, 4)
    write_table_view(
        df=df,
        title=title,
        description=description,
        left_columns=left_columns,
        paging=True,
    )


if __name__ == "__main__":
    main()
