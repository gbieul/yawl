"""
Module used for BigQuery interactions.
"""
import re
from typing import Optional

from yawl.clients.bigquery_datatransfer import BigQueryDataTransfer, DestTableNameTemplate
from yawl.shared.constants import SERVICE_ACCOUNT_EMAIL
from yawl.workflows.base import WorkFlowStep
from yawl.workflows.queue import queue


class BigQueryWorkflowStep(WorkFlowStep):
    def __init__(
        self, sql: str, dest_table: str, squeduled_query_name: str, schedule: str
    ) -> None:
        # dest_table contains fully qualified table as "project.dataset.table"
        self.__sql = sql
        self.__project_id = dest_table.split(".")[0]
        self.__dataset = dest_table.split(".")[1]
        self.__dest_table = dest_table.split(".")[2]
        self.__squeduled_query_name = squeduled_query_name
        self.__schedule = schedule
        self.__upstream = None

        self.__client = BigQueryDataTransfer(
            project_id=self.__project_id, service_account=SERVICE_ACCOUNT_EMAIL
        )

    @property
    def dest_table(self) -> str:
        return self.__dest_table

    @property
    def upstream(self) -> Optional[str]:
        return self.__upstream

    @upstream.setter
    def upstream(self, upstream: Optional[str]) -> None:
        self.__upstream = upstream  # type: ignore

    def get_sql_file(self) -> str:
        """
        Cleans up extra spaces and new lines of a query file making it
        up a single, long, string.
        """

        with open(self.__sql, "r") as f:
            file = f.read()
        self.__sql = re.sub(r"[\s]{2,}|\n", " ", file)

    def execute(self) -> None:
        if self.__sql.endswith(".sql"):
            self.get_sql_file()

        self.__client.create_transfer_config(
            query_str=self.__sql,
            dest_dataset_id=self.__dataset,
            dest_table_id=self.dest_table,
            squeduled_query_name=self.__squeduled_query_name,
            schedule=self.__schedule,
            dest_table_name_template=DestTableNameTemplate.no_template.value,
            write_disposition="WRITE_TRUNCATE",
            partitioning_field="",
        )
        print(
            (
                f"Executing step of upstream {self.upstream}"
                f" and destination {self.dest_table}"
            )
        )


if __name__ == "__main__":
    step_1 = BigQueryWorkflowStep(
        sql="file_1.sql",
        dest_table="project.dataset.table_1",
        squeduled_query_name="Query 1",
        schedule="Every Mon-Fri 09:00",
    )
    step_2 = BigQueryWorkflowStep(
        sql="file_2.sql",
        dest_table="project.dataset.table_2",
        squeduled_query_name="Query 2",
        schedule="Every Mon-Fri 10:00",
    )
    with queue() as q:
        q.add(step_1).add(step_2).process()
