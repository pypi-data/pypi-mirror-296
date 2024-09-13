"""Core module for defining the self update logic for the Vantage Agent."""

import re
import subprocess
import sys
from importlib.metadata import version

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from vantage_agent.scheduler import schedule_tasks, scheduler
from vantage_agent.vantage_api_client import backend_client

package_name = "vantage_agent"


async def _fetch_upstream_version_info() -> str:
    logger.debug("Fetching the upstream version info from vantage API")
    response = await backend_client.get("/cluster/openapi.json")
    response.raise_for_status()

    data = response.json()
    upstream_version: str = data["info"]["version"]
    return upstream_version


def _need_update(current_version: str, upstream_version: str) -> bool:
    """Compare the current version with the upstream version.

    In case the current version is the same as the upstream version, return False.
    If the major versions are different, return False, as updates across major versions are not desired.
    Otherwise, return True, allowing updates and rollbacks across all minor and patch versions,
    including handling for pre-release versions ('a' for alpha, 'b' for beta).
    """
    current_major: int | str
    current_minor: int | str
    current_patch: int | str
    upstream_major: int | str
    upstream_minor: int | str
    upstream_patch: int | str

    # regular expression to parse version strings: major.minor.patch
    version_pattern = r"^(\d+)\.(\d+)\.(\d+)$"

    current_match = re.match(version_pattern, current_version)
    upstream_match = re.match(version_pattern, upstream_version)

    if not current_match or not upstream_match:
        raise ValueError(
            f"One of the following versions are improperly formatted: {current_version}, {upstream_version}"
        )

    current_major, current_minor, current_patch = current_match.groups()
    upstream_major, upstream_minor, upstream_patch = upstream_match.groups()

    current_major, current_minor, current_patch = map(int, [current_major, current_minor, current_patch])
    upstream_major, upstream_minor, upstream_patch = map(
        int, [upstream_major, upstream_minor, upstream_patch]
    )

    # major version check
    if current_major != upstream_major:
        return False
    # minor and patch version check
    elif current_minor != upstream_minor or current_patch != upstream_patch:
        return True
    return False


def _update_package(version: str) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", f"{package_name}=={version}"])


async def self_update_agent() -> None:
    """Fetch the upstream version and update the agent if necessary.

    In case the agent is updated, the scheduler is shutdown and restarted with the new version.
    """
    global scheduler

    current_version = version(package_name)
    upstream_version = await _fetch_upstream_version_info()
    logger.debug(
        f"Vantage Agent version info: current_version={current_version}, upstream_version={upstream_version}"
    )

    if _need_update(current_version, upstream_version):
        logger.warning(
            "The Vantage Agent is outdated in relation to the upstream version; an update is required."
        )

        logger.debug("Shutting down the scheduler...")
        scheduler.shutdown(wait=False)

        logger.debug("Clearing the scheduler jobs...")
        scheduler_jobs: list[Job] = scheduler.get_jobs()
        for job in scheduler_jobs:
            job.remove()

        logger.debug(f"Updating {package_name} from version {current_version} to {upstream_version}...")
        _update_package(upstream_version)
        logger.debug("Update completed successfully.")

        logger.debug(f"Loading plugins from version {upstream_version}...")
        new_scheduler = AsyncIOScheduler()
        schedule_tasks(new_scheduler)
        new_scheduler.start()
        logger.debug("Plugins loaded successfully.")

        logger.info("Replacing the scheduler with the new version...")
        scheduler = new_scheduler
    else:
        logger.debug("No update is required or update crosses a major version divide.")
