#!/usr/bin/env python3

import logging
import click
from lib.entrypoint import Entrypoint
from lib.logger import Logger

logger = Logger.get_logger("dataset-recorder")

@click.group()
def cli():
    pass

@click.command(help="run the main application")
@click.argument('configuration_file', type=click.Path(exists=True))
@click.option('--debug', is_flag=True, help="Debug mode")
def run(configuration_file: str, debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
    entrypoint = Entrypoint(config_file=configuration_file)
    entrypoint.do_diagnostics()
    entrypoint.take_shot()
    entrypoint.stop()

@click.command(help="do device diagnostics")
@click.argument('configuration_file', type=click.Path(exists=True))
@click.option('--debug', is_flag=True, help="Debug mode")
def diagnostics(configuration_file: str, debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
    entrypoint = Entrypoint(config_file=configuration_file)
    entrypoint.do_diagnostics()


cli.add_command(run)
cli.add_command(diagnostics)


if __name__ == "__main__":
    cli()
