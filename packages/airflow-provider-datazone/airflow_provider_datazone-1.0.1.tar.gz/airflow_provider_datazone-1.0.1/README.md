<p align="center">
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://framerusercontent.com/images/hKDe0OtgNAvok8JZ0I6HSY8It0Y.png?scale-down-to=512" width="60" style="margin-right: 30px"/>
  </a>
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" width="60" />
  </a>
</p>
<h1 align="center">
  Airflow Datazone Provider
</h1>
  <h3 align="center">
    A provider package for Apache Airflow that provides a set of operators and hooks to interact with Datazone.
</h3>

## Installation

You can install this package using `pip`:

```bash
pip install airflow-datazone-provider
```

## Usage


### Creating a connection

To integrate with Datazone on Airflow, you can create a connection in the Airflow UI with the following parameters:

- **Conn Id**: `<your_conn_id>`
- **Conn Type**: `Datazone`
- **Host**: `<your_datazone_host>`
- **API Key**: `<your_datazone_api_key>`
- **Extra**: Optional extra parameters in JSON format. For example, to specify a compute, you can use the following JSON:

```json
{
    "compute": "XSMALL"
}
```


### DatazoneRunExecutionOperator

The `DatazoneRunExecutionOperator` is an operator that allows you to run an execution on Datazone.

```python
from airflow import DAG
from datazone_provider.operators.datazone_run_execution import DatazoneRunExecutionOperator
from datetime import datetime

dag = DAG(
    "my_dag",
    start_date=datetime(2021, 1, 1),
    schedule_interval=None
)

dz_task = DatazoneRunExecutionOperator(
    dag=dag,
    task_id="run_datazone_execution",
    conn_id="<your_conn_id>",
    pipeline_id="<your_pipeline_id>",
    run_config={
        "compute": "XSMALL",
        "env_vars": {
            "DEMO_KEY": "DEMO_VALUE"
        }
    }
)

dz_task
```
