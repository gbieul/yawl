"""
Read data from Google BigQuery
"""
import google.cloud.bigquery as bigquery
from pandas.core.frame import DataFrame


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

    def query(self, query_string: str) -> DataFrame:
        """
        Execute query returning dataframe with results
        """

        dataframe = self.bqclient.query(query_string).result().to_dataframe()

        return dataframe

    def load(
        self, table_id: str, job_config: bigquery.LoadJobConfig, dataframe: DataFrame
    ) -> None:
        """
        Load data on BigQuery table
        """

        job = self.bqclient.load_table_from_dataframe(
            dataframe, table_id, job_config=job_config
        )
        job.result()  # Wait for the job to complete.
