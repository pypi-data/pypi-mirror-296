"""Task definitions for the Vantage Agent."""

from apscheduler.job import Job
from apscheduler.schedulers.base import BaseScheduler

from vantage_agent.logicals.health import report_health_status
from vantage_agent.logicals.scontrol import (
    upload_scontrol_config,
    upload_scontrol_node,
    upload_scontrol_partition,
)
from vantage_agent.logicals.update import self_update_agent
from vantage_agent.settings import SETTINGS


def cluster_config_task(scheduler: BaseScheduler) -> Job:
    """Schedule a task to report the cluster config."""
    return scheduler.add_job(upload_scontrol_config, "interval", seconds=SETTINGS.TASK_JOBS_INTERVAL_SECONDS)


def cluster_partition_task(scheduler: BaseScheduler) -> Job:
    """Schedule a task to report the cluster config."""
    return scheduler.add_job(
        upload_scontrol_partition, "interval", seconds=SETTINGS.TASK_JOBS_INTERVAL_SECONDS
    )


def cluster_node_task(scheduler: BaseScheduler) -> Job:
    """Schedule a task to report the cluster config."""
    return scheduler.add_job(upload_scontrol_node, "interval", seconds=SETTINGS.TASK_JOBS_INTERVAL_SECONDS)


def self_update_task(scheduler: BaseScheduler) -> Job:
    """Schedule a task to self update the agent every ``TASK_SELF_UPDATE_INTERVAL_SECONDS`` seconds."""
    if SETTINGS.TASK_SELF_UPDATE_INTERVAL_SECONDS is None:
        return None
    return scheduler.add_job(
        self_update_agent, "interval", seconds=SETTINGS.TASK_SELF_UPDATE_INTERVAL_SECONDS
    )


def status_report_task(scheduler: BaseScheduler) -> Job:
    """Schedule a task to report the status."""
    return scheduler.add_job(report_health_status, "interval", seconds=SETTINGS.TASK_JOBS_INTERVAL_SECONDS)
