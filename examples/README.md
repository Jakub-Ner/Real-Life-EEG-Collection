### Examples 

This package contains examples of how to leverage data collected with the use of Mind-Collector.

#### extract_heatmaps.py and extract_heatmaps.demo.ipynb
Enables for device channel selection and extraction of heatmaps (one per channel). y axis represents consecutive data rows, wheras x axis - frequency bands. See [example](./extract_heatmaps.demo.ipynb).

You can run the scipt for ALL recordings or specified one:
```bash
python extract_heatmaps.py ALL '../Mind-Collector/data/'
# or 
python extract_heatmaps.py ONE  '../Mind-Collector/data/lol_2024-08-04T21-10-29/eeg.csv'
```
