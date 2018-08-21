# Native support for Fire TV in Home Assistant

No Python 2 service necessary!  And it can also handle device authentication.

**This is a work in progress!**


## Installation

Copy the `media_player/firetv.py` to your `custom_components` folder (`custom_components/media_player/firetv.py`).


## Configuration

```yaml
media_player:
- platform: firetv
  host: "192.168.0.21:5555"
  name: Fire TV 1
  adbkey: "/config/android/adbkey"

- platform: firetv
  host: "192.168.0.22:5555"
  name: Fire TV 2
```


## Current status / known issues

Currently, it seems to be working for me!  I'm able to connect to my Fire TV stick that doesn't have authentication *and* my Fire TV stick that does have it.


## Acknowledgments

This is based on [python-firetv](https://github.com/happyleavesaoc/python-firetv) by happyleavesaoc, and it depends on [python-adb](https://github.com/google/python-adb).
