# Native support for Fire TV in Home Assistant

No Python 2 service necessary!  And it can also handle device authentication.

**This is a work in progress!**


## Installation

Copy the `adb` folder and the files `python_firetv.py` and `media_player/firetv.py` to your `custom_components` folder.


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

I can get the media players to show up in Home Assistant.  I can turn them on/off.  However, their states don't update.


## Acknowledgments

This is based on [python-firetv](https://github.com/happyleavesaoc/python-firetv) by happyleavesaoc.  I've also included [python-adb](https://github.com/google/python-adb), with some modifications made for compatibility.
