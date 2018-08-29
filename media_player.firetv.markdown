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
  - platform: firetv
    name: Fire TV 1
    host: "192.168.0.111:5555"

  - platform: firetv
    name: Fire TV 2
    host: "192.168.0.222:5555"
    adbkey: "/config/android/adbkey"
```

Configuration variables:

- **host** (*Required*): The IP address and port for your Fire TV device.  The standard port for ADB on a Fire TV is 5555.
- **name** (*Optional*): The friendly name of the device, default is 'Amazon Fire TV'.
- **adbkey** (*Optional*): The path to your `adbkey` file.  Note that the file `adbkey.pub` must be in the same directory.  

### {% linkable_title ADB Authentication (for Fire TV devices with recent software) %}

If you get a "Device authentication required, no keys available" error when trying to setup Fire TV, then you'll need to create an adbkey and add its path to your configuration.  Follow the instructions on this page to connect to your Fire TV from your computer: [Connecting to Fire TV Through adb](https://developer.amazon.com/zh/docs/fire-tv/connecting-adb-to-device.html).  

**Important!**  You must check the box that says "always allow connections from this device."  ADB authentication in Home Assistant will only work using a trusted key.

Once you've successfully connected to your Fire TV via the command `adb connect <ipaddress>`, the files `adbkey` and `adbkey.pub` will be created on your computer.  Copy these to your Home Assistant folder and add the path to the `adbkey` file to your configuration.  
