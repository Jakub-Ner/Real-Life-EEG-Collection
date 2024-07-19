from multiprocessing import Process, Queue

from time import sleep

from src.utils.logger import get_logger

logger = get_logger(__name__)


class SharedQueue:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_queues = {}

    def put(self, *args, **kwargs):
        for queue in self.output_queues.values():
            queue.put(*args, **kwargs)

    def create_output_for(self, worker_name: str):
        self.output_queues[worker_name] = Queue()
        logger.info(f"Created output queue for {worker_name}")
        return self.output_queues[worker_name]


class Node(Process):
    def __init__(self, name, worker_jobs):
        super().__init__()
        self.name = name
        self.worker_jobs = worker_jobs

    def run(self):
        print(f"{self.name} is running")

        i = 0
        while True:
            print(f"{self.name} puts new task {i}")
            self.worker_jobs.put(f"Task {i}")
            sleep(1)
            i += 1


class Worker(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def set_jobs(self, jobs: Queue):
        self.jobs = jobs

    def run(self):
        assert hasattr(
            self, "jobs"
        ), "Jobs attribute must be set before running the worker"

        print(f"{self.name} is running")

        while True:
            print(f"{self.name} is working")
            print(self.jobs.get())
            sleep(1)


jobs = SharedQueue()
w = Worker("Worker1")
w2 = Worker("Worker2")

w.set_jobs(jobs.create_output_for(getattr(w, "name")))
w2.set_jobs(jobs.create_output_for(getattr(w2, "name")))

n = Node("Node", jobs)

if __name__ == "__main__":

    w.start()
    w2.start()
    n.start()

    n.join()
    w.join()
    w2.join()
