import os
import pathlib
import dotenv

DIR_ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR_DATA = DIR_ROOT / "data"
DIR_ESI = DIR_DATA / "esi"
DIR_ETL = DIR_DATA / "etl"
DIR_SDE = DIR_DATA / "sde"

dotenv.load_dotenv(DIR_ROOT / ".env")

ESI_JITA_ORDERS_CSV = DIR_ESI / "jita_orders.csv"
ESI_VALE_ORDERS_CSV = DIR_ESI / "vale_orders.csv"

ETL_ORDERS_CSV = DIR_ETL / "orders.csv"

SDE_LOCAL_MD5 = DIR_SDE / "local.md5"
SDE_CATEGORIES_CSV = DIR_SDE / "categories.csv"
SDE_GROUPS_CSV = DIR_SDE / "groups.csv"
SDE_MARKET_GROUPS_CSV = DIR_SDE / "market_groups.csv"
SDE_META_GROUPS_CSV = DIR_SDE / "meta_groups.csv"
SDE_META_TYPES_CSV = DIR_SDE / "meta_types.csv"
SDE_RACES_CSV = DIR_SDE / "races.csv"
SDE_TYPES_CSV = DIR_SDE / "types.csv"

JWT_PATH = DIR_ROOT / 'jwt.json'
CLIENT_ID = os.environ.get('CLIENT_ID')
CALLBACK_URL = os.environ.get('CALLBACK_URL')
SCOPE = os.environ.get('SCOPE')
