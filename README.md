# Native support for Fire TV in Home Assistant

No Python 2 service necessary!  And it can also handle device authentication.


## Installation

Copy the `media_player/firetv.py` to your `custom_components` folder (`custom_components/media_player/firetv.py`) in your configuration directory.  If you do not have a `custom_components` folder, then you will need to create it.  


## Configuration

```yaml
media_player:
  - platform: firetv
    name: Fire TV 1
    host: 192.168.0.111

  - platform: firetv
    name: Fire TV 2
    host: 192.168.0.222
    adbkey: "/config/android/adbkey"
```


## ADB Authentication (for Fire TV devices with recent software)

If you get a "Device authentication required, no keys available" error when trying to setup Fire TV, then you'll need to create an adbkey and add its path to your configuration.  Follow the instructions on this page to connect to your Fire TV from your computer: [Connecting to Fire TV Through adb](https://developer.amazon.com/zh/docs/fire-tv/connecting-adb-to-device.html).  

**Important!**  In the dialog appearing on your Fire TV, you must check the box that says "always allow connections from this device."  ADB authentication in Home Assistant will only work using a trusted key.

Once you've successfully connected to your Fire TV via the command `adb connect <ipaddress>`, the files `adbkey` and `adbkey.pub` will be created on your computer.  Copy these to your Home Assistant folder and add the path to the `adbkey` file to your configuration.  


## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'firetv'`

**Solution:** Restart Home Assistant.  This error occurs because HA needs some time to install the dependencies, and it tries to setup the component before the dependencies have been installed.  


### Issue: Error while setting up platform firetv *(with an ADB key)*

**Solution:** There is probably an issue with your ADB key.  Here are some possibilities.  

1. Your key is not pre-authenticated.  Before using the `adbkey` in Home Assistant, you _**must**_ connect to your Fire TV device using the ADB binary and tell the Fire TV to always allow connections from this computer.  For more information, see the section "ADB Authentication (for Fire TV devices with recent software)" above.

2. Home Assistant does not have the appropriate permissions for the `adbkey` file and so it is not able to use it.  Once you fix the permissions, the component should work.

3. You are already connected to the Fire TV via ADB from another device.  Only one device can be connected, so disconnect the other device, restart the Fire TV (for good measure), and then restart Home Assistant.  


## Acknowledgments

This is based on [python-firetv](https://github.com/happyleavesaoc/python-firetv) by happyleavesaoc, and it depends on [python-adb](https://github.com/google/python-adb).
