import pathlib
import jinja2
import pandas as pd
from talent import settings

DIR_TEMPLATES = pathlib.Path(__file__).parent / "templates"

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath=DIR_TEMPLATES),
    lstrip_blocks=True,
    trim_blocks=True,
)

with settings.ETL_TYPES_CSV.open("r", encoding="utf8") as file:
    TYPES = pd.read_csv(file)
with settings.ETL_HISTORY_CSV.open("r", encoding="utf8") as file:
    HISTORY = pd.read_csv(file)
with settings.ETL_ORDERS_CSV.open("r", encoding="utf8") as file:
    ORDERS = pd.read_csv(file)


def write_table(df: pd.DataFrame, title: str):
    template = env.get_template("table.html")
    file_name = title.lower().replace(" ", "_")
    path = settings.DIR_DOCS / f"{file_name}.html"
    df.columns = [c.replace("_", " ").title() for c in df.columns]

    with path.open("w", encoding="utf8") as f:
        table = df.to_html(
            border=False,
            classes="display",
            escape=False,
            float_format="{:.0f}".format,
            index=False,
            justify="center",
            na_rep="",
            table_id="datatable",
        )
        html = template.render(
            title=title,
            table=table,
        )
        f.write(html)


def build_excessive_markup():
    pass


def build_high_volume():
    pass


def build_low_stock():
    pass


def main():
    build_excessive_markup()
    build_high_volume()
    build_low_stock()


if __name__ == "__main__":
    main()
