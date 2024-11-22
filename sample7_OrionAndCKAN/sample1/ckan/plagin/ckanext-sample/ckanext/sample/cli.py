import click


@click.group(short_help="sample CLI.")
def sample():
    """sample CLI.
    """
    pass


@sample.command()
@click.argument("name", default="sample")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [sample]
