import click

from talent.docs import build
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


@click.group(name="docs")
def group_docs():
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


cli.add_command(group_docs)
cli.add_command(group_esi)
cli.add_command(group_etl)
cli.add_command(group_sde)


@click.command(name="build")
def docs_build():
    click.echo("Building docs")
    build.main()


group_docs.add_command(docs_build)


@click.command(name="jita_orders")
def esi_jita_orders():
    click.echo("Retrieving Jita orders")
    jita_orders.main()


@click.command(name="vale_history")
def esi_vale_history():
    click.echo("Retrieving Vale history")
    vale_history.main()


@click.command(name="vale_orders")
def esi_vale_orders():
    click.echo("Retrieving Vale orders")
    vale_orders.main()


group_esi.add_command(esi_jita_orders)
group_esi.add_command(esi_vale_history)
group_esi.add_command(esi_vale_orders)


@click.command(name="history")
def etl_history():
    click.echo("Processing history")
    history.main()


@click.command(name="orders")
def etl_orders():
    click.echo("Processing orders")
    orders.main()


@click.command(name="types")
def etl_types():
    click.echo("Processing types")
    types.main()


group_etl.add_command(etl_history)
group_etl.add_command(etl_orders)
group_etl.add_command(etl_types)


@click.command(name="download")
def sde_download():
    click.echo("Retrieving static data")
    download.main()


group_sde.add_command(sde_download)
