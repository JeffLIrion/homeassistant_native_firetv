"""
Support for functionality to interact with FireTV devices.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/media_player.firetv/
"""
import functools
import logging
import threading
import voluptuous as vol

from homeassistant.components.media_player import (
    MediaPlayerDevice, PLATFORM_SCHEMA, SUPPORT_NEXT_TRACK, SUPPORT_PAUSE,
    SUPPORT_PLAY, SUPPORT_PREVIOUS_TRACK, SUPPORT_SELECT_SOURCE, SUPPORT_STOP,
    SUPPORT_TURN_OFF, SUPPORT_TURN_ON, SUPPORT_VOLUME_SET, )
from homeassistant.const import (
    CONF_HOST, CONF_NAME, CONF_PORT, STATE_IDLE, STATE_OFF, STATE_PAUSED,
    STATE_PLAYING, STATE_STANDBY)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['https://github.com/JeffLIrion/python-firetv/zipball/pure-python-adb#firetv==1.0.8']

_LOGGER = logging.getLogger(__name__)

SUPPORT_FIRETV = SUPPORT_PAUSE | \
    SUPPORT_TURN_ON | SUPPORT_TURN_OFF | SUPPORT_PREVIOUS_TRACK | \
    SUPPORT_NEXT_TRACK | SUPPORT_SELECT_SOURCE | SUPPORT_STOP | \
    SUPPORT_VOLUME_SET | SUPPORT_PLAY

CONF_ADBKEY = 'adbkey'
CONF_ADB_SERVER_IP = 'adb_server_ip'
CONF_ADB_SERVER_PORT = 'adb_server_port'
CONF_GET_SOURCE = 'get_source'
CONF_GET_SOURCES = 'get_sources'
CONF_SET_STATES = 'set_states'

DEFAULT_NAME = 'Amazon Fire TV'
DEFAULT_PORT = 5555
DEFAULT_ADB_SERVER_PORT = 5037
DEFAULT_GET_SOURCE = True
DEFAULT_GET_SOURCES = True
DEFAULT_SET_STATES = True


def has_adb_files(value):
    """Check that ADB key files exist."""
    priv_key = value
    pub_key = '{}.pub'.format(value)
    cv.isfile(pub_key)
    return cv.isfile(priv_key)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_ADBKEY): has_adb_files,
    vol.Optional(CONF_ADB_SERVER_IP): cv.string,
    vol.Optional(
        CONF_ADB_SERVER_PORT, default=DEFAULT_ADB_SERVER_PORT): cv.port
    vol.Optional(CONF_GET_SOURCE, default=DEFAULT_GET_SOURCE): cv.boolean,
    vol.Optional(CONF_GET_SOURCES, default=DEFAULT_GET_SOURCES): cv.boolean,
    vol.Optional(CONF_SET_STATES, default=DEFAULT_SET_STATES): cv.boolean
})

PACKAGE_LAUNCHER = "com.amazon.tv.launcher"
PACKAGE_SETTINGS = "com.amazon.tv.settings"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the FireTV platform."""
    from firetv import FireTV

    host = '{0}:{1}'.format(config[CONF_HOST], config[CONF_PORT])

    if CONF_ADB_SERVER_IP not in config:
        # "python-adb"
        if CONF_ADBKEY in config:
            ftv = FireTV(host, config[CONF_ADBKEY])
            adb_log = " using adbkey='{0}'".format(config[CONF_ADBKEY])
        else:
            ftv = FireTV(host)
            adb_log = ""
    else:
        # "pure-python-adb"
        ftv = FireTV(host, adb_server_ip=config[CONF_ADB_SERVER_IP],
                     adb_server_port=config[CONF_ADB_SERVER_PORT])
        adb_log = " using ADB server at {0}:{1}".format(
            config[CONF_ADB_SERVER_IP], config[CONF_ADB_SERVER_PORT])

    if not ftv.available:
        _LOGGER.warning("Could not connect to Fire TV at %s%s", host, adb_log)
        return

    name = config[CONF_NAME]
    get_source = config[CONF_GET_SOURCE]
    get_sources = config[CONF_GET_SOURCES]
    set_states = config[CONF_SET_STATES]

    device = FireTVDevice(ftv, name, get_source, get_sources, set_states)
    add_entities([device])
    _LOGGER.info("Setup Fire TV at %s%s", host, adb_log)


def adb_decorator(override_available=False):
    """Send an ADB command if the device is available and not locked."""
    def adb_wrapper(func):
        """Wait if previous ADB commands haven't finished."""
        @functools.wraps(func)
        def _adb_wrapper(self, *args, **kwargs):
            # If the device is unavailable, don't do anything
            if not self.available and not override_available:
                return None

            # "python-adb"
            if not self.firetv.adb_server_ip:
                # If an ADB command is already running, skip this command
                if not self.adb_lock.acquire(blocking=False):
                    _LOGGER.info('Skipping an ADB command because a previous '
                                 'command is still running')
                    return None

                # More ADB commands will be prevented while trying this one
                try:
                    returns = func(self, *args, **kwargs)
                except self.exceptions:
                    _LOGGER.error('Failed to execute an ADB command; '
                                  'will attempt to re-establish the ADB '
                                  'connection in the next update')
                    returns = None
                    self._available = False  # pylint: disable=protected-access
                finally:
                    self.adb_lock.release()

            # "pure-python-adb"
            else:
                try:
                    returns = func(self, *args, **kwargs)
                except self.exceptions:
                    _LOGGER.error('Failed to execute an ADB command; '
                                  'will attempt to re-establish the ADB '
                                  'connection in the next update')
                    returns = None
                    self._available = False  # pylint: disable=protected-access

            return returns

        return _adb_wrapper

    return adb_wrapper


