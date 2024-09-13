import click
import csv
from click_default_group import DefaultGroup
from rich_click import RichGroup
from rich.console import Console
import pandas as pd

from typing import List, Optional

import grafte.chart as txchart


class DefaultRichGroup(DefaultGroup, RichGroup):
    """Make `click-default-group` work with `rick-click`."""

    pass


# Define a custom decorator that adds common options
def common_var_options(func):
    options = [
        click.argument(
            "input_file", nargs=1, type=click.File("r"), default="-", required=True
        ),
        click.option(
            "--infer",
            default=True,
            help=f"Load input into Pandas Dataframe to infer and typecast values",
            required=False,
            show_default=True,
            type=click.BOOL,
        ),
        click.option(
            "--output-file",
            "-o",
            help=f"Set the path of the output file to save to, if desired",
            required=False,
            show_default=False,
            type=click.Path(),
        ),
        click.option(
            "--quiet",
            "-q",
            help=f"Suppress the display of the produced chart",
            is_flag=True,
            default=False,
            required=False,
            show_default=True,
        ),
        click.option(
            "--xvar",
            "-x",
            help="The name of the column to use as the x-variable. Defaults to first column",
            required=False,
            show_default=False,
            type=click.STRING,
        ),
        click.option(
            "--yvar",
            "-y",
            help="The name of the column to use as the y-variable. Defaults to second column",
            required=False,
            show_default=False,
            type=click.STRING,
        ),
    ]
    for o in options:
        func = o(func)
    return func


def process_headers(
    headers: List[str], xvar: Optional[str], yvar: Optional[str]
) -> (str, str):
    if not xvar:
        xvar = headers[0]
    if not yvar:
        yvar = headers[1]
    return xvar, yvar


def read_input_file(input_file, infer=True) -> (List[dict], List[str]):
    data = []
    if infer:
        data = pd.read_csv(input_file).to_dict("records")
    else:
        data = list(csv.DictReader(input_file))

    headers = list(data[0].keys())

    return data, headers


def chart_command(
    TheChart: txchart.Chart, input_file, output_file, infer, xvar, yvar, quiet
):

    data, headers = read_input_file(input_file, infer)
    xvar, yvar = process_headers(headers, xvar, yvar)

    chart = TheChart(data, xvar=xvar, yvar=yvar)

    chart.render()
    if output_file:
        chart.save(output_file)

    if not quiet:
        chart.show()


@click.version_option()
@click.group(cls=DefaultRichGroup, default_if_no_args=False)
def cli():
    pass


@cli.command()
@common_var_options
def bar(input_file, output_file, infer, xvar, yvar, quiet):
    """
    Make a bar chart
    """
    chart_command(txchart.Bar, input_file, output_file, infer, xvar, yvar, quiet)


@cli.command()
@common_var_options
def line(input_file, output_file, infer, xvar, yvar, quiet):
    """
    Make a line chart
    """
    chart_command(txchart.Line, input_file, output_file, infer, xvar, yvar, quiet)


@cli.command()
@common_var_options
def scatter(input_file, output_file, infer, xvar, yvar, quiet):
    """
    Make a scatterplot
    """
    chart_command(txchart.Scatter, input_file, output_file, infer, xvar, yvar, quiet)
