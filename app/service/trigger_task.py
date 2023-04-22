from datetime import datetime
import multiprocessing
import os
import copy
import subprocess


class ConcurrentTask:

    def __init__(self):
        self.available_threads = multiprocessing.cpu_count() - 1

    def get_concurrent_num(self, num):
        return min(self.available_threads, num)

    @staticmethod
    def _cypress_task(task_group):
        env = os.environ.copy()
        env["PATH"] = "/usr/local/bin:" + env["PATH"]
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        process_id = os.getpid()
        log_file = f'test/log_{current_time}_{process_id}.txt'
        with open(log_file, "w") as f:
            subprocess.Popen(
                ['npm', 'run', 'cy:report', '--', '--spec', ",".join(task_group)],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd='/Users/steven/Desktop/dev/foundational-api-testing',
                env=env
            )

    def trigger_task(self, num_threads, task_group):
        print("available threads: ", self.available_threads)
        processes = list()
        if len(task_group) == num_threads:
            for i in range(num_threads):
                process = multiprocessing.Process(target=self._cypress_task, args=(task_group[i],))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()
