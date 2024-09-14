from __future__ import annotations

from typing import Any, Tuple

import requests
from requests.auth import HTTPBasicAuth

from airflow.hooks.base import BaseHook


class DatazoneHook(BaseHook):

    conn_name_attr = "datazone_conn_id"
    default_conn_name = "datazone_default"
    conn_type = "datazone"
    hook_name = "DatazoneHook"

    @staticmethod
    def get_connection_form_widgets() -> dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField

        return {
            "api_key": PasswordField(lazy_gettext("API Key"), widget=BS3PasswordFieldWidget()),
        }

    @staticmethod
    def get_ui_field_behaviour() -> dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ["port", "password", "login", "schema"],
            "relabeling": {},
            "placeholders": {
                "extra": json.dumps(
                    {
                        "example_parameter": "parameter",
                    },
                    indent=4,
                ),
                "api_key": "API Key",
                "host": "https://app.datazone.co",
            },
        }

    def __init__(
        self,
        datazone_conn_id: str = "datazone",
        method: str = "POST",
        auth_type: Any = HTTPBasicAuth,
    ) -> None:
        super().__init__()
        self.datazone_conn_id = datazone_conn_id
        self.method = method.upper()
        self.base_url: str = ""
        self.auth_type: Any = auth_type

    def get_conn(self, headers: dict[str, Any] | None = None) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        session = requests.Session()

        if self.datazone_conn_id:
            conn = self.get_connection(self.datazone_conn_id)

            if conn.host and "://" in conn.host:
                self.base_url = conn.host
            else:
                # schema defaults to HTTP
                schema = conn.schema if conn.schema else "http"
                host = conn.host if conn.host else ""
                self.base_url = schema + "://" + host

            if conn.port:
                self.base_url = self.base_url + ":" + str(conn.port)
            if conn.login:
                session.auth = self.auth_type(conn.login, conn.password)
            if conn.extra:
                try:
                    session.headers.update(conn.extra_dejson)
                except TypeError:
                    self.log.warning("Connection to %s has invalid extra field.", conn.host)
        if headers:
            session.headers.update(headers)

        return session

    def run(
        self,
        endpoint: str | None = None,
        data: dict[str, Any] | str | None = None,
        headers: dict[str, Any] | None = None,
        **request_kwargs,
    ) -> Any:
        """
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """

        session = self.get_conn(headers)

        if self.base_url and not self.base_url.endswith("/") and endpoint and not endpoint.startswith("/"):
            url = self.base_url + "/" + endpoint
        else:
            url = (self.base_url or "") + (endpoint or "")

        if self.method == "GET":
            # GET uses params
            req = requests.Request(self.method, url, headers=headers)
        else:
            # Others use data
            req = requests.Request(self.method, url, data=data, headers=headers)

        prepped_request = session.prepare_request(req)

        self.log.info("Sending %r to url: %s", self.method, url)

        try:
            response = session.send(prepped_request)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning("%s Tenacity will retry to execute the operation", ex)
            raise ex

    def test_connection(self) -> Tuple[bool, str]:
        """Test a connection"""
        try:
            self.run()
            return True, "Connection successfully tested"
        except Exception as e:
            return False, str(e)
