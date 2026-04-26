import click


@click.group()
def main():
    pass


@main.command()
@click.argument("logfile", type=click.Path(exists=True))
@click.option("--severity", default=None)
@click.option("--since", default=None)
def summarize(logfile, severity, since):
    pass
