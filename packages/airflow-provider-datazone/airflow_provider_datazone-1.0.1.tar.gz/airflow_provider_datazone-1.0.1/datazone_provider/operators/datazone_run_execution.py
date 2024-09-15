from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any, Dict

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator

from datazone_provider.hooks.datazone import DatazoneHook
from datazone_provider.models.execution import FINISHED_STATUSES, PROBLEMATIC_STATUSES

if TYPE_CHECKING:
    from airflow.utils.context import Context


class DatazoneRunExecutionOperator(BaseOperator):
    ui_color = "#FCE7F3"

    def __init__(
        self,
        *,
        datazone_conn_id: str = DatazoneHook.default_conn_name,
        pipeline_id: str,
        run_config: Dict[str, Any],
        retries: int = 0,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs, retries=retries)
        self.datazone_conn_id = datazone_conn_id
        self.pipeline_id = pipeline_id
        self.run_config = run_config

    def execute(self, context: Context) -> Any:
        hook = DatazoneHook(datazone_conn_id=self.datazone_conn_id)
        execution = hook.run_execution(pipeline_id=self.pipeline_id, run_config=self.run_config)

        print(f"Execution started with id {execution.get('id')}")

        status = execution.get("status")
        cursor = None
        while status not in FINISHED_STATUSES:
            logs = hook.get_execution_logs(execution.get("id"), cursor=cursor)
            cursor = logs.get("cursor")
            status = logs.get("status")
            for log in logs.get("logs"):
                print(log["message"])

            time.sleep(5)
        if status in PROBLEMATIC_STATUSES:
            raise AirflowException(f"Execution failed with status {status}. Check datazone logs for more information.")

        return execution
