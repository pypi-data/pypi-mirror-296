# copyright 2016-2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-celerytask automatic tests base class"""

import os
import sys
import multiprocessing
import time

import redis
import celery
import celery.result

from cubicweb.devtools import testlib
from cubicweb_celerytask.ccplugin import CeleryMonitorCommand


class BaseCeleryTaskTC(testlib.CubicWebTC):
    worker_args = [
        "worker_concurrency=1",
        "worker_pool=solo",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        REDIS_URL = os.environ.get("PIFPAF_REDIS_URL", "redis://localhost:6379/1")
        redis_client = redis.Redis.from_url(REDIS_URL)
        redis_client.flushall()
        task_module_path = cls.datapath("tasks")
        sys.path.insert(0, task_module_path)
        conf = celery.current_app.conf
        conf.broker_url = REDIS_URL
        conf.result_backend = REDIS_URL
        conf.CUBICWEB_CELERYTASK_REDIS_URL = REDIS_URL
        conf.task_always_eager = False
        conf.imports = ("cw_celerytask_helpers.helpers", "tasks")
        # this is required since we use a non-cubicweb worker, so the startup
        # hook setting CUBICWEB_CELERYTASK_LOGDIR won't run.
        conf.CUBICWEB_CELERYTASK_LOGDIR = os.path.join(cls.config.appdatahome, "logs")
        cls.worker = multiprocessing.Process(target=cls.start_worker)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.worker.terminate()
        cls.worker.join()

    @classmethod
    def start_worker(cls):
        app = celery.current_app
        app.config_from_cmdline(cls.worker_args, namespace="worker")
        worker = app.Worker()
        worker.start()

    def wait_async_task(self, cnx, task_id, timeout=5):
        result = celery.result.AsyncResult(task_id)
        start = time.time()
        while abs(time.time() - start) < timeout:
            if result.ready():
                CeleryMonitorCommand.loop(cnx, timeout=0)
                return result
            if not self.worker.is_alive():
                # will be joined in tearDown
                raise RuntimeError("Celery worker terminated")
            time.sleep(0.1)
        raise RuntimeError("Timeout")
