import numpy as np
from src.utils.config_helpers import Config, EegChannel

def mean_band(row: np.ndarray) -> np.ndarray:
    print(row)
    print(row.shape)
    return row.max(axis=1)

import onnxruntime as rt
MODEL_PATH = "classifiers/svm-without-preprocessing-90p.onnx"

session = rt.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
label_name = [o.name for o in session.get_outputs()]

def predict(row: np.ndarray) -> np.ndarray:
    print(row.astype(np.float32))
    print(input_name)

    return np.array(session.run(label_name, {input_name: row.astype(np.float32).reshape(1, -1)})[0])

CONFIG = Config(
    TITLE="Event Monitor",
    REFRESH_DELAY=0.1, # seconds

    EEG_DATA_PATH="../Mind-Collector/data/lol_2024-09-16T16-43-59/eeg.csv",
    EEG_BUFFER_SIZE=100,
    EEG_REALTIME=True,
    EEG_SAMPLING_RATE=25,
    EEG_CHANNELS=[
        EegChannel("alpha", slice(16, 24, 1)),
        EegChannel("beta-low", slice(24, 32, 1)),
        EegChannel("beta-mid", slice(32, 40, 1)),
        EegChannel("beta-high", slice(40, 48, 1)),
        EegChannel("gamma", slice(48, 56, 1)),
        # EegChannel("sin", slice(0, 1, 1)),
        # EegChannel("cos", slice(1, 2, 1)),
    ],
    EEG_YTICKS=range(25, 50, 5),
    EEG_AGGREGATION=mean_band,
    EEG_MARKERS={'0': 'none', '1': 'kill', '2': 'death'},

    EEG_PREDICTION=predict, # TODO: replace with model.predict

)
