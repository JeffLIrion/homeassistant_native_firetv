---
layout: page
title: "FireTV"
description: "Instructions on how to integrate Fire-TV into Home Assistant."
date: 2015-10-23 18:00
sidebar: true
comments: false
sharing: true
footer: true
logo: firetv.png
ha_category: Media Player
ha_release: 0.7.6
ha_iot_class: "Local Polling"
---


The `firetv` platform allows you to control an [Amazon Fire TV/stick](http://www.amazon.com/Amazon-DV83YW-Fire-TV/dp/B00U3FPN4U).

Steps to configure your Amazon Fire TV stick with Home Assistant:

- Turn on ADB Debugging on your Amazon Fire TV:
  - From the main (Launcher) screen, select Settings.
  - Select System > Developer Options.
  - Select ADB Debugging.
- Find Amazon Fire TV device IP:
  - From the main (Launcher) screen, select Settings.
  - Select System > About > Network.

To add FireTV to your installation, Note your device name, and add the following to your `configuration.yaml` file:

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

  # a device for which getting the current app (source) and the running apps (sources) cause issues
  - platform: firetv
    name: Fire TV 3
    host: 192.168.0.123
    get_source: false
    get_sources: false
```

Configuration variables:

- **host** (*Required*): The IP address your Fire TV device.  
- **name** (*Optional*): The friendly name of the device; the default is 'Amazon Fire TV'.
- **port** (*Optional*): The port for your Fire TV device; the default is 5555.
- **adbkey** (*Optional*): The path to your `adbkey` file.  Note that the file `adbkey.pub` must be in the same directory.  
- **get_source** (*Optional*): Whether or not to retrieve the current app as the source; the default is `true`.
- **get_sources** (*Optional*): Whether or not to retrieve the running apps as the list of sources; the default is `true`.

### {% linkable_title ADB Authentication (for Fire TV devices with recent software) %}

If you get a "Device authentication required, no keys available" error when trying to setup Fire TV, then you'll need to create an adbkey and add its path to your configuration.  Follow the instructions on this page to connect to your Fire TV from your computer: [Connecting to Fire TV Through adb](https://developer.amazon.com/zh/docs/fire-tv/connecting-adb-to-device.html).  

**Important!**  In the dialog appearing on your Fire TV, you must check the box that says "always allow connections from this device."  ADB authentication in Home Assistant will only work using a trusted key.

Once you've successfully connected to your Fire TV via the command `adb connect <ipaddress>`, the files `adbkey` and `adbkey.pub` will be created on your computer.  Copy these to your Home Assistant folder and add the path to the `adbkey` file to your configuration.  
