import click
from vianaxabreu_de_toolkit.vm import start, stop, connect, test1

@click.group()
def cli():
    pass
cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)
cli.add_command(test1)


if __name__ == '__main__':
    cli()
