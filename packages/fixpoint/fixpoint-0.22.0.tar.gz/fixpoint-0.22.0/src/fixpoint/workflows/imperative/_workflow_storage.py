"""Storage for workflow metadata (runs, attempts, etc.)"""

__all__ = [
    "WorkflowStorage",
    "InMemWorkflowStorage",
    "OnDiskWorkflowStorage",
    "WorkflowRunAttemptData",
]

import datetime
import sqlite3
from typing import Dict, Optional, Protocol, Tuple

from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field

from fixpoint._storage.definitions import WORKFLOW_RUN_ATTEMPTS_SQLITE_TABLE
from fixpoint._storage.sql import ParamNameKind, param


class WorkflowRunAttemptData(BaseModel):
    """Data about a workflow run attempt"""

    attempt_id: str
    workflow_id: str
    workflow_run_id: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class WorkflowStorage(Protocol):
    """Protocol for storing workflow metadata (runs, attempts, etc.)"""

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the latest stored workflow run attempt"""

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""


class InMemWorkflowStorage(WorkflowStorage):
    """Stores workflow run and attempt data in memory

    In-memory workflow only works for a single org_id, so it just ignores the
    `org_id` arguments in its methods.
    """

    # key is run ID
    _runs: Dict[Tuple[str, str], WorkflowRunAttemptData]

    def __init__(self) -> None:
        self._runs: Dict[Tuple[str, str], WorkflowRunAttemptData] = {}

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the stored workflow run"""
        return self._runs.get((workflow_id, workflow_run_id), None)

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""
        self._runs[(workflow_run.workflow_id, workflow_run.workflow_run_id)] = (
            workflow_run
        )


def _get_workflow_run_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    workflow_id: str,
    workflow_run_id: str,
) -> Tuple[str, Dict[str, str]]:
    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        SELECT id, workflow_id, workflow_run_id FROM {table}
        WHERE
            workflow_id = {_param("workflow_id")}
            AND workflow_run_id = {_param("workflow_run_id")}
            AND org_id = {_param("org_id")}
        ORDER BY created_at DESC
        LIMIT 1
        """
    args = {
        "workflow_id": workflow_id,
        "workflow_run_id": workflow_run_id,
        "org_id": org_id,
    }
    return query, args


def _store_workflow_run_query(
    kind: ParamNameKind, table: str, org_id: str, workflow_run: WorkflowRunAttemptData
) -> Tuple[str, Dict[str, str]]:
    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
        INSERT INTO {table}
            (id, workflow_id, workflow_run_id, org_id)
        VALUES ({','.join(_param(pn) for pn in ["id", "workflow_id", "workflow_run_id", "org_id"])})
        """
    args = {
        "id": workflow_run.attempt_id,
        "workflow_id": workflow_run.workflow_id,
        "workflow_run_id": workflow_run.workflow_run_id,
        "org_id": org_id,
    }
    return query, args


class PostgresWorkflowStorage(WorkflowStorage):
    """Stores workflow run and attempt data in a Postgres database"""

    _pool: ConnectionPool

    def __init__(self, pool: ConnectionPool) -> None:
        self._pool = pool

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the latest stored workflow run attempt"""
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                query, args = _get_workflow_run_query(
                    ParamNameKind.POSTGRES,
                    "fixpoint.workflow_run_attempts",
                    org_id,
                    workflow_id,
                    workflow_run_id,
                )
                cursor.execute(query, args)
                row = cursor.fetchone()
                if row is None:
                    return None
                attempt_id, wfid, wfrunid = row

        return WorkflowRunAttemptData(
            attempt_id=attempt_id,
            workflow_id=wfid,
            workflow_run_id=wfrunid,
        )

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                query, args = _store_workflow_run_query(
                    ParamNameKind.POSTGRES,
                    "fixpoint.workflow_run_attempts",
                    org_id,
                    workflow_run,
                )
                cursor.execute(query, args)
            conn.commit()


class OnDiskWorkflowStorage(WorkflowStorage):
    """Stores workflow run and attempt data on disk"""

    _conn: sqlite3.Connection

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> None:
        with self._conn:
            self._conn.execute(WORKFLOW_RUN_ATTEMPTS_SQLITE_TABLE)

    def get_workflow_run(
        self, org_id: str, workflow_id: str, workflow_run_id: str
    ) -> Optional[WorkflowRunAttemptData]:
        """Gets the stored workflow run"""
        with self._conn:
            query, args = _get_workflow_run_query(
                ParamNameKind.SQLITE,
                "workflow_run_attempts",
                org_id,
                workflow_id,
                workflow_run_id,
            )
            cursor = self._conn.execute(query, args)
            row = cursor.fetchone()
            if row is None:
                return None
            attempt_id, wfid, wfrunid = row

        return WorkflowRunAttemptData(
            attempt_id=attempt_id,
            workflow_id=wfid,
            workflow_run_id=wfrunid,
        )

    def store_workflow_run(
        self, org_id: str, workflow_run: WorkflowRunAttemptData
    ) -> None:
        """Stores the workflow run"""
        with self._conn:
            query, args = _store_workflow_run_query(
                ParamNameKind.SQLITE,
                "workflow_run_attempts",
                org_id,
                workflow_run,
            )
            self._conn.execute(query, args)
