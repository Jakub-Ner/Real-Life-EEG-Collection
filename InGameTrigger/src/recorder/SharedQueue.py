from multiprocessing import Queue

from src.utils.logger import get_logger

logger = get_logger(__name__)


class SharedQueue:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_queues = {}

    def put(self, *args, **kwargs):
        for queue in self.output_queues.values():
            queue.put(*args, **kwargs)

    def create_output_for(self, worker_name: str) -> Queue:
        self.output_queues[worker_name] = Queue()
        logger.info(f"Created output queue for {worker_name}")
        return self.output_queues[worker_name]
