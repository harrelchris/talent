import pathlib

DIR_ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR_DATA = DIR_ROOT / "data"
DIR_ESI = DIR_DATA / "esi"
DIR_SDE = DIR_DATA / "sde"

ESI_JITA_ORDERS_CSV = DIR_ESI / "jita_orders.csv"

SDE_LOCAL_MD5 = DIR_SDE / "local.md5"
SDE_CATEGORIES_CSV = DIR_SDE / "categories.csv"
SDE_GROUPS_CSV = DIR_SDE / "groups.csv"
SDE_MARKET_GROUPS_CSV = DIR_SDE / "market_groups.csv"
SDE_META_GROUPS_CSV = DIR_SDE / "meta_groups.csv"
SDE_META_TYPES_CSV = DIR_SDE / "meta_types.csv"
SDE_RACES_CSV = DIR_SDE / "races.csv"
SDE_TYPES_CSV = DIR_SDE / "types.csv"
