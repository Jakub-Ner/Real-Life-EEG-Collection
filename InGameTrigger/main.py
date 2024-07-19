from fire import Fire

from configuation import CONFIG
from src.recorder.eeg.utils.helpers import Recorder
from src.recorder.SharedQueue import SharedQueue
from src.randomClick.RandomClick import RandomClick
from src.recorder.eeg.EEGRecorder import EEGRecorder
from src.utils.common import AbstractTrigger, get_now
from src.utils.logger import get_logger

logger = get_logger(__name__)


def init_triggers(recorder_jobs) -> list[AbstractTrigger]:
    triggers = []

    if CONFIG.randomClick:
        triggers.append(
            RandomClick(
                CONFIG.randomClick.RANDOM_RANGE,
                CONFIG.randomClick.KEY,
                recorder_jobs,
            )
        )

    if CONFIG.ssMarkers:
        for marker in CONFIG.ssMarkers:
            ...
        # triggers.append(ScreenshotMarker(marker.top, marker.bottom, marker.marker, marker.delay_s))
    return triggers


# @assert_udp
def main(randomClickOn: bool | None = None, ssMarkerOn: bool | None = None):

    if randomClickOn and not CONFIG.randomClick:
        logger.warning("Random click lacks configuration, it won't start")

    if ssMarkerOn and not CONFIG.ssMarkers:
        logger.warning("Screenshot markers lacks configuration, it won't start")

    logger.info(f"Initiating In-game Trigger {get_now()}")

    recorder_jobs = SharedQueue()

    recorders: list[Recorder] = [
        EEGRecorder(
            CONFIG.general.FILENAME_PREFIX,
            recorder_jobs.create_output_for(CONFIG.general.FILENAME_PREFIX),
        ),
    ]
    triggers = init_triggers(recorder_jobs)

    for recorder in recorders:
        recorder.start()
    for trigger in triggers:
        print(trigger)
        trigger.start()

    try:
        for recorder in recorders:
            recorder.join()
        for trigger in triggers:
            trigger.join()
    except KeyboardInterrupt:

        for recorder in recorders:
            recorder.join()
        for trigger in triggers:
            trigger.terminate()
        logger.info("All triggers stopped by user")


if __name__ == "__main__":
    Fire(main)
