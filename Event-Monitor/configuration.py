import numpy as np
from src.utils.config_helpers import Config, PlotArgument, PlotFragmentConfig

def mean_band(row: np.ndarray) -> np.ndarray:
    # print(row)
    # print(row.shape)
    return row.max(axis=1)

import onnxruntime as rt
MODEL_PATH = "classifiers/svm-without-preprocessing-90p.onnx"

session = rt.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
label_name = [o.name for o in session.get_outputs()]

def predict(row: np.ndarray) -> np.ndarray:
    # print(row.astype(np.float32))
    # print(input_name)

    prediction = np.array(session.run(label_name, {input_name: row.astype(np.float32).reshape(1, -1)})[0])
    # print(prediction)
    return prediction

EEG_CHANNELS = [
    PlotArgument("alpha", slice(16, 24, 1)),
    PlotArgument("beta-low", slice(24, 32, 1)),
    PlotArgument("beta-mid", slice(32, 40, 1)),
    PlotArgument("beta-high", slice(40, 48, 1)),
    PlotArgument("gamma", slice(48, 56, 1)),
]

DATA_FRAGMENT_CONFIG = PlotFragmentConfig(
    EEG_YTICKS=range(10, 30, 5),
    PLOT_FUNCTION=mean_band,
    ARGUMENTS=EEG_CHANNELS,
    # X_NUMBER=6, # 5 channels + 1 marker
)

PREDICT_FRAGMENT_CONFIG = PlotFragmentConfig(
    EEG_YTICKS=np.linspace(-0.1, 2.1, num=3),
    PLOT_FUNCTION=predict,
    ARGUMENTS=[PlotArgument("prediction", slice(0, 1, 1))],
    # X_NUMBER=2, # 1 prediction + 1 marker
)

CONFIG = Config(
    DATA_FRAGMENT=DATA_FRAGMENT_CONFIG,
    PREDICT_FRAGMENT=PREDICT_FRAGMENT_CONFIG,
    TITLE="Event Monitor",
    REFRESH_DELAY=0.1, # seconds

    EEG_DATA_PATH="./eeg.csv.out",
    EEG_BUFFER_SIZE=100,
    EEG_REALTIME=True,
    EEG_SAMPLING_RATE=25,
    MARKERS={'1': 'kill', '2': 'death'},
    EEG_CHANNELS=EEG_CHANNELS,


)
