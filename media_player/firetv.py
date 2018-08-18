"""
Support for functionality to interact with FireTV devices.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/media_player.firetv/
"""
import logging
import voluptuous as vol

from homeassistant.components.media_player import (
    SUPPORT_NEXT_TRACK, SUPPORT_PAUSE, SUPPORT_PREVIOUS_TRACK, PLATFORM_SCHEMA,
    SUPPORT_SELECT_SOURCE, SUPPORT_STOP, SUPPORT_TURN_OFF, SUPPORT_TURN_ON,
    SUPPORT_VOLUME_SET, SUPPORT_PLAY, MediaPlayerDevice)
from homeassistant.const import (
    STATE_IDLE, STATE_OFF, STATE_PAUSED, STATE_PLAYING, STATE_STANDBY,
    STATE_UNKNOWN, CONF_HOST, CONF_NAME)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['libusb1>=1.0.16', 'pycryptodome']

_LOGGER = logging.getLogger(__name__)

SUPPORT_FIRETV = SUPPORT_PAUSE | \
    SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_PREVIOUS_TRACK | \
    SUPPORT_NEXT_TRACK | SUPPORT_SELECT_SOURCE | SUPPORT_STOP | \
    SUPPORT_VOLUME_SET | SUPPORT_PLAY

CONF_ADBKEY = 'adbkey'

DEFAULT_HOST = 'localhost'
DEFAULT_NAME = 'Amazon Fire TV'
DEFAULT_ADBKEY = ''

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_ADBKEY, default=DEFAULT_ADBKEY): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the FireTV platform."""
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    adbkey = config.get(CONF_ADBKEY)

    device = FireTVDevice(host, name, adbkey)
    if not device._firetv._adb:
        _LOGGER.warning("Could not connect to Fire TV at {0}".format(host))
    else:
        _LOGGER.info('Setup Fire TV at {0}'.format(host))
        add_devices([device])


class FireTVDevice(MediaPlayerDevice):
    """Representation of an Amazon Fire TV device on the network."""

    def __init__(self, host, name, adbkey):
        """Initialize the FireTV device."""
        from custom_components.python_firetv import FireTV
        self._firetv = FireTV(host, adbkey)
        self._name = name
        self._state = STATE_UNKNOWN
        self._running_apps = None
        self._current_app = None

    @property
    def name(self):
        """Return the device name."""
        return self._name

    @property
    def should_poll(self):
        """Device should be polled."""
        return True

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_FIRETV

    @property
    def state(self):
        """Return the state of the player."""
        return self._state

    @property
    def source(self):
        """Return the current app."""
        return self._current_app

    @property
    def source_list(self):
        """Return a list of running apps."""
        return self._running_apps

    def update(self):
        """Get the latest date and update device state."""
        self._state = {
            'idle': STATE_IDLE,
            'off': STATE_OFF,
            'play': STATE_PLAYING,
            'pause': STATE_PAUSED,
            'standby': STATE_STANDBY,
            'disconnected': STATE_UNKNOWN,
        }.get(self._firetv.state, STATE_UNKNOWN)

        if self._state not in [STATE_OFF, STATE_UNKNOWN]:
            self._running_apps = self._firetv.running_apps()
            self._current_app = self._firetv.current_app
        else:
            self._running_apps = None
            self._current_app = None

            if self._state == STATE_UNKNOWN:
                self._firetv.connect()

    def turn_on(self):
        """Turn on the device."""
        self._firetv.turn_on()

    def turn_off(self):
        """Turn off the device."""
        self._firetv.turn_off()

    def media_play(self):
        """Send play command."""
        self._firetv.media_play()

    def media_pause(self):
        """Send pause command."""
        self._firetv.media_pause()

    def media_play_pause(self):
        """Send play/pause command."""
        self._firetv.media_play_pause()

    def media_stop(self):
        """Send stop (back) command."""
        self._firetv.back()

    def volume_up(self):
        """Send volume up command."""
        self._firetv.volume_up()

    def volume_down(self):
        """Send volume down command."""
        self._firetv.volume_down()

    def media_previous_track(self):
        """Send previous track command (results in rewind)."""
        self._firetv.media_previous()

    def media_next_track(self):
        """Send next track command (results in fast-forward)."""
        self._firetv.media_next()

    def select_source(self, source):
        """Select input source."""
        if isinstance(source, str):
            if not source.startswith('!'):
                self._firetv.launch_app(source)
            else:
                self._firetv.stop_app(source[1:].lstrip())
