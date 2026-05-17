import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Activity:
    name: str
    start_time: int
    end_time: int

    def __str__(self) -> str:
        return f'"{self.name}" {self.get_times()}'

    def get_end_time(self) -> int:
        return self.end_time

    def get_times(self) -> set[int]:
        return {h for h in range(self.start_time, self.end_time + 1)}

    def conflicts_with(self, other: 'Activity') -> bool:
        return bool(self.get_times().intersection(other.get_times()))

    @classmethod
    def from_path(cls, path: Path):
        data = json.loads(path.read_text())
        if not isinstance(data, list):
            raise ValueError(
                f'Expected data to be a list of json objects. Got: {data}'
            )
        return [cls(**d) for d in data]


def activity_selection(activities: list[Activity]) -> list[Activity]:
    if not activities:
        return []

    activities = sorted(activities, key=Activity.get_end_time)
    chosen_activities: list[Activity] = [activities[0]]

    current = chosen_activities[0]
    for i in range(1, len(activities)):
        if not activities[i].conflicts_with(current):
            current = activities[i]
            chosen_activities.append(current)

    return chosen_activities
