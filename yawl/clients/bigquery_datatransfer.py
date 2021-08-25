"""
Client used to schedule queries on BigQuery.
"""
import logging
from enum import Enum

from google.cloud import bigquery_datatransfer

logger = logging.getLogger(__name__)


class DestTableNameTemplate(Enum):
    run_date = "_{run_date}"
    run_time = "_{run_time}"
    no_template = ""


class BigQueryDataTransfer:
    def __init__(self, project_id: str, service_account: str) -> None:
        self._project_id = project_id
        self._service_account = service_account
        self._bq_datatransfer_client = None

    @property
    def bq_datatransfer_client(self):
        if not self._bq_datatransfer_client:
            self._bq_datatransfer_client = (
                bigquery_datatransfer.DataTransferServiceClient()
            )
            self._parent = self._bq_datatransfer_client.common_project_path(
                self._project_id
            )

        return self._bq_datatransfer_client

    def create_transfer_config(
        self,
        query_str: str,
        dest_dataset_id: str,
        dest_table_id: str,
        squeduled_query_name: str,
        schedule: str,
        dest_table_name_template: DestTableNameTemplate = DestTableNameTemplate.no_template.value,  # noqa: E501
        write_disposition: str = "WRITE_TRUNCATE",
        partitioning_field: str = "",
    ):
        transfer_config = bigquery_datatransfer.TransferConfig(
            destination_dataset_id=dest_dataset_id,
            display_name=squeduled_query_name,
            data_source_id="scheduled_query",
            params={
                "query": query_str,
                "destination_table_name_template": f"{dest_table_id}{dest_table_name_template}",  # noqa: E501
                "write_disposition": write_disposition,
                "partitioning_field": partitioning_field,
            },
            schedule=schedule,
        )

        transfer_config_request = self.bq_datatransfer_client.create_transfer_config(
            bigquery_datatransfer.CreateTransferConfigRequest(
                parent=self._parent,
                transfer_config=transfer_config,
                service_account_name=self._service_account,
            )
        )
        logger.info(f"Created scheduled query {transfer_config_request.name}")
