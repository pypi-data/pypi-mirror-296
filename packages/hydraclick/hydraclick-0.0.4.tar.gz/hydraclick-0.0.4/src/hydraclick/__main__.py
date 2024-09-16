import sys
import logging

import click
import flogging

from hydraclick import hydra_command


@click.group()
def cli():
    """Run command line interface for hydraclick."""
    flogging.setup(allow_trailing_dot=True)


@cli.command(short_help="test_stuff.")
@hydra_command()
def nothing(args, **kwargs):
    """Test function that does nothing."""
    logging.warning(f"Doing nothing {args, kwargs}")


if __name__ == "__main__":
    sys.exit(cli())
