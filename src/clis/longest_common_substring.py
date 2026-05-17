import click
import rich
from lib.longest_common_substring import longest_common_substring


@click.group
def main():
    pass


@main.command('find')
@click.argument('str1', type=click.STRING)
@click.argument('str2', type=click.STRING)
def find_longest_common_substring(str1, str2):
    lcs, matrix = longest_common_substring(str1, str2)
    click.echo(f'The longest common substring is: {lcs}')

    # TODO :: printout a rich table representing the matrix we generated
    if max(len(str1), len(str2)) <= 12:
        from rich import table
        t = table.Table()
