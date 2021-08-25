"""
Read data from Google BigQuery
"""
from logging import getLogger

import google.cloud.bigquery as bigquery
from pandas.core.frame import DataFrame

logger = getLogger(__name__)


class BigQueryClient:
    """
    Client to read data from Google BigQuery
    """

    _bqclient = None

    @property
    def bqclient(self) -> bigquery.Client:
        """
        Google BigQuery API Client
        """

        if self._bqclient is None:
            self._bqclient = bigquery.Client()

        return self._bqclient

    def query(
        self, query_string: str, dest_table_id: str, allow_large_results: bool = False
    ) -> DataFrame:
        """
        Executes query loading into a destination table.
        """
        job_config = bigquery.QueryJobConfig(destination=dest_table_id)

        result = self.bqclient.query(
            query_string, job_config=job_config, allow_large_results=allow_large_results
        ).result()

        logger.info(f"Query results loaded to the table {dest_table_id}")
        return result
