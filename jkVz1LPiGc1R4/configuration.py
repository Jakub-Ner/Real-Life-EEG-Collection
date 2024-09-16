from src.utils.config_helpers import Config, EegChannel


CONFIG = Config(
  EEG_PATH='./data.csv',
  EEG_CHANNELS=[
    EegChannel(name='AF3', columns=slice(0, 1)),
  ]
)
