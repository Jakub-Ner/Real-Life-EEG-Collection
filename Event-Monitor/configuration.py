from src.utils.config_helpers import Config, EegChannel

def mean_band(row):
    return row.max(axis=0)

CONFIG = Config(
    TITLE="Event Monitor",
    REFRESH_DELAY=0.04, # seconds

    EEG_DATA_PATH="data.csv",
    EEG_BUFFER_SIZE=100,
    EEG_REALTIME=True,
    EEG_SAMPLING_RATE=25,
    EEG_CHANNELS=[
        # EegChannel("alpha", slice(16, 25, 1)),
        # EegChannel("beta", slice(17, 26, 1)),
        EegChannel("sin", slice(0, 1, 1)),
        EegChannel("cos", slice(1, 2, 1)),
    ],
    EEG_YTICKS=range(-1, 1, 1),
    EEG_AGGREGATION=mean_band,
    EEG_MARKERS={'0': 'none', '1': 'kill', '2': 'death'},

    EEG_PREDICTION=mean_band, # TODO: replace with model.predict

)
