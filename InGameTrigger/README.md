## In-game Trigger

## EEG acquisition types

To EEG data new column is added (`marker`) to indicate the event like `flash` or lack (`0`).

### Event oriented
The recorder toggle on N seconds before (not always supported) and toggle off N seconds after the event.

### Continuous
The recorder is always on. 

## Available Triggers

### Random Click Trigger
This option enables to trigger an event (like Flash) at random intervals. The user can specify the range of the intervals and the key to be pressed. In this way, the user can simulate a real-life scenario where the player is trolled by the game.

### Screenshot Triggered Markers
<img src="../imgs/kills-deaths-assits.png" alt="KDA" width="100" >

Levereges part of the screen to mark an event, when the view changes (player died, killed, etc). The user can seamlesly specify the region of the screen to be monitored (look at [tools](./tools/README.md)). 




### Usage

```shell
python ./main.py  --random_range=300,320,1 --key=d --filename=lol
```
