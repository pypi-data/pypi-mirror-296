import heapq
import time
import asyncio
import logging
from croniter import croniter


logger = logging.getLogger(__name__)


class CronJob:
    def __init__(self, async_func, cron, args=None, kwargs=None, name=None) -> None:
        self.async_func = async_func
        self.cron = cron
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.name = name


class LightweightCron:
    """
    currently this is a static cron schedule
    wait exact time then trigger the earliest job
    """

    def __init__(self, jobs) -> None:
        self._jobs = jobs
        if not self._jobs:
            raise Exception("jobs are required")

    def _init_jobs(self):
        """
        add jobs to headq
        add idx to break tie for headq
        """
        q = []
        curr_ts = time.time()
        for idx, job in enumerate(self._jobs):
            iter = croniter(job.cron, curr_ts)
            q.append((int(iter.get_next()), idx, iter, job, None))
        heapq.heapify(q)

        return q

    async def run(self):
        # init jobs
        q = self._init_jobs()

        while True:
            curr_ts = int(time.time())
            run_ts, idx, iter, job, _ = q[0]
            # logger.info(f"run_ts={run_ts}, curr_ts={curr_ts}, job={job.name}")
            if run_ts > curr_ts:
                # wait until first job can run
                # logger.info(f"wait {run_ts - curr_ts} seconds")
                await asyncio.sleep(run_ts - curr_ts)
            else:
                # run job
                task = asyncio.create_task(job.async_func(*job.args, **job.kwargs), name=job.name)

                # add job next
                heapq.heapreplace(q, (int(iter.get_next()), idx, iter, job, task))

                # let tasks run
                await asyncio.sleep(0)
