import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os
from fire import Fire

def show_statistics(markers):
  marker_names = np.unique(markers)
  for marker_name in marker_names:
    print(f"Marker {marker_name}:", markers[markers == marker_name].count())

def read_eeg_data(path) -> tuple[np.ndarray, pd.Series]:
  df = pd.read_csv(path)
  markers = df.iloc[:, -1]
  data = df.iloc[:, 16:56] / 30.0 # take only alpha, beta, gamma and normalize values to 0-1
  return data.to_numpy(), markers

def get_channel(data, channel):
  """
  Unicorn device has 8 channels (1-8).
  """
  channel -= 1
  return data[:, channel::8]

def prepare_images(data, channels, markers, event, duration, freqs=5) -> list[np.ndarray]:
    img = np.zeros((duration, freqs, len(channels)))
    imgs = []
    for event_idx in markers[markers == event].index:
        for i, channel in enumerate(channels):
            img[:, :, i] = get_channel(data, channel)[event_idx:event_idx+duration, :]
        imgs.append(img)
    return imgs

def preview_image(img, channels, event):
    _, axes = plt.subplots(1, len(channels), figsize=(15, 5))
    for i, channel in enumerate(channels):
        axes[i].imshow(img[:, :, i], cmap='gray')
        axes[i].set_title(f'{event} event for channel {channel}')
        axes[i].set_xticks(np.arange(5), ['alpha', 'beta-low', 'mid-beta', 'beta-high', 'gamma'], rotation=90)
        axes[i].set_ylabel('Time')
    plt.show()

def extract_event_types(markers):
  u = np.unique(markers)
  return u[u != '0']

def get_prefix(path):
  return f"{path.split('/')[-1].split('.')[0]}"

def save_images(imgs: list[np.ndarray], out_folder: str, prefix: str):
    os.makedirs(out_folder, exist_ok=True)

    for i, img in enumerate(imgs):
        path = os.path.join(out_folder, f'{prefix}_{i}.png')
        cv2.imwrite(path, (img * 255).astype(np.uint8))

def extract_heatmaps(eeg_path: str, out_folder: str='./data/heatmaps', duration: int=20, channels: list[int]=[1,2,3,4]):
  data, markers = read_eeg_data(eeg_path)
  show_statistics(markers)

  events = extract_event_types(markers)

  for event in events:
    imgs = prepare_images(data, channels, markers, event, duration)
    save_images(imgs, os.path.join(out_folder, event), get_prefix(eeg_path))

if __name__ == '__main__':
  Fire(extract_heatmaps)