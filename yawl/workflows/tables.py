from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterator, List, Optional


class WorkFlowStep(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def dest_table(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def upstream(self) -> Optional[str]:
        raise NotImplementedError()


class BigQueryWkStep(WorkFlowStep):
    def __init__(self, sql: str, dest_table: str) -> None:
        self.__dest_table = dest_table
        self.__sql = sql
        self.__upstream = None

    @property
    def dest_table(self) -> str:
        return self.__dest_table

    @property
    def upstream(self) -> Optional[str]:
        return self.__upstream

    @upstream.setter
    def upstream(self, upstream: Optional[str]) -> None:
        self.__upstream = upstream  # type: ignore

    def execute(self) -> None:
        if self.__sql.endswith(".sql"):
            pass
        print(
            (
                f"Executing step of upstream {self.__upstream}"
                f" and destination {self.__dest_table}"
            )
        )


class Queue:
    def __init__(self) -> None:
        self.__commands: List[WorkFlowStep] = []

    def add(self, command: BigQueryWkStep) -> "Queue":
        if self.__commands:
            command.upstream = self.__commands[-1].dest_table  # type: ignore

        self.__commands.append(command)
        return self

    def process(self) -> None:
        for command in self.__commands:
            command.execute()


@contextmanager
def queue() -> Iterator[Queue]:
    queue = Queue()
    yield queue


if __name__ == "__main__":
    step_1 = BigQueryWkStep("file_1.sql", "table_1")
    step_2 = BigQueryWkStep("file_2.sql", "table_2")
    with queue() as q:
        q.add(step_1).add(step_2).process()
