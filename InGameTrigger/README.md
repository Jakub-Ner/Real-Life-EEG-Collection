## In-game Trigger

## Available Recorders

Recorder is a Process that listens for incoming events emited by triggers. It is responsible for collecting and annotating data. You can run multiple recorders at the same time.

### EEG Recorder
Wrapper around EEG Streamer. Currently only UDPStreamer is implemented.

## Available Triggers

A trigger is a process that creates events based on certain inputs. These inputs can come from a user (like facial expressions), a game (such as a scoreboard update), or the trigger itself (like simulating a button click). You can have several triggers running simultaneously.

### Screenshot Triggered Markers
<img src="../imgs/kills-deaths-assits.png" alt="KDA" width="100" >

Levereges part of the screen to mark an event, when the view changes (player died, killed an enemy, etc). The user can seamlesly specify the region of the screen to be monitored (look at [tools](./tools/README.md)). 

After specifying the region, the process takes screenshots at a fixed interval and compares the images. If the images are different, the process triggers an event. This is useful to monitor the player's performance in a game, like League of Legends, where the player's KDA (Kills, Deaths, Assists) is always displayed on the screen.

<p>
    <img src="../imgs/before-killing.png" alt="KDA" width="100" >
    <img src="../imgs/after-killing.png" alt="KDA" width="100" >
</p>


### Random Click Trigger
This option enables to trigger an event (like Flash) at random intervals. The user can specify the range of the intervals and the key to be pressed. In this way, the user can simulate a real-life scenario where the player is trolled by the game.


### Usage

```shell
python ./main.py
```
