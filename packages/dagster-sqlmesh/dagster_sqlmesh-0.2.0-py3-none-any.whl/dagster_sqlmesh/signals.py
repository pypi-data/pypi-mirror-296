import logging
from sqlmesh.core.scheduler import Signal

from sqlmesh.core.scheduler import Batch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DagsterSource(Signal):
    # concrete implementation of abstraction method from Signal
    def check_intervals(self, batch: Batch) -> bool | Batch:
        """ "Filter the batch to only return the intervals for which the file exists"""
        logger.debug("batches")
        logger.debug(batch)
        return True


def signal_factory(signal_meta: dict[str, str | int | float | bool]) -> Signal:
    kind = str(signal_meta.get("kind", ""))
    if kind.lower() == "dagstersource":
        return DagsterSource()
    logger.debug(signal_meta)
    raise ValueError("unknown signal")
