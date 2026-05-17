from pathlib import Path
import click

from lib.activities import Activity, activity_selection


@click.group
def main():
    pass


@main.command('select-greedy')
@click.argument(
    'activities',
    type=click.Path(path_type=Path)
)
def select(activities: Path):
    """
    Use a greedy algorithm to select the most non-conflicting
    activities out of those defined at an input json path.
    """
    activities = Activity.from_path(activities)
    click.secho('Processing activities:', fg='yellow')
    for activity in activities:
        click.secho(f'  - {str(activity)}', fg='cyan')

    chosen = activity_selection(activities)
    click.secho('Selected:', fg='yellow')
    for activity in chosen:
        click.secho(f'  - {str(activity)}', fg='cyan')
