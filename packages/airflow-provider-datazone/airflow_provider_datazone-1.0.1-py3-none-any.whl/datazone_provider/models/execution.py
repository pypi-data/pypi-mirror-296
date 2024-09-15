from enum import Enum
from typing import List


class ExecutionStatus(str, Enum):
    CREATED = "CREATED"
    WAITING_UPSTREAMS = "WAITING_UPSTREAMS"
    UPSTREAM_FAILURE = "UPSTREAM_FAILURE"
    READY_TO_START = "READY_TO_START"
    NOT_STARTED = "NOT_STARTED"
    STARTING = "STARTING"
    STARTED = "STARTED"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CANCELING = "CANCELING"
    CANCELED = "CANCELED"


FINISHED_STATUSES: List[ExecutionStatus] = [
    ExecutionStatus.SUCCESS,
    ExecutionStatus.CANCELED,
    ExecutionStatus.FAILURE,
    ExecutionStatus.UPSTREAM_FAILURE,
]

PROBLEMATIC_STATUSES: List[ExecutionStatus] = [
    ExecutionStatus.FAILURE,
    ExecutionStatus.CANCELED,
    ExecutionStatus.UPSTREAM_FAILURE,
]
