from yawl.workflows.bigquery_workflow import BigQueryWorkflowStep
from yawl.workflows.queue import queue

if __name__ == "__main__":
    step_1 = BigQueryWorkflowStep(
        sql="./example.sql",
        dest_table="project.dataset.table_1",
        squeduled_query_name="test_query_1",
        schedule="every mon,wed 09:00",
    )
    step_2 = BigQueryWorkflowStep(
        sql="./example.sql",
        dest_table="project.dataset.table_2",
        squeduled_query_name="test_query_2",
        schedule="every tue,thu 10:00",
    )
    with queue() as q:
        q.add(step_1).add(step_2).process()
