from src.utils.config_helpers import Config, EegChannel

def mean_band(row):
    return row.mean(axis=0)

CONFIG = Config(
    TITLE="Event Monitor",
    REFRESH_DELAY=300,

    EEG_DATA_PATH="../Mind-Collector/data/lol_2024-08-08T16-38-51/eeg.csv",
    EEG_BUFFER_SIZE=100,
    EEG_REALTIME=False,
    EEG_SAMPLING_RATE=25,
    EEG_CHANNELS=[
        EegChannel("alpha", slice(16, 25, 1)),
        EegChannel("beta", slice(17, 26, 1)),
    ],
    EEG_AGGREGATION=mean_band,
    EEG_MARKERS={'0': 'none', '1': 'kill', '2': 'death'},

    EEG_PREDICTION=mean_band, # TODO: replace with model.predict

)
