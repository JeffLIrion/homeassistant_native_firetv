# Native support for Fire TV in Home Assistant

No Python 2 service necessary!  And it can also handle device authentication.


## Installation

Copy the `media_player/firetv.py` to your `custom_components` folder (`custom_components/media_player/firetv.py`) in your configuration directory.  If you do not have a `custom_components` folder, then you will need to create it.  


## Configuration

```yaml
# Example configuration.yaml entry
media_player:
  # a device that does not require ADB authentication
  - platform: firetv
    name: Fire TV 1
    host: 192.168.0.111

  # a device that does require ADB authentication
  - platform: firetv
    name: Fire TV 2
    host: 192.168.0.222
    adbkey: "/config/android/adbkey"

  # a device for which getting the running apps causes issues
  - platform: firetv
    name: Fire TV 3
    host: 192.168.0.222
    get_sources: false
```


## ADB Authentication (for Fire TV devices with recent software)

If you get a "Device authentication required, no keys available" error when trying to setup Fire TV, then you'll need to create an adbkey and add its path to your configuration.  Follow the instructions on this page to connect to your Fire TV from your computer: [Connecting to Fire TV Through adb](https://developer.amazon.com/zh/docs/fire-tv/connecting-adb-to-device.html).  

**Important!**  You must check the box that says "always allow connections from this device."  ADB authentication in Home Assistant will only work using a trusted key.

Once you've successfully connected to your Fire TV via the command `adb connect <ipaddress>`, the files `adbkey` and `adbkey.pub` will be created on your computer.  Copy these to your Home Assistant folder and add the path to the `adbkey` file to your configuration.  


## Acknowledgments

This is based on [python-firetv](https://github.com/happyleavesaoc/python-firetv) by happyleavesaoc, and it depends on [python-adb](https://github.com/google/python-adb).
