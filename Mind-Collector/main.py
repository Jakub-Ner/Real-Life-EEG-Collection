from fire import Fire
from multiprocessing import Process

from configuration import CONFIG
from src.utils.SharedQueue import SharedQueue
from src.utils.logger import get_logger

logger = get_logger(__name__)


def init_triggers(recorder_jobs: SharedQueue) -> list[Process]:
    triggers = []

    for trigger_config in CONFIG.triggers:
        triggers.append(
            trigger_config.CLASS(
                trigger_config.CONFIG,
                recorder_jobs,
            )
        )
    return triggers


def init_recorders(recorder_jobs: SharedQueue) -> list[Process]:
    recorders = []
    for recorder_config in CONFIG.recorders:
        recorders.append(
            recorder_config.CLASS(
                recorder_config.CONFIG,
                recorder_jobs.create_output_for(recorder_config.CLASS.__name__),
            )
        )
    return recorders


def main():
    logger.info(f"Initiating In-game Trigger")

    CONFIG.general.initialize() 
    recorder_jobs = SharedQueue()

    recorders = init_recorders(recorder_jobs)
    triggers = init_triggers(recorder_jobs)

    for recorder in recorders:
        recorder.start()
    for trigger in triggers:
        trigger.start()

    try:
        for recorder in recorders:
            recorder.join()
        for trigger in triggers:
            trigger.join()

    except KeyboardInterrupt:
        for recorder in recorders:
            recorder.terminate()
        for trigger in triggers:
            trigger.terminate()
        logger.info("All triggers stopped by user")


if __name__ == "__main__":
    Fire(main)