class FireTVDevice(MediaPlayerDevice):
    """Representation of an Amazon Fire TV device on the network."""

    def __init__(self, ftv, name, get_source, get_sources, set_states):
        """Initialize the FireTV device."""
        from adb.adb_protocol import (
            InvalidChecksumError, InvalidCommandError, InvalidResponseError)
        from adb.usb_exceptions import TcpTimeoutException

        self.firetv = ftv

        self._name = name
        self._get_source = get_source
        self._get_sources = get_sources
        self._set_states = set_states

        # whether or not the ADB connection is currently in use
        self.adb_lock = threading.Lock()

        # ADB exceptions to catch
        if not self.fire.adb_server_ip:
            # "python-adb"
            self.exceptions = (AttributeError, BrokenPipeError, TypeError,
                               ValueError, InvalidChecksumError,
                               InvalidCommandError, InvalidResponseError,
                               TcpTimeoutException)
        else:
            # "pure-python-adb"
            self.exceptions = (ConnectionResetError,)

        self._state = None
        self._available = self.firetv.available
        self._current_app = None
        self._running_apps = None

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
    def available(self):
        """Return whether or not the ADB connection is valid."""
        return self._available

    @property
    def source(self):
        """Return the current app."""
        return self._current_app

    @property
    def source_list(self):
        """Return a list of running apps."""
        return self._running_apps

    @adb_decorator(override_available=True)
    def update(self):
        """Get the latest date and update device state."""
        # Check if device is disconnected.
        if not self._available:
            self._running_apps = None
            self._current_app = None

            # Try to connect
            self._available = self.firetv.connect()

        # If the ADB connection is not intact, don't update.
        if not self._available:
            return

        # Check if device is off.
        if not self.firetv.screen_on:
            self._state = STATE_OFF
            self._running_apps = None
            self._current_app = None

        # Check if screen saver is on.
        elif not self.firetv.awake:
            self._state = STATE_IDLE
            self._running_apps = None
            self._current_app = None

        else:
            # Get the running apps.
            if self._get_sources:
                self._running_apps = self.firetv.running_apps

            # Get the current app.
            if self._get_source:
                current_app = self.firetv.current_app
                if isinstance(current_app, dict)\
                        and 'package' in current_app:
                    self._current_app = current_app['package']
                else:
                    self._current_app = current_app

                # Show the current app as the only running app.
                if not self._get_sources:
                    if self._current_app:
                        self._running_apps = [self._current_app]
                    else:
                        self._running_apps = None

                # Check if the launcher is active.
                if self._current_app in [PACKAGE_LAUNCHER,
                                         PACKAGE_SETTINGS]:
                    self._state = STATE_STANDBY

                # Check for a wake lock (device is playing).
                elif self.firetv.wake_lock:
                    self._state = STATE_PLAYING

                # Otherwise, device is paused.
                else:
                    self._state = STATE_PAUSED

            # Don't get the current app.
            elif self.firetv.wake_lock:
                # Check for a wake lock (device is playing).
                self._state = STATE_PLAYING
            else:
                # Assume the devices is on standby.
                self._state = STATE_STANDBY

    @adb_decorator()
    def turn_on(self):
        """Turn on the device."""
        self.firetv.turn_on()
        if self._set_states:
            self._state = STATE_IDLE

    @adb_decorator()
    def turn_off(self):
        """Turn off the device."""
        self.firetv.turn_off()
        if self._set_states:
            self._state = STATE_OFF

    @adb_decorator()
    def media_play(self):
        """Send play command."""
        self.firetv.media_play()

    @adb_decorator()
    def media_pause(self):
        """Send pause command."""
        self.firetv.media_pause()

    @adb_decorator()
    def media_play_pause(self):
        """Send play/pause command."""
        self.firetv.media_play_pause()

    @adb_decorator()
    def media_stop(self):
        """Send stop (back) command."""
        self.firetv.back()

    @adb_decorator()
    def volume_up(self):
        """Send volume up command."""
        self.firetv.volume_up()

    @adb_decorator()
    def volume_down(self):
        """Send volume down command."""
        self.firetv.volume_down()

    @adb_decorator()
    def media_previous_track(self):
        """Send previous track command (results in rewind)."""
        self.firetv.media_previous()

    @adb_decorator()
    def media_next_track(self):
        """Send next track command (results in fast-forward)."""
        self.firetv.media_next()

    @adb_decorator()
    def select_source(self, source):
        """Select input source.

        If the source starts with a '!', then it will close the app instead of
        opening it.
        """
        if isinstance(source, str):
            if not source.startswith('!'):
                self.firetv.launch_app(source)
                if self._set_states:
                    self._current_app = source
            else:
                self.firetv.stop_app(source[1:].lstrip())
                if self._set_states:
                    self._current_app = PACKAGE_LAUNCHER
                    self._state = STATE_STANDBY
