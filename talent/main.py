import click

from talent.sde import download
from talent.esi import jita_orders
from talent.esi import vale_history
from talent.esi import vale_orders
from talent.etl import history
from talent.etl import orders
from talent.etl import types


@click.group()
def cli():
    pass


@click.group(name="esi")
def group_esi():
    pass


@click.group(name="etl")
def group_etl():
    pass


@click.group(name="sde")
def group_sde():
    pass


cli.add_command(group_esi)
cli.add_command(group_etl)
cli.add_command(group_sde)


@click.command(name="jita_orders")
def esi_jita_orders():
    jita_orders.main()


@click.command(name="vale_history")
def esi_vale_history():
    vale_history.main()


@click.command(name="vale_orders")
def esi_vale_orders():
    vale_orders.main()


group_esi.add_command(esi_jita_orders)
group_esi.add_command(esi_vale_history)
group_esi.add_command(esi_vale_orders)


@click.command(name="history")
def etl_history():
    history.main()


@click.command(name="history")
def etl_orders():
    orders.main()


@click.command(name="history")
def etl_types():
    types.main()


group_etl.add_command(etl_history)
group_etl.add_command(etl_orders)
group_etl.add_command(etl_types)


@click.command(name="download")
def sde_download():
    download.main()


group_sde.add_command(sde_download)
