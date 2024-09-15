from __future__ import annotations

from typing import Any, Tuple

import requests

from airflow.hooks.base import BaseHook
from retry import retry


class DatazoneHook(BaseHook):

    conn_name_attr = "datazone_conn_id"
    default_conn_name = "datazone_default"
    conn_type = "datazone"
    hook_name = "Datazone"
    api_prefix = "/api/v1"

    @classmethod
    def get_ui_field_behaviour(cls) -> dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ["port", "login", "schema"],
            "relabeling": {
                "password": "Datazone API Key",
            },
            "placeholders": {
                "extra": json.dumps(
                    {
                        "default_compute": "MEDIUM",
                    },
                    indent=4,
                ),
                "host": "https://app.datazone.co",
            },
        }

    def __init__(
        self,
        datazone_conn_id: str = "datazone_default",
    ) -> None:
        super().__init__()
        self.datazone_conn_id = datazone_conn_id
        self.base_url = None

    def get_conn(self, headers: dict[str, Any] | None = None) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        session = requests.Session()

        conn = self.get_connection(self.datazone_conn_id)
        host = conn.host

        if "://" not in host:
            host = f"https://{host}"

        if host.endswith("/"):
            host = host[:-1]

        self.base_url = f"{host}{self.api_prefix}"

        session.headers.update({"x-api-key": conn.password})
        if conn.extra:
            try:
                session.headers.update(conn.extra_dejson)
            except TypeError:
                self.log.warning("Connection to %s has invalid extra field.", conn.host)

        return session

    @retry(tries=3, delay=5)
    def get_user_me(self):
        """Get the current user"""
        session = self.get_conn()
        response = session.get(f"{self.base_url}/user/me")
        response.raise_for_status()
        return response.json()

    @retry(tries=3, delay=5)
    def run_execution(self, pipeline_id: str, run_config: dict[str, Any]) -> dict:
        """Run an execution"""
        session = self.get_conn()
        response = session.post(
            f"{self.base_url}/execution/run",
            json={
                "pipeline_id": pipeline_id,
                "run_config": run_config,
            },
        )
        response.raise_for_status()
        return response.json()

    @retry(tries=3, delay=5)
    def get_execution_logs(self, execution_id: str, cursor: str | None = None) -> dict:
        """Get the logs for an execution"""
        url = f"/execution/logs/{execution_id}"
        if cursor:
            url += f"?cursor={cursor}"

        session = self.get_conn()
        response = session.get(f"{self.base_url}{url}")
        response.raise_for_status()
        return response.json()

    def test_connection(self) -> Tuple[bool, str]:
        """Test a connection"""
        try:
            user = self.get_user_me()
            return True, f"Connection successfully tested for {user['email']}"
        except Exception as e:
            return False, str(e)
