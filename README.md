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

I have two Fire TV sticks, one that requires authentication and one that does not.

* The Fire TV without authentication seems to be working correctly for me.
* The Fire TV that requires authentication shows up in Home Assistant when I use M2Crypto, but not when I use pycryptodome.  I'm able to use M2Crypto on my Home Assistant installation in a virtual environment on my laptop, but not in Hass.io on my Raspberry Pi.


## Acknowledgments

This is based on [python-firetv](https://github.com/happyleavesaoc/python-firetv) by happyleavesaoc.  I've also included [python-adb](https://github.com/google/python-adb), with some modifications made for compatibility.
