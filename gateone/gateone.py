#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Liftoff Software Corporation
#
# For license information see LICENSE.txt

# TODO:

# Meta
__version__ = '1.2.0'
__version_info__ = (1, 2, 0)
__license__ = "AGPLv3 or Proprietary (see LICENSE.txt)"
__author__ = 'Dan McDougall <daniel.mcdougall@liftoffsoftware.com>'

# NOTE: Docstring includes reStructuredText markup for use with Sphinx.
__doc__ = '''\
.. _gateone.py:

Gate One
========
Gate One is a web-based terminal emulator written in Python using the Tornado
web framework.  This module runs the primary daemon process and acts as a
central controller for all running terminals and terminal programs.  It supports
numerous configuration options and can also be called with the --kill switch
to kill all running terminal programs (if using dtach--otherwise they die on
their own when gateone.py is stopped).

Dependencies
------------
Gate One requires Python 2.6+ but runs best with Python 2.7+.  It also depends
on the following 3rd party Python modules:

 * `Tornado <http://www.tornadoweb.org/>`_ 2.2+ - A non-blocking web server framework that powers FriendFeed.

The following modules are optional and can provide Gate One with additional
functionality:

 * `pyOpenSSL <https://launchpad.net/pyopenssl>`_ 0.10+ - An OpenSSL module/wrapper for Python.  Only used to generate self-signed SSL keys and certificates.  If pyOpenSSL isn't available Gate One will fall back to using the 'openssl' command to generate self-signed certificates.
 * `kerberos <http://pypi.python.org/pypi/kerberos>`_ 1.0+ - A high-level Kerberos interface for Python.  Only necessary if you plan to use the Kerberos authentication module.
 * `python-pam <http://packages.debian.org/lenny/python-pam>`_ 0.4.2+ - A Python module for interacting with PAM (the Pluggable Authentication Module present on nearly every Unix).  Only necessary if you plan to use PAM authentication.

With the exception of python-pam, both the required and optional modules can usually be installed via one of these commands:

    .. ansi-block::

        \x1b[1;34muser\x1b[0m@modern-host\x1b[1;34m:~ $\x1b[0m sudo pip install tornado pyopenssl kerberos

...or:

    .. ansi-block::

        \x1b[1;34muser\x1b[0m@legacy-host\x1b[1;34m:~ $\x1b[0m sudo easy_install tornado pyopenssl kerberos

.. note:: The use of pip is recommended.  See http://www.pip-installer.org/en/latest/installing.html if you don't have it.

The python-pam module is available in most Linux distribution repositories.  Simply executing one of the following should take care of it:

    .. ansi-block::

        \x1b[1;34muser\x1b[0m@debian-or-ubuntu-host\x1b[1;34m:~ $\x1b[0m sudo apt-get install python-pam

    .. ansi-block::

        \x1b[1;34muser\x1b[0m@redhat-host\x1b[1;34m:~ $\x1b[0m sudo yum install python-pam

    .. ansi-block::

        \x1b[1;34muser\x1b[0m@gentoo-host\x1b[1;34m:~ $\x1b[0m sudo emerge python-pam

    .. ansi-block::

        \x1b[1;34muser\x1b[0m@suse-host\x1b[1;34m:~ $\x1b[0m sudo yast -i python-pam

Settings
--------
All of Gate One's configurable options can be controlled either via command line
switches or by settings in the server.conf file (they match up 1-to-1).  If no
server.conf exists one will be created using defaults (i.e. when Gate One is run
for the first time).  Settings in the server.conf file use the following format::

    <setting> = <value>

Here's an example::

    address = "127.0.0.1;::1;10.1.1.4" # Strings are surrounded by quotes
    port = 443 # Numbers don't need quotes

There are a few important differences between the configuration file and
command line switches in regards to boolean values (True/False).  A switch such
as --debug evaluates to "debug = True" and this is exactly how it would be
configured in server.conf::

    debug = True # Booleans don't need quotes either

.. note:: The following values in server.conf are case sensitive: True, False and None (and should not be placed in quotes).

Running gateone.py with the --help switch will print the usage information as
well as descriptions of what each configurable option does:

.. ansi-block::

    \x1b[1;31mroot\x1b[0m@host\x1b[1;34m:~ $\x1b[0m ./gateone.py --help
    Usage: ./gateone.py [OPTIONS]

    Options:
      --help                           show this help information
      --log_file_max_size              max size of log files before rollover
      --log_file_num_backups           number of log files to keep
      --log_file_prefix=PATH           Path prefix for log files. Note that if you are running multiple tornado processes, log_file_prefix must be different for each of them (e.g. include the port number)
      --log_to_stderr                  Send log output to stderr (colorized if possible). By default use stderr if --log_file_prefix is not set and no other logging is configured.
      --logging=debug|info|warning|error|none Set the Python log level. If 'none', tornado won't touch the logging configuration.
      --address                        Run on the given address.  Default is all addresses (IPv6 included).  Multiple address can be specified using a semicolon as a separator (e.g. '127.0.0.1;::1;10.1.1.100').
      --auth                           Authentication method to use.  Valid options are: none, api, google, kerberos, pam
      --certificate                    Path to the SSL certificate.  Will be auto-generated if none is provided.
      --command                        Run the given command when a user connects (e.g. '/bin/login').
      --config                         Path to the config file.  Default: /opt/gateone/server.conf
      --cookie_secret                  Use the given 45-character string for cookie encryption.
      --debug                          Enable debugging features such as auto-restarting when files are modified.
      --disable_ssl                    If enabled, Gate One will run without SSL (generally not a good idea).
      --dtach                          Wrap terminals with dtach. Allows sessions to be resumed even if Gate One is stopped and started (which is a sweet feature).
      --embedded                       Doesn't do anything (yet).
      --enable_unix_socket             Enable Unix socket support use_unix_sockets (if --enable_unix_socket=True).
      --https_redirect                 If enabled, a separate listener will be started on port 80 that redirects users to the configured port using HTTPS.
      --js_init                        A JavaScript object (string) that will be used when running GateOne.init() inside index.html.  Example: --js_init="{scheme: 'white'}" would result in GateOne.init({scheme: 'white'})
      --keyfile                        Path to the SSL keyfile.  Will be auto-generated if none is provided.
      --kill                           Kill any running Gate One terminal processes including dtach'd processes.
      --locale                         The locale (e.g. pt_PT) Gate One should use for translations.  If not provided, will default to $LANG (which is 'en_US' in your current shell), or en_US if not set.
      --new_api_key                    Generate a new API key that an external application can use to embed Gate One.
      --origins                        A semicolon-separated list of origins you wish to allow access to your Gate One server over the WebSocket.  This value must contain the hostnames and FQDNs (e.g. https://foo;https://foo.bar;) users will use to connect to your Gate One server as well as the hostnames/FQDNs of any sites that will be embedding Gate One. Here's the default on your system: 'https://localhost;https://yourhostname'. Alternatively, '*' may be  specified to allow access from anywhere.
      --pam_realm                      Basic auth REALM to display when authenticating clients.  Default: hostname.  Only relevant if PAM authentication is enabled.
      --pam_service                    PAM service to use.  Defaults to 'login'. Only relevant if PAM authentication is enabled.
      --pid_file                       Path of the pid file.   Default: /tmp/gateone.pid
      --port                           Run on the given port.
      --session_dir                    Path to the location where session information will be stored.
      --session_logging                If enabled, logs of user sessions will be saved in <user_dir>/<user>/logs.  Default: Enabled
      --session_timeout                Amount of time that a session should be kept alive after the client has logged out.  Accepts <num>X where X could be one of s, m, h, or d for seconds, minutes, hours, and days.  Default is '5d' (5 days).
      --sso_realm                      Kerberos REALM (aka DOMAIN) to use when authenticating clients. Only relevant if Kerberos authentication is enabled.
      --sso_service                    Kerberos service (aka application) to use. Defaults to HTTP. Only relevant if Kerberos authentication is enabled.
      --syslog_facility                Syslog facility to use when logging to syslog (if syslog_session_logging is enabled).  Must be one of: auth, cron, daemon, kern, local0, local1, local2, local3, local4, local5, local6, local7, lpr, mail, news, syslog, user, uucp.  Default: daemon
      --syslog_host                    Remote host to send syslog messages to if syslog_logging is enabled.  Default: None (log to the local syslog daemon directly).  NOTE:  This setting is required on platforms that don't include Python's syslog module.
      --syslog_session_logging         If enabled, logs of user sessions will be written to syslog.
      --unix_socket_path               Run on the given socket file.  Default: /tmp/gateone.sock
      --url_prefix                     An optional prefix to place before all Gate One URLs. e.g. '/gateone/'.  Use this if Gate One will be running behind a reverse proxy where you want it to be located at some sub-URL path.
      --user_dir                       Path to the location where user files will be stored.

.. note:: Some of these options (e.g. log_file_prefix) are inherent to the Tornado framework.  You won't find them anywhere in gateone.py.

File Paths
----------
Gate One stores its files, temporary session information, and persistent user
data in the following locations (Note: Many of these are configurable):

================= ==================================================================================
File/Directory      Description
================= ==================================================================================
authpam.py        Contains the PAM authentication Mixin used by auth.py.
auth.py           Authentication classes.
certificate.pem   The default certificate Gate One will use in SSL communications.
docs/             Gate One's documentation.
gateone.py        Gate One's primary executable/script. Also, the file containing this documentation
i18n/             Gate One's internationalization (i18n) support and locale/translation files.
keyfile.pem       The default private key used with SSL communications.
logviewer.py      A utility to view Gate One session logs.
plugins/          Plugins go here in the form of ./plugins/<plugin name>/<plugin files|directories>
remote_syslog.py  A module that supports sending syslog messages over UDP to a remote syslog host.
server.conf       Gate One's configuration file.
sso.py            A Kerberos Single Sign-on module for Tornado (used by auth.py)
static/           Non-dynamic files that get served to clients (e.g. gateone.js, gateone.css, etc).
templates/        Tornado template files such as index.html.
terminal.py       A Pure Python terminal emulator module.
termio.py         Terminal input/output control module.
tests/            Various scripts and tools to test Gate One's functionality.
utils.py          Various supporting functions.
users/            Persistent user data in the form of ./users/<username>/<user-specific files>
users/<user>/logs This is where session logs get stored if session_logging is set.
/tmp/gateone      Temporary session data in the form of /tmp/gateone/<session ID>/<files>
================= ==================================================================================

Running
-------
Executing Gate One is as simple as:

.. ansi-block::

    \x1b[1;31mroot\x1b[0m@host\x1b[1;34m:~ $\x1b[0m ./gateone.py

.. note:: By default Gate One will run on port 443 which requires root on most systems.  Use `--port=(something higher than 1024)` for non-root users.

Plugins
-------
Gate One includes support for any combination of the following types of plugins:

 * Python
 * JavaScript
 * CSS

Python plugins can integrate with Gate One in three ways:

 * Adding or overriding tornado.web.RequestHandlers (with a given regex).
 * Adding or overriding methods (aka "commands") in ApplicationWebSocket.
 * Adding special plugin-specific escape sequence handlers (see the plugin development documentation for details on what/how these are/work).

JavaScript plugins will be added to the <body> tag of Gate One's base index.html
template by way of a single file (`{{gateone_js}}` below) that is the
concatenation of all plugins' JS templates:

.. code-block:: html

    <script type="text/javascript" src="{{gateone_js}}"></script>

CSS plugins are similar to JavaScript but instead of being appended to the
<body> they are added to the <head> by way of a WebSocket download and some
fancy JavaScript inside of gateone.js:

.. code-block:: javascript

    CSSPluginAction: function(url) {
        // Loads the CSS for a given plugin by adding a <link> tag to the <head>
        var queries = url.split('?')[1].split('&'), // So we can parse out the plugin name and the template
            plugin = queries[0].split('=')[1],
            file = queries[1].split('=')[1].split('.')[0];
        // The /cssrender method needs the prefix and the container
        url = url + '&container=' + GateOne.prefs.goDiv.substring(1);
        url = url + '&prefix=' + GateOne.prefs.prefix;
        url = GateOne.prefs.url + url.substring(1);
        GateOne.Utils.loadCSS(url, plugin+'_'+file);
    }

There are also hooks throughout Gate One's code for plugins to add or override
Gate One's functionality.  Documentation on how to write plugins can be found in
the Plugin Development docs.  From the perspective of gateone.py, it performs
the following tasks in relation to plugins:

 * Imports Python plugins and connects their hooks.
 * Serves the index.html that includes plugins' respective .js and .css files.

Class Docstrings
================
'''

# Standard library modules
import os
import sys
import logging
import time
import socket
import pty
import atexit
import ssl
import hashlib
from functools import wraps
from datetime import datetime, timedelta

# Tornado modules (yeah, we use all this stuff)
try:
    import tornado.httpserver
    import tornado.ioloop
    import tornado.options
    import tornado.web
    import tornado.auth
    import tornado.template
    import tornado.netutil
    from tornado.websocket import WebSocketHandler
    from tornado.escape import json_decode
    from tornado.options import define, options
    from tornado import locale
    from tornado import version as tornado_version
    from tornado import version_info as tornado_version_info
except ImportError:
    print("\x1b[31;1mERROR:\x1b[0m Gate One requires the Tornado framework.  "
          "You probably want to run something like, \x1b[1m'pip install "
          "--upgrade tornado'\x1b[0m.")
    sys.exit(1)

if tornado_version_info[0] < 2 and tornado_version_info[1] < 2:
    print("\x1b[31;1mERROR:\x1b[0m Gate One requires version 2.2+ of the "
            "Tornado framework.  The installed version of Tornado is version "
            "%s." % tornado_version)
    sys.exit(1)

# We want this turned on right away
tornado.options.enable_pretty_logging()

# Our own modules
from auth import NullAuthHandler, KerberosAuthHandler, GoogleAuthHandler
from auth import APIAuthHandler, SSLAuthHandler, PAMAuthHandler
from auth import require, authenticated, policies, applicable_policies
from utils import generate_session_id, mkdir_p
from utils import gen_self_signed_ssl, killall, get_plugins, load_modules
from utils import merge_handlers, none_fix, convert_to_timedelta
from utils import FACILITIES, json_encode, recursive_chown, ChownError
from utils import write_pid, read_pid, remove_pid, drop_privileges, minify
from utils import check_write_permissions, get_applications, get_settings

# Setup the locale functions before anything else
locale.set_default_locale('en_US')
user_locale = None # Replaced with the actual user locale object in __main__
def _(string):
    """
    Wraps user_locale.translate so we can .encode('UTF-8') when writing to
    stdout.  This function will get overridden by the regular translate()
    function in __main__
    """
    if user_locale:
        return user_locale.translate(string).encode('UTF-8')
    else:
        return string.encode('UTF-8')

# Globals
SESSIONS = {} # We store the crux of most session info here
CMD = None # Will be overwritten by options.command
TIMEOUT = timedelta(days=5) # Gets overridden by options.session_timeout
# SESSION_WATCHER be replaced with a tornado.ioloop.PeriodicCallback that watches for
# sessions that have timed out and takes care of cleaning them up.
SESSION_WATCHER = None
CLEANER = None # Log cleaner PeriodicCallback
GATEONE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_CACHE = {}
# PERSIST is a generic place for applications and plugins to store stuff in a
# way that lasts between page loads.  USE RESPONSIBLY.
PERSIST = {}
APPLICATIONS = {}
PLUGINS = {}
PLUGIN_WS_CMDS = {} # Gives plugins the ability to extend/enhance ApplicationWebSocket
PLUGIN_HOOKS = {} # Gives plugins the ability to hook into various things.
PLUGIN_AUTH_HOOKS = [] # For plugins to register functions to be called after a
                       # user successfully authenticates
PLUGIN_ENV_HOOKS = {} # Allows plugins to add environment variables that will be
                      # available to all executed commands.
# Gate One registers a handler for for terminal.py's CALLBACK_OPT special escape
# sequence callback.  Whenever this escape sequence is encountered, Gate One
# will parse the sequence's contained characters looking for the following
# format:
#   <plugin name>|<whatever>
# The <whatever> part will be passed to any plugin matching <plugin name> if the
# plugin has 'Escape': <function> registered in its hooks.
PLUGIN_ESC_HANDLERS = {}
# This is used to store plugin terminal hooks that are called when a new
# terminal is created (so a plugin could override/attach callbacks to the
# multiplex or terminal emulator instances).  NOTE: This is specifically for
# adding to the terminal emulator's CALLBACK_* capability.  For modifying the
# terminal emulator instance directly see PLUGIN_NEW_TERM_HOOKS.
PLUGIN_TERM_HOOKS = {}
# The NEW_TERM hooks are called at the end of ApplicationWebSocket.new_terminal()
# with 'self' and the new instance of the terminal emulator as the only
# arguments.  It's a more DIY/generic version of PLUGIN_TERM_HOOKS.
PLUGIN_NEW_TERM_HOOKS = []
# 'Command' hooks get called before a new Multiplex instance is created inside
# of ApplicationWebSocket.new_multiplex().  They are passed the 'command' and must
# return a string that will be used as the replacement 'command'.  This allows
# plugin authors to modify the configured 'command' before it is executed
PLUGIN_COMMAND_HOOKS = []
# 'Multiplex' hooks get called at the end of ApplicationWebSocket.new_multiplex()
# with the instance of ApplicationWebSocket and the new instance of Multiplex as
# the only arguments, respectively.
PLUGIN_NEW_MULTIPLEX_HOOKS = []

# Secondary locale setup
locale_dir = os.path.join(GATEONE_DIR, 'i18n')
locale.load_gettext_translations(locale_dir, 'gateone')
# NOTE: The locale gets set in __main__

# Helper functions
def require_auth(method):
    """
    An equivalent to tornado.web.authenticated for WebSockets
    (ApplicationWebSocket, specifically).
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.write_message(_("Only valid users please.  Thanks!"))
            self.close() # Close the WebSocket
        return method(self, *args, **kwargs)
    return wrapper

def cleanup_user_logs():
    """
    Cleans up all user logs (everything in the user's 'logs' directory and
    subdirectories that ends in 'log') older than the `user_logs_max_age`
    setting.  The log directory is assumed to be:

        *user_dir*/<user>/logs

    ...where *user_dir* is whatever Gate One happens to have configured for
    that particular setting.
    """
    logging.debug("cleanup_session_logs()")
    settings = get_settings(os.path.join(GATEONE_DIR, 'settings'))
    user_dir = settings['*']['gateone']['user_dir']
    default = "30d"
    max_age_str = settings['*']['gateone'].get('user_logs_max_age', default)
    max_age = convert_to_timedelta(max_age_str)
    def descend(path):
        """
        Descends *path* removing logs it finds older than `max_age` and calls
        :func:`descend` on any directories.
        """
        for fname in os.listdir(path):
            log_path = os.path.join(path, fname)
            if os.path.isdir(log_path):
                descend(log_path)
                continue
            if not log_path.endswith('log'):
                continue
            mtime = time.localtime(os.stat(log_path).st_mtime)
            # Convert to a datetime object for easier comparison
            mtime = datetime.fromtimestamp(time.mktime(mtime))
            if datetime.now() - mtime > max_age:
                # The log is older than max_age, remove it
                logging.info(_("Removing log due to age (>%s old): %s" % (
                    max_age_str, log_path)))
                os.remove(log_path)
    for user in os.listdir(user_dir):
        logs_path = os.path.abspath(os.path.join(user_dir, user, 'logs'))
        if not os.path.exists(logs_path):
            # Nothing to do
            continue
        descend(logs_path)

def policy_send_user_message(cls, policy):
    """
    Called by :func:`gateone_policies`, returns True if the user is
    authorized to send messages to other users and if applicable, all users
    (broadcasts).
    """
    error_msg = _("You do not have permission to send messages to %s.")
    try:
        upn = cls.f_args[0]['upn']
    except (KeyError, IndexError):
        # send_user_message got bad *settings*.  Deny
        return False
    # TODO: Add a mechanism that allows users to mute other users here.
    if upn == 'AUTHENTICATED':
        cls.error = error_msg % "all users at once"
    else:
        cls.error = error_msg % upn
    return policy.get('send_user_messages', True)

def policy_broadcast(cls, policy):
    """
    Called by :func:`gateone_policies`, returns True if the user is
    authorized to broadcast messages using the
    :meth:`ApplicationWebSocket.broadcast` method.  It makes this determination
    by checking the `['gateone']['send_broadcasts']` policy.
    """
    cls.error = _("You do not have permission to broadcast messages.")
    return policy.get('send_broadcasts', True)

def gateone_policies(cls):
    """
    This function gets registered under 'gateone' in the
    :attr:`ApplicationWebSocket.security` dict and is called by the
    :func:`require` decorator by way of the :class:`policies` sub-function. It
    returns True or False depending on what is defined in the settings dir and
    what function is being called.

    This function will keep track of and place limmits on the following:

        * Who can send messages to other users (including broadcasts).

    If no 'terminal' policies are defined this function will always return True.
    """
    instance = cls.instance # ApplicationWebSocket instance
    function = cls.function # Wrapped function
    f_args = cls.f_args     # Wrapped function's arguments
    f_kwargs = cls.f_kwargs # Wrapped function's keyword arguments
    policy_functions = {
        'send_user_message': policy_send_user_message,
        'broadcast': policy_broadcast,
    }
    user = instance.current_user
    policy = applicable_policies('gateone', user, instance.ws.policies)
    if not policy: # Empty RUDict
        return True # A world without limits!
    if function.__name__ in policy_functions:
        return policy_functions[function.__name__](cls, policy)
    return True # Default to permissive if we made it this far

@atexit.register # I love this feature!
def kill_all_sessions():
    """
    Calls all 'timeout_callbacks' attached to all `SESSIONS`.
    """
    for session in SESSIONS.keys():
        if "timeout_callbacks" in SESSIONS[session]:
            if SESSIONS[session]["timeout_callbacks"]:
                for callback in SESSIONS[session]["timeout_callbacks"]:
                    callback(session)

def timeout_sessions():
    """
    Loops over the SESSIONS dict killing any sessions that haven't been used
    for the length of time specified in *TIMEOUT* (global).  The value of
    *TIMEOUT* can be set in server.conf or specified on the command line via the
    *session_timeout* value.  Arguments:

    .. note:: This function is meant to be called via Tornado's :meth:`~tornado.ioloop.PeriodicCallback`.
    """
    # Commented because it is a bit noisy.  Uncomment to debug this mechanism.
    #logging.debug("timeout_sessions() TIMEOUT: %s" % TIMEOUT)
    try:
        if not SESSIONS: # Last client has timed out
            logging.info(_("All user sessions have terminated."))
            global SESSION_WATCHER
            if SESSION_WATCHER:
                SESSION_WATCHER.stop() # Stop ourselves
                SESSION_WATCHER = None # So authenticate() will know to start it
            # Reload gateone.py to free up memory (CPython can be a bit
            # overzealous in keeping things cached).  In theory this isn't
            # necessary due to Gate One's prodigous use of dynamic imports but
            # in reality people will see an idle gateone.py eating up 30 megs of
            # RAM and wonder, "WTF...  No one has connected in weeks."
            logging.info(_("The last idle session has timed out. Reloading..."))
            try:
                os.execv(sys.executable, [sys.executable] + sys.argv)
            except OSError:
                # Mac OS X versions prior to 10.6 do not support execv in
                # a process that contains multiple threads.
                os.spawnv(os.P_NOWAIT, sys.executable,
                    [sys.executable] + sys.argv)
                sys.exit(0)
        for session in list(SESSIONS.keys()):
            if "last_seen" not in SESSIONS[session]:
                # Session is in the process of being created.  We'll check it
                # the next time timeout_sessions() is called.
                continue
            if SESSIONS[session]["last_seen"] == 'connected':
                # Connected sessions do not need to be checked for timeouts
                continue
            if datetime.now() > SESSIONS[session]["last_seen"] + TIMEOUT:
                # Kill the session
                logging.info(_("{session} timeout.".format(session=session)))
                if "timeout_callbacks" in SESSIONS[session]:
                    if SESSIONS[session]["timeout_callbacks"]:
                        for callback in SESSIONS[session]["timeout_callbacks"]:
                            callback(session)
                del SESSIONS[session]
    except Exception as e:
        logging.info(_(
            "Exception encountered in timeout_sessions(): {exception}".format(
                exception=e)
        ))
        import traceback
        traceback.print_exc(file=sys.stdout)

# Classes
class HTTPSRedirectHandler(tornado.web.RequestHandler):
    """
    A handler to redirect clients from HTTP to HTTPS.
    """
    def get(self):
        """Just redirects the client from HTTP to HTTPS"""
        port = self.settings['port']
        url_prefix = self.settings['url_prefix']
        host = self.request.headers.get('Host', 'localhost')
        self.redirect(
            'https://%s:%s%s' % (host, port, url_prefix))

class StaticHandler(tornado.web.StaticFileHandler):
    """
    An override of :class:`tornado.web.StaticFileHandler` to ensure that the
    Access-Control-Allow-Origin header gets set correctly.
    """
    # This is the only function we need to override thanks to the thoughtfulness
    # of the Tornado devs.
    def set_extra_headers(self, path):
        """
        Adds the Access-Control-Allow-Origin header to allow cross-origin
        access to static content for applications embedding Gate One.
        Specifically, this is necessary in order to support loading fonts
        from different origins.
        """
        self.set_header('Access-Control-Allow-Origin', '*')

class BaseHandler(tornado.web.RequestHandler):
    """
    A base handler that all Gate One RequestHandlers will inherit methods from.
    """
    # Right now it's just the one function...
    def get_current_user(self):
        """Tornado standard method--implemented our way."""
        # NOTE: self.current_user is actually an @property that calls
        #       self.get_current_user() and caches the result.
        user_json = self.get_secure_cookie("gateone_user")
        if user_json:
            user = json_decode(user_json)
            user['ip_address'] = self.request.remote_ip
            if user and 'upn' not in user:
                return None
            return user
    # More may be added in the future

class DownloadHandler(BaseHandler):
    """
    A :class:`tornado.web.RequestHandler` to serve up files that wind up in a
    given user's `session_dir` in the 'downloads' directory.  Generally speaking
    these files are generated by the terminal emulator (e.g. cat somefile.pdf)
    but it could be used by plugins as a way to serve up temporary files as
    well.
    """
    # NOTE:  This is a modified version of torando.web.StaticFileHandler
    @tornado.web.authenticated
    def get(self, path, include_body=True):
        session_dir = self.settings['session_dir']
        user = self.current_user
        if user and 'session' in user:
            session = user['session']
        else:
            logging.error(_("DownloadHandler: Could not determine use session"))
            return # Something is wrong
        filepath = os.path.join(session_dir, session, 'downloads', path)
        abspath = os.path.abspath(filepath)
        if not os.path.exists(abspath):
            self.set_status(404)
            self.write(self.get_error_html(404))
            return
        if not os.path.isfile(abspath):
            raise tornado.web.HTTPError(403, "%s is not a file", path)
        import stat, mimetypes
        stat_result = os.stat(abspath)
        modified = datetime.fromtimestamp(stat_result[stat.ST_MTIME])
        self.set_header("Last-Modified", modified)
        mime_type, encoding = mimetypes.guess_type(abspath)
        if mime_type:
            self.set_header("Content-Type", mime_type)
        # Set the Cache-Control header to private since this file is not meant
        # to be public.
        self.set_header("Cache-Control", "private")
        # Check the If-Modified-Since, and don't send the result if the
        # content has not been modified
        ims_value = self.request.headers.get("If-Modified-Since")
        if ims_value is not None:
            import email.utils
            date_tuple = email.utils.parsedate(ims_value)
            if_since = datetime.fromtimestamp(time.mktime(date_tuple))
            if if_since >= modified:
                self.set_status(304)
                return
        # Finally, deliver the file
        with open(abspath, "rb") as file:
            data = file.read()
            hasher = hashlib.sha1()
            hasher.update(data)
            self.set_header("Etag", '"%s"' % hasher.hexdigest())
            if include_body:
                self.write(data)
            else:
                assert self.request.method == "HEAD"
                self.set_header("Content-Length", len(data))

    def get_error_html(self, status_code, **kwargs):
        self.require_setting("static_url")
        if status_code in [404, 500, 503, 403]:
            filename = os.path.join(self.settings['static_url'], '%d.html' % status_code)
            if os.path.exists(filename):
                f = open(filename, 'r')
                data = f.read()
                f.close()
                return data
        import httplib
        return "<html><title>%(code)d: %(message)s</title>" \
                "<body class='bodyErrorPage'>%(code)d: %(message)s</body></html>" % {
            "code": status_code,
            "message": httplib.responses[status_code],
        }

class MainHandler(BaseHandler):
    """
    Renders index.html which loads Gate One.

    Will include the minified version of gateone.js if available as
    gateone.min.js.

    Will encode GATEONE_DIR/static/bell.ogg as a data:URI and put it as the
    <source> of the <audio> tag inside the index.html template.  Gate One
    administrators can replace bell.ogg with whatever they like but the file
    size should be less than 32k when encoded to Base64.
    """
    @tornado.web.authenticated
    @tornado.web.addslash
    # TODO: Get this auto-minifying gateone.js
    def get(self):
        hostname = os.uname()[1]
        location = self.get_argument("location", "default")
        prefs = self.get_argument("prefs", None)
        gateone_js = "%sstatic/gateone.js" % self.settings['url_prefix']
        minified_js_abspath = os.path.join(GATEONE_DIR, 'static')
        minified_js_abspath = os.path.join(
            minified_js_abspath, 'gateone.min.js')
        js_init = self.settings['js_init']
        # Use the minified version if it exists
        if os.path.exists(minified_js_abspath):
            gateone_js = "%sstatic/gateone.min.js" % self.settings['url_prefix']
        template_path = os.path.join(GATEONE_DIR, 'templates')
        index_path = os.path.join(template_path, 'index.html')
        head_html = ""
        body_html = ""
        for plugin, hooks in PLUGIN_HOOKS.items():
            if 'HTML' in hooks:
                if 'head' in hooks['HTML']:
                    if hooks['HTML']['head']:
                        for item in hooks['HTML']['head']:
                            head_html += "%s\n" % item
                if 'body' in hooks['HTML']:
                    if hooks['HTML']['body']:
                        for item in hooks['HTML']['body']:
                            body_html += "%s\n" % item
        self.render(
            index_path,
            hostname=hostname,
            gateone_js=gateone_js,
            jsplugins=PLUGINS['js'],
            cssplugins=PLUGINS['css'],
            location=location,
            js_init=js_init,
            url_prefix=self.settings['url_prefix'],
            head=head_html,
            body=body_html,
            prefs=prefs
        )

class GOApplication(object):
    """
    The base from which all Gate One Applications will inherit.  Applications
    are expected to be written like so::

        class SomeApplication(GOApplication):
            def initialize(self):
                "Called when the Application is instantiated."
                initialize_stuff()
                # Here's some good things to do in an initialize() function...
                # Register a policy-checking function:
                self.ws.security.update({'some_app': policy_checking_func})
                # Register some WebSocket actions (note the app:action naming convention)
                self.ws.commands.update({
                    'some_app:do_stuff': self.do_stuff,
                    'some_app:do_other_stuff': self.do_other_stuff
                })
            def open(self):
                "Called when the connection is established."
                # Setup whatever is necessary for session tracking and whatnot.
            def authenticate(self):
                "Called when the user *successfully* authenticates."
                # Here's the best place to instantiate things, send the user
                # JavaScript/CSS files, and similar post-authentication details.
            def on_close(self):
                "Called when the connection is closed."
                # This is a good place to halt any background/periodic operations.

    GOApplications will be automatically imported into Gate One and registered
    appropriately as long as they follow the following conventions:

        * The application and its module(s) should live inside its own directory inside the 'applications' directory.  For example, `/opt/gateone/applications/some_app/some_app.py`
        * Subclasses of `GOApplication` must be added to an `apps` global (list) inside of the application's module(s) like so: `apps = [SomeApplication]` (usually a good idea to put that at the very bottom of the module).

    .. note:: All .py modules inside of the application's main directory will be imported even if they do not contain or register a `GOApplication`.

    .. tip:: You can add command line arguments to Gate One by calling :func:`tornado.options.define` anywhere in your application's global namespace.  This works because the :func:`~tornado.options.define` function registers options in Gate One's global namespace (as `tornado.options.options`) and Gate One imports application modules before it evaluates command line arguments.
    """
    def __init__(self, ws):
        self.ws = ws # WebSocket instance
        # Setup some shortcuts to make things more natural and convenient
        self.write_message = ws.write_message
        self.close = ws.close
        self.get_current_user = ws.get_current_user
        self.current_user = ws.current_user
        self.security = ws.security
        self.request = ws.request
        self.settings = ws.settings
        self.on = ws.on
        self.off = ws.off

    def __repr__(self):
        return "GOApplication: %s" % self.__class__

    def initialize(self):
        """
        Called by :meth:`ApplicationWebSocket.open` after __init__().
        GOApplications can override this function to perform their own actions
        when the WebSocket is initialized.
        """
        pass

    def open(self):
        """
        Called by :meth:`ApplicationWebSocket.open` after the WebSocket is
        opened.  GOApplications can override this function to perform their own
        actions when the WebSocket is opened.
        """
        pass

    def on_close(self):
        """
        Called by :meth:`ApplicationWebSocket.on_close` after the WebSocket is
        closed.  GOApplications can override this function to perform their own
        actions when the WebSocket is closed.
        """
        pass

    def trigger(self, events, *args, **kwargs):
        """
        A clone of :meth:`ApplicationWebSocket.trigger` that calls registered
        callbacks with `self` from :class:`GOApplication` (as opposed to the
        `self` from :class:`ApplicationWebSocket`).  This gives Applications and
        plugins the ability to call :meth:`self.trigger` or
        :meth:`self.ws.trigger` depending on what is most appropriate for the
        given event.
        """
        if isinstance(events, basestring):
            events = [events]
        for event in events:
            if event in self.ws._events:
                for callback_obj in self.ws._events[event]:
                    callback_obj['callback'](self, *args, **kwargs)
                    callback_obj['calls'] += 1
                    if callback_obj['calls'] == callback_obj['times']:
                        self.off(event, callback_obj['callback'])

    def add_handler(self, pattern, handler, **kwargs):
        """
        Adds the given *handler* (`tornado.web.RequestHandler`) to the Tornado
        Application (`self.ws.application`) to handle URLs matching *pattern*.
        If given, *kwargs* will be added to the `tornado.web.URLSpec` when the
        complete handler is assembled.

        .. note:: If the *pattern* does not start with the configured `url_prefix` it will be automatically prepended.
        """
        logging.debug("Adding handler: (%s, %s)" % (pattern, handler))
        url_prefix = self.ws.settings['url_prefix']
        if not pattern.startswith(url_prefix):
            if pattern.startswith('/'):
                # Get rid of the / (it will be in the url_prefix)
                pattern = pattern.lstrip('/')
        spec = tornado.web.URLSpec(pattern, handler, kwargs)
        # Why the Tornado devs didn't give us a simple way to do this is beyond
        # me.
        self.ws.application.handlers[0][1].append(spec)

class ApplicationWebSocket(WebSocketHandler):
    """
    The main WebSocket interface for Gate One, this class is setup to call
    'commands' (aka WebSocket Actions) which are methods registered in
    `self.commands`.  Methods that are registered this way will be exposed and
    directly callable over the WebSocket.
    """
    instances = set()
    # These three attributes handle watching files for changes:
    watched_files = {}     # Format: {<file path>: <modification time>}
    file_update_funcs = {} # Format: {<file path>: <function called on update>}
    file_watcher = None    # Will be replaced with a PeriodicCallback
    prefs = {} # Gets updated with every call to open()
    def __init__(self, application, request, **kwargs):
        self.user = None
        self.commands = {
            'ping': self.pong,
            'authenticate': self.authenticate,
            'get_style': self.get_style,
            'get_js': self.get_js,
            'enumerate_themes': self.enumerate_themes,
            'go:send_user_message': self.send_user_message,
            'go:broadcast': self.broadcast
        }
        self._events = {}
        # This is used to keep track of used API authentication signatures so
        # we can prevent replay attacks.
        self.prev_signatures = []
        self.origin_denied = True # Only allow valid origins
        self.file_cache = FILE_CACHE # So applications and plugins can reference
        self.persist = PERSIST # So applications and plugins can reference
        self.apps = [] # Gets filled up by self.initialize()
        # The security dict stores applications' various policy functions
        self.security = {}
        WebSocketHandler.__init__(self, application, request, **kwargs)

    @classmethod
    def file_checker(cls):
        #logging.debug("file_checker()") # Kinda noisy so I've commented it out
        if not SESSIONS:
            # No connected sessions; no point in watching files
            cls.file_checker.stop()
            # Also remove the broadcast file so we know to start up the
            # file_watcher again if a user connects.
            session_dir = cls.prefs['*']['gateone']['session_dir']
            broadcast_file = os.path.join(session_dir, 'broadcast') # Default
            broadcast_file = cls.prefs['*']['gateone'].get(
                'broadcast_file', broadcast_file) # If set, use that
            del cls.watched_files[broadcast_file]
            del cls.file_update_funcs[broadcast_file]
            os.remove(broadcast_file)
        for path, mtime in cls.watched_files.items():
            if os.stat(path).st_mtime == mtime:
                continue
            try:
                cls.file_update_funcs[path]()
            except Exception as e:
                logging.error(_(
                    "Exception encountered trying to execute the file update "
                    "function for %s..." % path))
                logging.error(e)

    @classmethod
    def watch_file(cls, path, func):
        """
        Registers the given file *path* and *func* in
        `ApplicationWebSocket.watched_files`.  The *func* will be called if the
        file at *path* is modified.
        """
        cls.watched_files.update({path: os.stat(path).st_mtime})
        cls.file_update_funcs.update({path: func})

    @classmethod
    def broadcast_file_update(cls):
        """
        Called when there's an update to the 'broadcast_file', broadcasts its
        contents to all connected users.
        """
        session_dir = cls.prefs['*']['gateone']['session_dir']
        broadcast_file = os.path.join(session_dir, 'broadcast')
        broadcast_file = cls.prefs['*']['gateone'].get(
            'broadcast_file', broadcast_file)
        with open(broadcast_file) as f:
            message = f.read()
        if message:
            message = message.rstrip()
            logging.info("Broadcast (via broadcast_file): %s" % message)
            message_dict = {'notice': message}
            cls._deliver(message_dict, upn="AUTHENTICATED")
            open(broadcast_file, 'w').write('') # Empty it out

    def initialize(self, apps=None, **kwargs):
        """
        This gets called by the Tornado framework when ApplicationWebSocket is
        instantiated.  It will be passed the list of *apps* (Gate One
        applications) that are assigned inside the :class:`Application` object.
        These *apps* will be mutated in-place so that `self` will refer to the
        current instance of :class:`ApplicationWebSocket`.  Kind of like a
        dynamic mixin.
        """
        logging.debug('ApplicationWebSocket.initialize(%s)' % apps)
        # Make sure we have all prefs ready for checking
        cls = ApplicationWebSocket
        cls.prefs = get_settings(os.path.join(GATEONE_DIR, 'settings'))
        if not apps:
            return
        for app in apps:
            instance = app(self)
            self.apps.append(instance)
            logging.debug("Initializing %s" % instance)
            if hasattr(instance, 'initialize'):
                instance.initialize()

    def on(self, events, callback, times=None):
        """
        Registers the given *callback* with the given *events* (string or list
        of strings) that will get called whenever the given *event* is triggered
        (using :meth:`ApplicationWebSocket.trigger`).  It works similarly to
        :js:meth:`GateOne.Events.on` in gateone.js.

        If *times* is given the *callback* will only be fired that many times
        before it is automatically removed from
        :attr:`ApplicationWebSocket._events`.
        """
        if isinstance(events, basestring):
            events = [events]
        callback_obj = {
            'callback': callback,
            'times': times,
            'calls': 0
        }
        for event in events:
            if event not in self._events:
                self._events.update({event: [callback_obj.copy()]})
            else:
                self._events[event].append(callback_obj.copy())

    def off(self, events, callback):
        """
        Removes the given *callback* from the given *events* (string or list of
        strings).
        """
        if isinstance(events, basestring):
            events = [events]
        for event in events:
            for callback_obj in self._events[event]:
                if callback_obj['callback'] == callback:
                    try:
                        del self._events[event]
                    except KeyError:
                        pass # Nothing to do

    def once(self, events, callback):
        """
        A shortcut for :meth:`self.on(events, callback, 1)`
        """
        self.on(events, callback, 1)

    def trigger(self, events, *args, **kwargs):
        """
        Fires the given *events* (string or list of strings).  All callbacks
        associated with these *events* will be called and if their respective
        objects have a *times* value set it will be used to determine when to
        remove the associated callback from the event.

        If given, callbacks associated with the given *events* will be called
        with *args* and *kwargs*.
        """
        if isinstance(events, basestring):
            events = [events]
        for event in events:
            if event in self._events:
                for callback_obj in self._events[event]:
                    callback_obj['callback'](self, *args, **kwargs)
                    callback_obj['calls'] += 1
                    if callback_obj['calls'] == callback_obj['times']:
                        self.off(event, callback_obj['callback'])

    def allow_draft76(self):
        """
        By overriding this function we're allowing the older version of the
        WebSockets protocol.  As long as communications happens over SSL there
        shouldn't be any security concerns with this.  This is mostly to support
        iOS Safari.
        """
        return True

    def get_current_user(self):
        """
        Mostly identical to the function of the same name in MainHandler.  The
        difference being that when API authentication is enabled the WebSocket
        will expect and perform its own auth of the client.
        """
        if self.user:
            return self.user
        user_json = self.get_secure_cookie("gateone_user")
        if not user_json:
            if not self.settings['auth']:
                # This can happen if the user's browser isn't allowing
                # persistent cookies (e.g. incognito mode)
                return {'upn': 'ANONYMOUS', 'session': generate_session_id()}
            return None
        user = json_decode(user_json)
        user['ip_address'] = self.request.remote_ip
        return user

    def open(self):
        """
        Called when a new WebSocket is opened.  Will deny access to any
        origin that is not defined in self.settings['origin'].
        """

        cls = ApplicationWebSocket
        cls.instances.add(self)
        valid_origins = self.settings['origins']
        if 'Origin' in self.request.headers:
            origin = self.request.headers['Origin']
        elif 'Sec-Websocket-Origin' in self.request.headers: # Old version
            origin = self.request.headers['Sec-Websocket-Origin']
        origin = origin.lower() # hostnames are case-insensitive
        origin = origin.split('://', 1)[1]
        logging.debug("open() origin: %s" % origin)
        if '*' not in valid_origins:
            if origin not in valid_origins:
                self.origin_denied = True
                denied_msg = _("Access denied for origin: %s" % origin)
                logging.error(denied_msg)
                self.write_message(denied_msg)
                self.write_message(_(
                    "If you feel this is incorrect you just have to add '%s' to"
                    " the 'origin' option in your settings.  See the docs "
                    "for details." % origin
                ))
                self.close()
        self.origin_denied = False
        # client_id is unique to the browser/client whereas session_id is unique
        # to the user.  It isn't used much right now but it will be useful in
        # the future once more stuff is running over WebSockets.
        self.client_id = generate_session_id()
        client_address = self.request.connection.address[0]
        user = self.current_user
        # NOTE: self.current_user will call self.get_current_user() the first
        # time it is used.
        if user and 'upn' in user:
            logging.info(
                _("WebSocket opened (%s %s) via origin %s.") % (
                    user['upn'], client_address, origin))
        else:
            logging.info(_("WebSocket opened (unknown user)."))
        if user and 'upn' not in user: # Invalid user info
            logging.error(_("Unauthenticated WebSocket attempt."))
            # In case this is a legitimate client that simply had its auth info
            # expire/go bad, tell it to re-auth by calling the appropriate
            # action on the other side.
            message = {'reauthenticate': True}
            self.write_message(json_encode(message))
            self.close() # Close the WebSocket
        # NOTE: By getting the prefs with each call to open() we make
        #       it possible to make changes inside the settings dir without
        #       having to restart Gate One (just need to wait for users to
        #       eventually re-connect or reload the page).
        # NOTE: Why store prefs in the class itself?  No need for redundancy.
        if 'cache_dir' not in cls.prefs['*']['gateone']:
            # Set the cache dir to a default if not set in the prefs
            import tempfile
            cache_dir = os.path.join(tempfile.gettempdir(), 'gateone_cache')
            cls.prefs['*']['gateone']['cache_dir'] = cache_dir
            if self.settings['debug']:
                # Clean out the cache_dir every page reload when in debug mode
                for fname in os.listdir(cache_dir):
                    filepath = os.path.join(cache_dir, fname)
                    os.remove(filepath)
        for app in self.apps: # Call applications' open() functions (if any)
            if hasattr(app, 'open'):
                app.open()

    def on_message(self, message):
        """Called when we receive a message from the client."""
        # This is super useful when debugging:
        logging.debug("message: %s" % repr(message))
        if self.origin_denied:
            logging.error(_("Message rejected due to invalid origin."))
            self.close() # Close the WebSocket
        message_obj = None
        try:
            message_obj = json_decode(message) # JSON FTW!
            if not isinstance(message_obj, dict):
                self.write_message(_("'Error: Message bust be a JSON dict.'"))
                return
        except ValueError: # We didn't get JSON
            self.write_message(_("'Error: We only accept JSON here.'"))
            return
        if message_obj:
            for key, value in message_obj.items():
                if key in PLUGIN_WS_CMDS:
                    try: # Plugins first so they can override behavior
                        PLUGIN_WS_CMDS[key](value, tws=self)
                        # tws==ApplicationWebSocket
                    except (KeyError, TypeError, AttributeError) as e:
                        logging.error(_(
                            "Error running plugin WebSocket action: %s" % key))
                else:
                    try:
                        if value:
                            self.commands[key](value)
                        else:
                            # Try, try again
                            self.commands[key]()
                    except (KeyError, TypeError, AttributeError) as e:
                        import traceback
                        for frame in traceback.extract_tb(sys.exc_info()[2]):
                            fname, lineno, fn, text = frame
                        logging.error(_(
                         "Error/Unknown WebSocket action, %s: %s (%s line %s)" %
                         (key, e, fname, lineno)))

    def on_close(self):
        """
        Called when the client terminates the connection.
        """
        logging.debug("on_close()")
        ApplicationWebSocket.instances.discard(self)
        user = self.current_user
        client_address = self.request.connection.address[0]
        if user and user['session'] in SESSIONS:
            # Update 'last_seen' with a datetime object for accuracy
            SESSIONS[user['session']]['last_seen'] = datetime.now()
        if user and 'upn' in user:
            logging.info(
                _("WebSocket closed (%s %s).") % (user['upn'], client_address))
        else:
            logging.info(_("WebSocket closed (unknown user)."))
        # Call applications' on_close() functions (if any)
        for app in self.apps:
            if hasattr(app, 'on_close'):
                app.on_close()

    def pong(self, timestamp):
        """
        Responds to a client 'ping' request...  Just returns the given
        timestamp back to the client so it can measure round-trip time.
        """
        message = {'pong': timestamp}
        self.write_message(json_encode(message))

    def authenticate(self, settings):
        """
        Authenticates the client by first trying to use the 'gateone_user'
        cookie or if Gate One is configured to use API authentication it will
        use *settings['auth']*.  Additionally, it will accept
        *settings['container']* and *settings['prefix']* to apply those to the
        equivalent properties (self.container and self.prefix).

        If *settings['location']* is something other than 'default' all new
        terminals will be associated with the given (string) value.  These
        terminals will be treated separately from the usual terminals so they
        can exist in a different browser tab/window.
        """
        logging.debug("authenticate(): %s" % settings)
        if 'Origin' in self.request.headers:
            origin = self.request.headers['Origin']
        elif 'Sec-Websocket-Origin' in self.request.headers: # Old version
            origin = self.request.headers['Sec-Websocket-Origin']
        # Make sure the client is authenticated if authentication is enabled
        if self.settings['auth'] and self.settings['auth'] != 'api':
            try:
                user = self.current_user
                if not user:
                    logging.error(_("Unauthenticated WebSocket attempt."))
                    # This usually happens when the cookie_secret gets changed
                    # resulting in "Invalid cookie..." errors.  If we tell the
                    # client to re-auth the problem should correct itself.
                    message = {'reauthenticate': True}
                    self.write_message(json_encode(message))
                    return
                elif user and user['upn'] == 'ANONYMOUS':
                    logging.error(_("Unauthenticated WebSocket attempt."))
                    # This can happen when a client logs in with no auth type
                    # configured and then later the server is configured to use
                    # authentication.  The client must be told to re-auth:
                    message = {'reauthenticate': True}
                    self.write_message(json_encode(message))
                    return
            except KeyError: # 'upn' wasn't in user
                # Force them to authenticate
                message = {'reauthenticate': True}
                self.write_message(json_encode(message))
                self.close() # Close the WebSocket
        elif self.settings['auth'] and self.settings['auth'] == 'api':
            if 'auth' in settings.keys():
                # 'auth' message should look like this:
                # {
                #    'api_key': 'MjkwYzc3MDI2MjhhNGZkNDg1MjJkODgyYjBmN2MyMTM4M',
                #    'upn': 'joe@company.com',
                #    'timestamp': '1323391717238',
                #    'signature': <gibberish>,
                #    'signature_method': 'HMAC-SHA1',
                #    'api_version': '1.0'
                # }
                #
                # *api_key* is the first half of what gets generated when you
                #   run ./gateone --new_api_key.
                # *upn* is the User Principal Name of the user.  This is
                #   typically something like "joe@company.com".
                # *timestamp* is a JavaScript Date() object converted into an
                #   "time since the epoch" (int or string is OK):
                #       var timestamp = new Date().getTime()
                # *signature* is an HMAC signature of the previous three
                #   variables that was created using the given API key's secret.
                # *signature_method* is the HMAC hashing algorithm to use for
                #   the signature.  Only HMAC-SHA1 is supported for now.
                # *api_version* is the auth API version.  Always "1.0" for now.
                #
                # For reference, here's how to make a signature using PHP:
                # $authobj = array('api_key' => 'M2I1MzJmZjk4MTEwNDk2Zjk4MjMwNmMwMTVkODQzMTEyO', 'upn' => $_SERVER['REMOTE_USER'], 'timestamp' => time() . '0000', 'signature_method' => 'HMAC-SHA1', 'api_version' => '1.0');
                # $authobj['signature'] = hash_hmac('sha1', $authobj['api_key'] . $authobj['upn'] . $authobj['timestamp'], '<secret>');
                # Note that the order matters:  api_key -> upn -> timestamp
                auth_obj = settings['auth']
                if 'api_key' in auth_obj:
                    # Assume everything else is present if the api_key is there
                    api_key = auth_obj['api_key']
                    upn = auth_obj['upn']
                    timestamp = str(auth_obj['timestamp'])
                    signature = auth_obj['signature']
                    signature_method = auth_obj['signature_method']
                    api_version = auth_obj['api_version']
                    if signature_method != 'HMAC-SHA1':
                        logging.error(_(
                                'AUTHENTICATION ERROR: Unsupported API auth '
                                'signature method: %s' % signature_method))
                        message = {'reauthenticate': True}
                        self.write_message(json_encode(message))
                        return
                    if api_version != "1.0":
                        logging.error(_(
                                'AUTHENTICATION ERROR: Unsupported API version:'
                                '%s' % api_version))
                        message = {'reauthenticate': True}
                        self.write_message(json_encode(message))
                        return
                    try:
                        secret = self.settings['api_keys'][api_key]
                    except KeyError:
                        logging.error(_(
                            'AUTHENTICATION ERROR: API Key not found.'))
                        message = {'reauthenticate': True}
                        self.write_message(json_encode(message))
                        return
                    # Check the signature against existing API keys
                    sig_check = tornado.web._create_signature(
                        secret, api_key, upn, timestamp)
                    if sig_check == signature:
                        # Everything matches (great!) so now we do due diligence
                        # by checking the timestamp against the
                        # api_timestamp_window setting and whether or not we've
                        # already used it (to prevent replay attacks).
                        if signature in self.prev_signatures:
                            logging.error(_(
                            "API authentication replay attack detected!  User: "
                            "%s, Remote IP: %s, Origin: %s" % (
                                upn, self.request.remote_ip, origin)))
                            message = {'notice': _(
                                'AUTH FAILED: Replay attack detected!  This '
                                'event has been logged.')}
                            self.write_message(json_encode(message))
                            self.close()
                            return
                        window = self.settings['api_timestamp_window']
                        then = datetime.fromtimestamp(int(timestamp)/1000)
                        time_diff = datetime.now() - then
                        if time_diff > window:
                            logging.error(_(
                            "API authentication failed due to an expired auth "
                            "object.  If you just restarted the server this is "
                            "normal (users just need to reload the page).  If "
                            " this problem persists it could be a problem with "
                            "the server's clock (either this server or the "
                            "server(s) embedding Gate One)."
                            ))
                            message = {'notice': _(
                                'AUTH FAILED: Authentication object timed out. '
                                'Try reloading this page (F5).')}
                            self.write_message(json_encode(message))
                            message = {'notice': _(
                                'AUTH FAILED: If the problem persists after '
                                'reloading this page please contact your server'
                                ' administrator to notify them of the issue.')}
                            self.write_message(json_encode(message))
                            self.close()
                            return
                        logging.debug(_("API Authentication Successful"))
                        self.prev_signatures.append(signature) # Prevent replays
                # Make a directory to store this user's settings/files/logs/etc
                        user_dir = os.path.join(self.settings['user_dir'], upn)
                        if not os.path.exists(user_dir):
                            logging.info(
                                _("Creating user directory: %s" % user_dir))
                            mkdir_p(user_dir)
                            os.chmod(user_dir, 0o770)
                        session_file = os.path.join(user_dir, 'session')
                        if os.path.exists(session_file):
                            session_data = open(session_file).read()
                            self.user = json_decode(session_data)
                        else:
                            with open(session_file, 'w') as f:
                        # Save it so we can keep track across multiple clients
                                self.user = {
                                    'upn': upn, # FYI: UPN == userPrincipalName
                                    'session': generate_session_id()
                                }
                                session_info_json = json_encode(self.user)
                                f.write(session_info_json)
                        # Attach any additional provided keys/values to the user
                        # object so applications embedding Gate One can use
                        # them in their own plugins and whatnot.
                        known_params = [
                            'api_key',
                            'api_version',
                            'timestamp',
                            'upn',
                            'signature',
                            'signature_method'
                        ]
                        for key, value in auth_obj.items():
                            if key not in known_params:
                                self.user[key] = value
                        # user dicts need a little extra attention for IPs...
                        self.user['ip_address'] = self.request.remote_ip
                        # Force-set the current user:
                        self._current_user = self.user
                    else:
                        logging.error(_(
                            "WebSocket auth failed signature check."))
                        message = {'reauthenticate': True}
                        self.write_message(json_encode(message))
                        return
            else:
                logging.error(_("Missing API Key in authentication object"))
                message = {'reauthenticate': True}
                self.write_message(json_encode(message))
                return
        else: # Anonymous auth
            # Double-check there isn't a user set in the cookie (i.e. we have
            # recently changed Gate One's settings).  If there is, force it
            # back to ANONYMOUS.
            if settings['auth']:
                cookie_data = None
                if isinstance(settings['auth'], basestring):
                    # The client is trying to authenticate using the
                    # 'gateone_user' parameter in localStorage.
                    # Authenticate/decode the encoded auth info
                    cookie_data = self.get_secure_cookie(
                        'gateone_user', value=settings['auth'])
                    # NOTE: The above doesn't actually touch any cookies
                else:
                    # Someone is attempting to perform API-based authentication
                    # but this server isn't configured with 'auth = "api"'.
                    # Let's be real user-friendly and point out this mistake
                    # with a helpful error message...
                    logging.error(_(
                        "Client tried to use API-based authentication but this "
                        "server is configured with 'auth = \"%s\".  Did you "
                        "forget to set 'auth = \"api\" in your settings?" %
                        self.settings['auth']))
                    message = {'notice': _(
                        "AUTHENTICATION ERROR: Server is not configured to "
                        "perform API-based authentication.  Did someone forget "
                        "to set 'auth = \"api\" in the settings?")}
                    self.write_message(json_encode(message))
                    return
                if cookie_data:
                    self.user = json_decode(cookie_data)
            if not self.user:
                # Generate a new session/anon user
                self.user = self.current_user
                # Also store/update their session info in localStorage
                encoded_user = self.create_signed_value(
                    'gateone_user', tornado.escape.json_encode(self.user))
                session_message = {'gateone_user': encoded_user}
                self.write_message(json_encode(session_message))
            if self.user['upn'] != 'ANONYMOUS':
                # Gate One server's auth config probably changed
                message = {'reauthenticate': True}
                self.write_message(json_encode(message))
                #self.close() # Close the WebSocket
                return
        try:
            user = self.current_user
            if user and 'session' in user:
                self.session = user['session']
            else:
                logging.error(_("Authentication failed for unknown user"))
                message = {'notice': _('AUTHENTICATION ERROR: User unknown')}
                self.write_message(json_encode(message))
                return
        except Exception as e:
            logging.error(_(
                "Exception encountered trying to authenticate: %s" % e))
            return
        try:
            # Execute any post-authentication hooks that plugins have registered
            if PLUGIN_AUTH_HOOKS:
                for auth_hook in PLUGIN_AUTH_HOOKS:
                    auth_hook(self, self.current_user, self.settings)
        except Exception as e:
            logging.error(_("Exception in registered Auth hook: %s" % e))
        # Apply the container/prefix settings (if present)
        if 'container' in settings:
            self.container = settings['container']
        if 'prefix' in settings:
            self.prefix = settings['prefix']
        # Locations are used to differentiate between different tabs/windows
        self.location = 'default'
        if 'location' in settings:
            self.location = settings['location']
        # This check is to make sure there's no existing session so we don't
        # accidentally clobber it.
        if self.session not in SESSIONS:
            # Old session is no good, start a new one:
            SESSIONS[self.session] = {
                'last_seen': 'connected',
                'timeout_callbacks': [],
                # Locations are virtual containers that indirectly correlate
                # with browser windows/tabs.  The point is to allow things like
                # opening/moving applications/terminals in/to new windows/tabs.
                'locations': {self.location: {}}
            }
        else:
            SESSIONS[self.session]['last_seen'] = 'connected'
            if self.location not in SESSIONS[self.session]['locations']:
                SESSIONS[self.session]['locations'][self.location] = {}
        # A shortcut for SESSIONS[self.session]['locations']:
        self.locations = SESSIONS[self.session]['locations']
        # Send our plugin .js and .css files to the client
        self.send_plugin_static_files(os.path.join(GATEONE_DIR, 'plugins'))
        # Call applications' authenticate() functions (if any)
        for app in self.apps:
            if hasattr(app, 'authenticate'):
                app.authenticate()
        # This is just so the client has a human-readable point of reference:
        message = {'set_username': self.current_user['upn']}
        self.write_message(json_encode(message))
        # Startup the session watcher if it isn't already running
        global SESSION_WATCHER
        if not SESSION_WATCHER:
            interval = self.prefs['*']['gateone'].get(
                'session_timeout_check_interval', 30*1000) # 30s default
            SESSION_WATCHER = tornado.ioloop.PeriodicCallback(
                timeout_sessions, interval)
            SESSION_WATCHER.start()
        # Startup the log cleaner so that old user logs get cleaned up
        global CLEANER
        if not CLEANER:
            default_interval = 5*60*1000 # 5 minutes
            # NOTE: This interval isn't in the settings by default because it is
            # kind of obscure.  No reason to clutter things up.
            interval = self.prefs['*']['gateone'].get(
                'user_logs_cleanup_interval', default_interval)
            CLEANER = tornado.ioloop.PeriodicCallback(
                cleanup_user_logs, interval)
            CLEANER.start()
        # Startup the file watcher if it isn't already running and get it
        # watching the broadcast file.
        cls = ApplicationWebSocket
        broadcast_file = os.path.join(self.settings['session_dir'], 'broadcast')
        broadcast_file = self.prefs['*']['gateone'].get(
            'broadcast_file', broadcast_file)
        if broadcast_file not in cls.watched_files:
            # No broadcast file means the file watcher isn't running
            open(broadcast_file, 'w').write('') # Touch file
            check_time = self.prefs['*']['gateone'].get(
                'file_check_interval', 5000)
            cls.watch_file(broadcast_file, cls.broadcast_file_update)
            io_loop = tornado.ioloop.IOLoop.instance()
            cls.file_watcher = tornado.ioloop.PeriodicCallback(
                cls.file_checker, check_time, io_loop=io_loop)
            cls.file_watcher.start()
        self.trigger('go:authenticate')

    def render_style(self, style_path, **kwargs):
        """
        Renders the CSS template at *style_path* using *kwargs* and returns the
        path to the rendered result.  If the given style has already been
        rendered the existing cache path will be returned.

        This method also cleans up older versions of the same rendered template.
        """
        cache_dir = self.prefs['*']['gateone']['cache_dir']
        mtime = os.stat(style_path).st_mtime
        safe_path = style_path.replace('/', '_')
        rendered_filename = 'rendered_%s_%s' % (safe_path, int(mtime))
        rendered_path = os.path.join(cache_dir, rendered_filename)
        if not os.path.exists(rendered_path):
            style_css = self.render_string(
                style_path,
                **kwargs
            )
            if bytes != str: # Python 3
                style_css = str(style_css, 'UTF-8')
            with open(rendered_path, 'w') as f:
                f.write(style_css)
            # Remove older versions of the rendered template if present
            for fname in os.listdir(cache_dir):
                if fname == rendered_filename:
                    continue
                elif safe_path in fname:
                    # Older version present.
                    # Remove it (and it's minified counterpart).
                    os.remove(os.path.join(cache_dir, fname))
        return rendered_path

    def get_style(self, settings):
        """
        Sends the CSS stylesheets matching the properties specified in
        *settings* to the client.  *settings* must contain the following:

            * **container** - The element Gate One resides in (e.g. 'gateone')
            * **prefix** - The string being used to prefix all elements (e.g. 'go\_')

        *settings* may also contain any combination of the following:

            * **theme** - The name of the CSS theme to be retrieved.
            * **colors** - The name of the text color CSS scheme to be retrieved.
            * **plugins** - If true, will send all plugin .css files to the client.
            * **print** - If true, will send the print stylesheet.
        """
        logging.debug('get_style(%s)' % settings)
        send_css = self.prefs['*']['gateone'].get('send_css', True)
        if not send_css:
            if not hasattr('logged_css_message', self):
                logging.info(_(
                    "send_css is false; will not send JavaScript."))
            # So we don't repeat this message a zillion times in the logs:
            self.logged_css_message = True
            return
        from utils import get_or_cache
        cache_dir = self.prefs['*']['gateone']['cache_dir']
        if not os.path.exists(cache_dir):
            mkdir_p(cache_dir)
        out_dict = {'result': 'Success'}
        templates_path = os.path.join(GATEONE_DIR, 'templates')
        themes_path = os.path.join(templates_path, 'themes')
        colors_path = os.path.join(templates_path, 'term_colors')
        printing_path = os.path.join(templates_path, 'printing')
        go_url = settings['go_url'] # Used to prefix the url_prefix
        if not go_url.endswith('/'):
            go_url += '/'
        container = settings["container"]
        prefix = settings["prefix"]
        theme = None
        if 'theme' in settings:
            theme = settings["theme"]
        colors = None
        if 'colors' in settings:
            colors = settings["colors"]
        plugins = None
        if 'plugins' in settings:
            plugins = settings["plugins"]
        _print = None
        if 'print' in settings:
            _print = settings["print"]
        template_args = dict(
            container=container,
            prefix=prefix,
            url_prefix=go_url
        )
        if theme:
            theme_filename = "%s.css" % theme
            theme_path = os.path.join(themes_path, theme_filename)
            rendered_path = self.render_style(
                theme_path, **template_args)
            if self.settings['debug']:
                out_dict['theme'] = get_or_cache(
                    cache_dir, rendered_path, minify=False)
            else:
                out_dict['theme'] = get_or_cache(
                    cache_dir, rendered_path, minify=True)
            # Now enumerate all applications/plugins looking for their own
            # implementations of this theme (must have same name).
            theme_paths = []
            plugins_dir = os.path.join(GATEONE_DIR, 'plugins')
            # Find plugin's theme-specific CSS files
            for plugin in os.listdir(plugins_dir):
                plugin_dir = os.path.join(plugins_dir, plugin)
                themes_dir = os.path.join(plugin_dir, 'templates', 'themes')
                theme_css_file = os.path.join(themes_dir, theme_filename)
                if not os.path.exists(theme_css_file):
                    continue
                rendered_path = self.render_style(
                    theme_css_file, **template_args)
                if self.settings['debug']:
                    out_dict['theme'] += '\n' + get_or_cache(
                        cache_dir, rendered_path, minify=False)
                else:
                    out_dict['theme'] += '\n' + get_or_cache(
                        cache_dir, rendered_path, minify=True)
            # Find application's theme-specific CSS files
            applications_dir = os.path.join(GATEONE_DIR, 'applications')
            for app in os.listdir(applications_dir):
                app_dir = os.path.join(applications_dir, app)
                themes_dir = os.path.join(app_dir, 'templates', 'themes')
                theme_css_file = os.path.join(themes_dir, theme_filename)
                if not os.path.exists(theme_css_file):
                    continue
                rendered_path = self.render_style(
                    theme_css_file, **template_args)
                if self.settings['debug']:
                    out_dict['theme'] += '\n' + get_or_cache(
                        cache_dir, rendered_path, minify=False)
                else:
                    out_dict['theme'] += '\n' + get_or_cache(
                        cache_dir, rendered_path, minify=True)
                # Find application plugin's theme-specific CSS files
                plugins_dir = os.path.join(app_dir, 'plugins')
                if not os.path.exists(plugins_dir):
                    continue
                for plugin in os.listdir(plugins_dir):
                    plugin_dir = os.path.join(plugins_dir, plugin)
                    themes_dir = os.path.join(plugin_dir, 'templates', 'themes')
                    theme_css_file = os.path.join(themes_dir, theme_filename)
                    if not os.path.exists(theme_css_file):
                        continue
                    rendered_path = self.render_style(
                        theme_css_file, **template_args)
                    if self.settings['debug']:
                        out_dict['theme'] += '\n' + get_or_cache(
                            cache_dir, rendered_path, minify=False)
                    else:
                        out_dict['theme'] += '\n' + get_or_cache(
                            cache_dir, rendered_path, minify=True)
        # TODO: Move text color themes into the terminal application
        if colors:
            color_path = os.path.join(colors_path, "%s.css" % colors)
            rendered_path = self.render_style(color_path, **template_args)
            if self.settings['debug']:
                out_dict['colors'] = get_or_cache(
                    cache_dir, rendered_path, minify=False)
            else:
                out_dict['colors'] =  get_or_cache(
                    cache_dir, rendered_path, minify=True)
        if plugins:
            # Build a dict of plugins
            out_dict['plugins'] = {}
            plugins_dir = os.path.join(GATEONE_DIR, 'plugins')
            for f in os.listdir(plugins_dir):
                if os.path.isdir(os.path.join(plugins_dir, f)):
                    out_dict['plugins'][f] = ''
            # Add each plugin's CSS template(s) to its respective dict
            for plugin in list(out_dict['plugins'].keys()):
                plugin_templates_path = os.path.join(
                    plugins_dir, plugin, 'templates')
                if os.path.exists(plugin_templates_path):
                    for f in os.listdir(plugin_templates_path):
                        if f.endswith('.css'):
                            plugin_css_path = os.path.join(
                                plugin_templates_path, f)
                            rendered_path = self.render_style(
                                plugin_css_path, **template_args)
                            if self.settings['debug']:
                                out_dict['plugins'][plugin] += '\n'
                                out_dict['plugins'][plugin] += get_or_cache(
                                    cache_dir, rendered_path, minify=False)
                            else:
                                out_dict['plugins'][plugin] += '\n'
                                out_dict['plugins'][plugin] += get_or_cache(
                                    cache_dir, rendered_path, minify=True)
        if _print:
            print_css_path = os.path.join(printing_path, "default.css")
            rendered_path = self.render_style(print_css_path, **template_args)
            if self.settings['debug']:
                out_dict['print'] = get_or_cache(
                    cache_dir, rendered_path, minify=False)
            else:
                out_dict['print'] = get_or_cache(
                    cache_dir, rendered_path, minify=True)
        self.write_message(json_encode({'load_style': out_dict}))

    @require(authenticated())
    def get_js(self, filename):
        """
        Attempts to find the specified *filename* file in Gate One's static
        directories (GATEONE_DIR/static/ and each plugin's respective 'static'
        dir).

        In the event that a plugin's JavaScript file has the same name as a file
        in GATEONE_DIR/static/ the plugin's copy of the file will take
        precedence.  This is to allow plugins to override defaults.

        .. note:: This will alow authenticated clients to download whatever file they want that ends in .js inside of /static/ directories.
        """
        logging.debug('get_js(%s)' % filename)
        out_dict = {'result': 'Success', 'filename': filename, 'data': None}
        js_files = {} # Key:value == 'somefile.js': '/full/path/to/somefile.js'
        static_dir = os.path.join(GATEONE_DIR, 'static')
        for f in os.listdir(static_dir):
            if f.endswith('.js'):
                js_file_path = os.path.join(static_dir, f)
                js_files.update({f: js_file_path})
        # Build a list of plugins
        plugins = []
        plugins_dir = os.path.join(GATEONE_DIR, 'plugins')
        for f in os.listdir(plugins_dir):
            if os.path.isdir(os.path.join(plugins_dir, f)):
                plugins.append(f)
        # Add each found JS file to the respective dict
        for plugin in plugins:
            plugin_static_path = os.path.join(plugins_dir, plugin, 'static')
            if os.path.exists(plugin_static_path):
                for f in os.listdir(plugin_static_path):
                    if f.endswith('.js'):
                        js_file_path = os.path.join(plugin_static_path, f)
                        js_files.update({f: js_file_path})
        if filename in js_files.keys():
            with open(js_files[filename]) as f:
                out_dict['data'] = f.read()
        message = {'load_js': out_dict}
        self.write_message(message)

# NOTE:  This is a work in progress...  May be on hold for a while
    #def send_cache_request(self, path_or_fileobj, kind):
        #"""
        #Asks the client to use the cached copy of the given file at
        #*path_or_fileobj* by sending it the filename and it's modification time.
        #If the modification time does not match what's in the client's cache the
        #client is expected to send a request for the full file using the
        #'load_style' or 'load_js' WebSocket actions.
        #"""
        #if isinstance(path_or_fileobj, basestring):
            #path = path_or_fileobj
            #filename = os.path.split(path)[1]
            #mtime = os.stat(path).st_mtime
        #else:
            #path_or_fileobj.seek(0) # Just in case
            #path = path_or_fileobj.name
            #filename = os.path.split(path_or_fileobj.name)[1]
            #mtime = os.stat(path_or_fileobj.name).st_mtime
        #logging.debug('send_js_or_css(%s)' % path)
        ## Use a hash of the full file path as the identifier at the client
        ## (they don't need to know our filesystem layout).
        #from utils import short_hash
        #client_filename = short_hash(path)
        #if not os.path.exists(path):
            #logging.error(_("send_cache_request(): File not found: %s" % path))
            #return
        #out_dict = {
            #'filename': client_filename,
            #'mtime' = mtime
        #}
        #message = {'go:try_cached_file', out_dict}

    def send_js_or_css(self, path_or_fileobj, kind, element_id=None):
        """
        If *kind* is 'js', reads the given JavaScript file at *path_or_fileobj*
        and sends it to the client using the 'load_js' WebSocket action.
        If *kind* is 'css', reads the given CSS file at *path_or_fileobj*
        and sends it to the client using the 'load_style' WebSocket action.

        Optionally, *element_id* may be provided which will be assigned to the
        <script> or <style> tag that winds up being created.

        .. note:: Files will be cached after being minified until a file is modified or Gate One is restarted.

        If the `slimit` module is installed JavaScript files will be minified
        before being sent to the client.
        If the `cssmin` module is installed CSS files will be minified before
        being sent to the client.
        """
        if kind == 'js':
            send_js = self.prefs['*']['gateone'].get('send_js', True)
            if not send_js:
                if not hasattr('logged_js_message', self):
                    logging.info(_(
                        "send_js is false; will not send JavaScript."))
                # So we don't repeat this message a zillion times in the logs:
                self.logged_js_message = True
                return
        elif kind == 'css':
            send_css = self.prefs['*']['gateone'].get('send_css', True)
            if not send_css:
                if not hasattr('logged_css_message', self):
                    logging.info(_("send_css is false; will not send CSS."))
                # So we don't repeat this message a zillion times in the logs:
                self.logged_css_message = True
        if isinstance(path_or_fileobj, basestring):
            path = path_or_fileobj
            filename = os.path.split(path)[1]
            mtime = os.stat(path).st_mtime
        else:
            path_or_fileobj.seek(0) # Just in case
            path = path_or_fileobj.name
            filename = os.path.split(path_or_fileobj.name)[1]
            mtime = os.stat(path_or_fileobj.name).st_mtime
        logging.debug('send_js_or_css(%s)' % path)
        if not os.path.exists(path):
            logging.error(_("send_js_or_css(): File not found: %s" % path))
            return
        from utils import get_or_cache
        from hashlib import md5
        # Use a hash of the filename because these names can get quite long.
        # Also, we don't want to reveal the file structure on the server.
        filename_hash = md5(filename).hexdigest()[:10]
        out_dict = {
            'result': 'Success',
            'filename': filename_hash,
            'element_id': element_id
        }
        cache_dir = self.prefs['*']['gateone']['cache_dir']
        if self.settings['debug']:
            out_dict['data'] = get_or_cache(cache_dir, path, minify=False)
        else:
            out_dict['data'] = get_or_cache(cache_dir, path, minify=True)
        if kind == 'js':
            message = {'load_js': out_dict}
        elif kind == 'css':
            out_dict['css'] = True # So loadStyleAction() knows what to do
            message = {'load_style': out_dict}
        self.write_message(message)

    def send_js(self, path):
        """
        A shortcut for `self.send_js_or_css(path, 'js')`
        """
        self.send_js_or_css(path, 'js')

    def send_css(self, path):
        """
        A shortcut for `self.send_js_or_css(path, 'css')`
        """
        self.send_js_or_css(path, 'css')

    def render_and_send_css(self, css_path, **kwargs):
        """
        Renders, caches (in the `cache_dir`), and sends a stylesheet template at
        the given *css_path*.  The template will be rendered with the following
        keyword arguments::

            container = self.container
            prefix = self.prefix
            url_prefix = self.settings['url_prefix']
            **kwargs

        Returns the path to the rendered template.

        .. note:: If you want to serve Gate One's CSS via a different mechanism (e.g. nginx) this functionality can be completely disabled by adding `'send_css': false` to gateone/settings/10server.conf
        """
        send_css = self.prefs['*']['gateone'].get('send_css', True)
        if not send_css:
            if not hasattr('logged_css_message', self):
                logging.info(_("send_css is false; will not send CSS."))
            # So we don't repeat this message a zillion times in the logs:
            self.logged_css_message = True
            return
        cache_dir = self.prefs['*']['gateone']['cache_dir']
        mtime = os.stat(css_path).st_mtime
        safe_path = css_path.replace('/', '_') # So we can name the file safely
        rendered_filename = 'rendered_%s_%s' % (safe_path, int(mtime))
        rendered_path = os.path.join(cache_dir, rendered_filename)
        if os.path.exists(rendered_path):
            self.send_css(rendered_path)
            return
        with open(css_path) as f:
            css_template = tornado.template.Template(f.read())
        rendered = self.render_string(
            css_path,
            container=self.container,
            prefix=self.prefix,
            url_prefix=self.settings['url_prefix'],
            **kwargs
        )
        with open(rendered_path, 'w') as f:
            f.write(rendered)
        self.send_css(rendered_path)
        # Remove older versions of the rendered template if present
        for fname in os.listdir(cache_dir):
            if fname == rendered_filename:
                continue
            elif safe_path in fname:
                # Older version present.
                # Remove it (and it's minified counterpart).
                os.remove(os.path.join(cache_dir, fname))
        return rendered_path

    def send_plugin_static_files(self, plugins_dir, application=None):
        """
        Sends all plugin .js and .css files to the client that exist inside
        *plugins_dir*.  Optionally, if *application* is given the policies that
        apply to the current user for that application will be used to determine
        whether or not a given plugin's static files will be sent.

        .. note:: If you want to serve Gate One's JavaScript via a different mechanism (e.g. nginx) this functionality can be completely disabled by adding `'send_js': false` to gateone/settings/10server.conf
        """
        logging.debug('send_plugin_static_files(%s)' % plugins_dir)
        send_js = self.prefs['*']['gateone'].get('send_js', True)
        if not send_js:
            if not hasattr('logged_js_message', self):
                logging.info(_("send_js is false; will not send JavaScript."))
            # So we don't repeat this message a zillion times in the logs:
            self.logged_js_message = True
            return
        policy = applicable_policies(application, self.current_user, self.prefs)
        # This controls the client-side plugins that will be sent
        allowed_client_side_plugins = policy.get('user_plugins', [])
        # Build a list of plugins
        plugins = []
        if not os.path.exists(plugins_dir):
            return # Nothing to do
        for f in os.listdir(plugins_dir):
            if os.path.isdir(os.path.join(plugins_dir, f)):
                if allowed_client_side_plugins:
                    if f in allowed_client_side_plugins:
                        plugins.append(f)
                else:
                    plugins.append(f)
        # Add each found JS file to the respective dict
        for plugin in plugins:
            plugin_static_path = os.path.join(plugins_dir, plugin, 'static')
            if os.path.exists(plugin_static_path):
                static_files = os.listdir(plugin_static_path)
                static_files.sort()
                for f in static_files:
                    if f.endswith('.js'):
                        js_file_path = os.path.join(plugin_static_path, f)
                        self.send_js(js_file_path)
                    elif f.endswith('.css'):
                        css_file_path = os.path.join(plugin_static_path, f)
                        self.send_css(css_file_path)

# TODO:  Separate generic Gate One css from the terminal-specific stuff.
    def enumerate_themes(self):
        """
        Returns a JSON-encoded object containing the installed themes and text
        color schemes.
        """
        templates_path = os.path.join(GATEONE_DIR, 'templates')
        themes_path = os.path.join(templates_path, 'themes')
        colors_path = os.path.join(templates_path, 'term_colors')
        themes = os.listdir(themes_path)
        themes = [a.replace('.css', '') for a in themes]
        colors = os.listdir(colors_path)
        colors = [a.replace('.css', '') for a in colors]
        message = {'themes_list': {'themes': themes, 'colors': colors}}
        self.write_message(message)

# NOTE: This is not meant to be a chat application.  That is forthcoming :)
#       The real purpose of send_user_message() and broadcast() are for
#       programmatic use.  For example, when a user shares a terminal and it
#       would be appropriate to notify certain users that the terminal is now
#       available for them to connect.  This may use something other than the
#       'notice' WebSocket action in the future to avoid confusion (if need be).
    @require(authenticated(), policies('gateone'))
    def send_user_message(self, settings):
        """
        Sends the given *settings['message']* to the given *settings['upn']*.

        if *upn* is 'AUTHENTICATED' all users will get the message.
        """
        if 'message' not in settings:
            self.send_message(_("Error: No message to send."))
            return
        if 'upn' not in settings:
            self.send_message(_("Error: Missing UPN."))
            return
        self.send_message(settings['message'], upn=settings['upn'])
        self.trigger('go:send_user_message', settings)

    def send_message(self, message, upn=None, session=None):
        """
        Sends the given *message* to the client using the 'notice' WebSocket
        action at the currently-connected client.

        If *upn* is provided the *message* will be sent to all users with a
        matching 'upn' value.

        If *session* is provided the message will be sent to all users with a
        matching session ID.  This is useful in situations where all users share
        the same 'upn' (i.e. ANONYMOUS).

        if *upn* is 'AUTHENTICATED' all users will get the message.
        """
        message_dict = {'notice': message}
        if upn:
            ApplicationWebSocket._deliver(message_dict, upn=upn)
        elif session:
            ApplicationWebSocket._deliver(message_dict, session=session)
        else: # Just send to the currently-connected client
            self.write_message(message_dict)
        self.trigger('go:send_message', message, upn, session)

    @require(authenticated(), policies('gateone'))
    def broadcast(self, message):
        """
        Sends the given *message* (string) to all connected, authenticated
        users.
        """
        logging.info("Broadcast: %s" % message)
        from utils import strip_xss # Prevent XSS attacks
        message, bad_tags = strip_xss(message, replacement="entities")
        self.send_message(message, upn="AUTHENTICATED")
        self.trigger('go:broadcast', message)

    @classmethod
    def _deliver(cls, message, upn="AUTHENTICATED", session=None):
        """
        Writes the given *message* (string) to all users matching *upn* using
        the write_message() function.  If *upn* is not provided or is
        "AUTHENTICATED", will send the *message* to all users.

        Alternatively a *session* ID may be specified instead of a *upn*.  This
        is useful when more than one user shares a UPN (i.e. ANONYMOUS).
        """
        logging.debug("_deliver(%s, upn=%s, session=%s)" %
            (message, upn, session))
        for instance in cls.instances:
            try: # Only send to users that have authenticated
                user = instance.current_user
            except AttributeError:
                continue
            if session and user['session'] == session:
                instance.write_message(message)
            elif upn == "AUTHENTICATED":
                instance.write_message(message)
            elif upn == user['upn']:
                instance.write_message(message)

class ErrorHandler(tornado.web.RequestHandler):
    """
    Generates an error response with status_code for all requests.
    """
    def __init__(self, application, request, status_code):
        tornado.web.RequestHandler.__init__(self, application, request)
        self.set_status(status_code)

    def get_error_html(self, status_code, **kwargs):
        self.require_setting("static_url")
        if status_code in [404, 500, 503, 403]:
            filename = os.path.join(
                self.settings['static_url'], '%d.html' % status_code)
            if os.path.exists(filename):
                f = open(filename, 'r')
                data = f.read()
                f.close()
                return data
        import httplib
        return "<html><title>%(code)d: %(message)s</title>" \
           "<body class='bodyErrorPage'>%(code)d: %(message)s</body></html>" % {
               "code": status_code,
               "message": httplib.responses[status_code],
        }

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

class GateOneApp(tornado.web.Application):
    def __init__(self, settings, **kwargs):
        """
        Setup our Tornado application...  Everything in *settings* will wind up
        in the Tornado settings dict so as to be accessible under self.settings.
        """
        global PLUGIN_WS_CMDS
        global PLUGIN_COMMAND_HOOKS
        global PLUGIN_ESC_HANDLERS
        global PLUGIN_AUTH_HOOKS
        global PLUGIN_TERM_HOOKS
        global PLUGIN_NEW_TERM_HOOKS
        global PLUGIN_NEW_MULTIPLEX_HOOKS
        global PLUGIN_ENV_HOOKS
        # Base settings for our Tornado app
        static_url = os.path.join(GATEONE_DIR, "static")
        tornado_settings = dict(
            cookie_secret=settings['cookie_secret'],
            static_url=static_url,
            static_url_prefix="%sstatic/" % settings['url_prefix'],
            gzip=True,
            login_url="%sauth" % settings['url_prefix']
        )
        # Make sure all the provided settings wind up in self.settings
        for k, v in settings.items():
            tornado_settings[k] = v
        # Setup the configured authentication type
        AuthHandler = NullAuthHandler # Default
        if 'auth' in settings and settings['auth']:
            if settings['auth'] == 'kerberos' and KerberosAuthHandler:
                AuthHandler = KerberosAuthHandler
            elif settings['auth'] == 'pam' and PAMAuthHandler:
                AuthHandler = PAMAuthHandler
            elif settings['auth'] == 'google':
                AuthHandler = GoogleAuthHandler
            elif settings['auth'] == 'ssl':
                AuthHandler = SSLAuthHandler
            elif settings['auth'] == 'api':
                AuthHandler = APIAuthHandler
            logging.info(_("Using %s authentication" % settings['auth']))
        else:
            logging.info(_(
                "No authentication method configured. All users will be "
                "ANONYMOUS"))
        docs_path = os.path.join(GATEONE_DIR, 'docs')
        docs_path = os.path.join(docs_path, 'build')
        docs_path = os.path.join(docs_path, 'html')
        url_prefix = settings['url_prefix']
        if not url_prefix.endswith('/'):
            # Make sure there's a trailing slash
            url_prefix = "%s/" % url_prefix
        # Make the / optional in the regex so it works with the @addslash
        # decorator.  e.g. "/whatever/" would become "/whatever/?"
        index_regex = "%s?" % url_prefix
        # Setup our URL handlers
        handlers = [
            (index_regex, MainHandler),
            (r"%sws" % url_prefix,
                ApplicationWebSocket, dict(apps=APPLICATIONS)),
            (r"%sauth" % url_prefix, AuthHandler),
            (r"%sdownloads/(.*)" % url_prefix, DownloadHandler),
            (r"%sdocs/(.*)" % url_prefix, tornado.web.StaticFileHandler, {
                "path": docs_path,
                "default_filename": "index.html"
            })
        ]
        if 'web_handlers' in kwargs:
            for handler_tuple in kwargs['web_handlers']:
                regex = handler_tuple[0]
                handler = handler_tuple[1]
                kwargs = {}
                try:
                    kwargs = handler_tuple[2]
                except IndexError:
                    pass # No kwargs for this handler
                # Make sure the regex is prefix with the url_prefix
                if not regex.startswith(url_prefix):
                    regex = "%s%s" % (url_prefix, regex)
                handlers.append((regex, handler, kwargs))
        # Override the default static handler to ensure the headers are set
        # to allow cross-origin requests.
        handlers.append(
            (r"%sstatic/(.*)" % url_prefix, StaticHandler, {"path": static_url}
        ))
        # Hook up the hooks
        for plugin_name, hooks in PLUGIN_HOOKS.items():
            if 'Web' in hooks:
                # Apply the plugin's Web handlers
                fixed_hooks = []
                if isinstance(hooks['Web'], (list, tuple)):
                    for h in hooks['Web']:
                        # h == (regex, Handler)
                        if not h[0].startswith(url_prefix): # Fix it
                            h = (url_prefix + h[0].lstrip('/'), h[1])
                            fixed_hooks.append(h)
                        else:
                            fixed_hooks.append(h)
                else:
                    if not hooks['Web'][0].startswith(url_prefix): # Fix it
                        hooks['Web'] = (
                            url_prefix + hooks['Web'][0].lstrip('/'),
                            hooks['Web'][1]
                        )
                        fixed_hooks.append(hooks['Web'])
                    else:
                        fixed_hooks.append(hooks['Web'])
                handlers.extend(fixed_hooks)
            if 'WebSocket' in hooks:
                # Apply the plugin's WebSocket commands
                PLUGIN_WS_CMDS.update(hooks['WebSocket'])
            if 'Escape' in hooks:
                # Apply the plugin's Escape handler
                PLUGIN_ESC_HANDLERS.update({plugin_name: hooks['Escape']})
            if 'Auth' in hooks:
                # Apply the plugin's post-authentication functions
                if isinstance(hooks['Auth'], (list, tuple)):
                    PLUGIN_AUTH_HOOKS.extend(hooks['Auth'])
                else:
                    PLUGIN_AUTH_HOOKS.append(hooks['Auth'])
            if 'Command' in hooks:
                # Apply the plugin's 'Command' hooks (called by new_multiplex)
                if isinstance(hooks['Command'], (list, tuple)):
                    PLUGIN_COMMAND_HOOKS.extend(hooks['Command'])
                else:
                    PLUGIN_COMMAND_HOOKS.append(hooks['Command'])
            if 'Multiplex' in hooks:
                # Apply the plugin's Multiplex hooks (called by new_multiplex)
                if isinstance(hooks['Multiplex'], (list, tuple)):
                    PLUGIN_NEW_MULTIPLEX_HOOKS.extend(hooks['Multiplex'])
                else:
                    PLUGIN_NEW_MULTIPLEX_HOOKS.append(hooks['Multiplex'])
            if 'Terminal' in hooks:
                # Apply the plugin's Terminal hooks (called by new_terminal)
                PLUGIN_TERM_HOOKS.update(hooks['Terminal'])
            if 'TermInstance' in hooks:
                # Apply the plugin's TermInstance hooks (called by new_terminal)
                if isinstance(hooks['TermInstance'], (list, tuple)):
                    PLUGIN_NEW_TERM_HOOKS.extend(hooks['TermInstance'])
                else:
                    PLUGIN_NEW_TERM_HOOKS.append(hooks['TermInstance'])
            if 'Environment' in hooks:
                PLUGIN_ENV_HOOKS.update(hooks['Environment'])
            if 'Init' in hooks:
                # Call the plugin's initialization functions
                hooks['Init'](tornado_settings)
        # This removes duplicate handlers for the same regex, allowing plugins
        # to override defaults:
        handlers = merge_handlers(handlers)
        # Include JS-only and CSS-only plugins (for logging purposes)
        js_plugins = [a.split('/')[2] for a in PLUGINS['js']]
        css_plugins = []
        for i in css_plugins:
            if '?' in i: # CSS Template
                css_plugins.append(i.split('plugin=')[1].split('&')[0])
            else: # Static CSS file
                css_plugins.append(i.split('/')[1])
        plugin_list = list(set(PLUGINS['py'] + js_plugins + css_plugins))
        plugin_list.sort() # So there's consistent ordering
        logging.info(_("Loaded plugins: %s" % ", ".join(plugin_list)))
        tornado.web.Application.__init__(self, handlers, **tornado_settings)

def define_options():
    """
    Calls `tornado.options.define` for all of Gate One's command-line options.
    """
    # NOTE: To test this function interactively you must import tornado.options
    # and call tornado.options.parse_config_file(*some_config_path*).  After you
    # do that the options will wind up in tornado.options.options
    global user_locale
    # Default to using the shell's LANG variable as the locale
    try:
        default_locale = os.environ['LANG'].split('.')[0]
    except KeyError: # $LANG isn't set
        default_locale = "en_US"
    user_locale = locale.get(default_locale)
    # NOTE: The locale setting above is only for the --help messages.
    # Simplify the auth option help message
    auths = "none, api, google, ssl"
    if KerberosAuthHandler:
        auths += ", kerberos"
    if PAMAuthHandler:
        auths += ", pam"
    # Simplify the syslog_facility option help message
    facilities = list(FACILITIES.keys())
    facilities.sort()
    # Figure out the default origins
    default_origins = [
        'localhost',
        '127.0.0.1',
    ]
    # Used both http and https above to demonstrate that both are acceptable
    try:
        additional_origins = socket.gethostbyname_ex(socket.gethostname())
    except socket.gaierror:
        # Couldn't get any IPs from the hostname
        additional_origins = []
    for host in additional_origins:
        if isinstance(host, str):
            default_origins.append('%s' % host)
        else: # It's a list
            for _host in host:
                default_origins.append('%s' % _host)
    default_origins = ";".join(default_origins)
    config_default = os.path.join(GATEONE_DIR, "server.conf")
    # NOTE: --settings_dir deprecates --config
    settings_default = os.path.join(GATEONE_DIR, "settings")
    define("config",
        default=config_default,
        help=_("DEPRECATED.  Use --settings_dir."),
        type=basestring
    )
    define("settings_dir",
        default=settings_default,
        help=_(
            "Path to the settings directory.  Default: %s" % settings_default),
        type=basestring
    )
    define(
        "debug",
        default=False,
        help=_("Enable debugging features such as auto-restarting when files "
               "are modified.")
    )
    define("cookie_secret", # 45 chars is, "Good enough for me" (cookie joke =)
        default=None,
        help=_("Use the given 45-character string for cookie encryption."),
        type=basestring
    )
    define("command",
        default=None,
        help=_(
            "DEPRECATED: Use the 'commands' option in the terminal settings."),
        type=basestring
    )
    define("address",
        default="",
        help=_("Run on the given address.  Default is all addresses (IPv6 "
               "included).  Multiple address can be specified using a semicolon"
               " as a separator (e.g. '127.0.0.1;::1;10.1.1.100')."),
        type=basestring)
    define("port", default=443, help=_("Run on the given port."), type=int)
    define(
        "enable_unix_socket",
        default=False,
        help=_("Enable Unix socket support."),
        type=bool)
    define(
        "unix_socket_path",
        default="/tmp/gateone.sock",
        help=_("Path to the Unix socket (if --enable_unix_socket=True)."),
        type=basestring)
    # Please only use this if Gate One is running behind something with SSL:
    define(
        "disable_ssl",
        default=False,
        help=_("If enabled, Gate One will run without SSL (generally not a "
               "good idea).")
    )
    define(
        "certificate",
        default="certificate.pem",
        help=_("Path to the SSL certificate.  Will be auto-generated if none is"
               " provided."),
        type=basestring
    )
    define(
        "keyfile",
        default="keyfile.pem",
        help=_("Path to the SSL keyfile.  Will be auto-generated if none is"
               " provided."),
        type=basestring
    )
    define(
        "ca_certs",
        default=None,
        help=_("Path to a file containing any number of concatenated CA "
               "certificates in PEM format.  They will be used to authenticate "
               "clients if the 'ssl_auth' option is set to 'optional' or "
               "'required'."),
        type=basestring
    )
    define(
        "ssl_auth",
        default='none',
        help=_("Enable the use of client SSL (X.509) certificates as a "
               "secondary authentication factor (the configured 'auth' type "
               "will come after SSL auth).  May be one of 'none', 'optional', "
               "or 'required'.  NOTE: Only works if the 'ca_certs' option is "
               "configured."),
        type=basestring
    )
    define(
        "user_dir",
        default=os.path.join(GATEONE_DIR, "users"),
        help=_("Path to the location where user files will be stored."),
        type=basestring
    )
    define(
        "user_logs_max_age",
        default="30d",
        help=_("Maximum amount of length of time to keep any given user log "
                "before it is removed."),
        type=basestring
    )
    define(
        "session_dir",
        default="/tmp/gateone",
        help=_(
            "Path to the location where session information will be stored."),
        type=basestring
    )
    define(
        "syslog_facility",
        default="daemon",
        help=_("Syslog facility to use when logging to syslog (if "
               "syslog_session_logging is enabled).  Must be one of: %s."
               "  Default: daemon" % ", ".join(facilities)),
        type=basestring
    )
    define(
        "syslog_host",
        default=None,
        help=_("Remote host to send syslog messages to if syslog_logging is "
               "enabled.  Default: None (log to the local syslog daemon "
               "directly).  NOTE:  This setting is required on platforms that "
               "don't include Python's syslog module."),
        type=basestring
    )
    define(
        "session_timeout",
        default="5d",
        help=_("Amount of time that a session is allowed to idle before it is "
        "killed.  Accepts <num>X where X could be one of s, m, h, or d for "
        "seconds, minutes, hours, and days.  Default is '5d' (5 days)."),
        type=basestring
    )
    define(
        "new_api_key",
        default=False,
        help=_("Generate a new API key that an external application can use to "
               "embed Gate One."),
    )
    define(
        "auth",
        default="none",
        help=_("Authentication method to use.  Valid options are: %s" % auths),
        type=basestring
    )
    # This is to prevent replay attacks.  Gate One only keeps a "working memory"
    # of API auth objects for this amount of time.  So if the Gate One server is
    # restarted we don't have to write them to disk as anything older than this
    # setting will be invalid (no need to check if it has already been used).
    define(
        "api_timestamp_window",
        default="30s", # 30 seconds
        help=_(
            "How long before an API authentication object becomes invalid.  "
            "Default is '30s' (30 seconds)."),
        type=basestring
    )
    define(
        "sso_realm",
        default=None,
        help=_("Kerberos REALM (aka DOMAIN) to use when authenticating clients."
               " Only relevant if Kerberos authentication is enabled."),
        type=basestring
    )
    define(
        "sso_service",
        default='HTTP',
        help=_("Kerberos service (aka application) to use. Defaults to HTTP. "
               "Only relevant if Kerberos authentication is enabled."),
        type=basestring
    )
    define(
        "pam_realm",
        default=os.uname()[1],
        help=_("Basic auth REALM to display when authenticating clients.  "
        "Default: hostname.  "
        "Only relevant if PAM authentication is enabled."),
        # NOTE: This is only used to show the user a REALM at the basic auth
        #       prompt and as the name in the GATEONE_DIR+'/users' directory
        type=basestring
    )
    define(
        "pam_service",
        default='login',
        help=_("PAM service to use.  Defaults to 'login'. "
               "Only relevant if PAM authentication is enabled."),
        type=basestring
    )
    define(
        "embedded",
        default=False,
        help=_("Doesn't do anything (yet).")
    )
    define(
        "locale",
        default=default_locale,
        help=_("The locale (e.g. pt_PT) Gate One should use for translations."
             "  If not provided, will default to $LANG (which is '%s' in your "
             "current shell), or en_US if not set."
             % os.environ.get('LANG', 'not set').split('.')[0]),
        type=basestring
    )
    define("js_init",
        default="",
        help=_("A JavaScript object (string) that will be used when running "
               "GateOne.init() inside index.html.  "
               "Example: --js_init=\"{scheme: 'white'}\" would result in "
               "GateOne.init({scheme: 'white'})"),
        type=basestring
    )
    define(
        "https_redirect",
        default=False,
        help=_("If enabled, a separate listener will be started on port 80 that"
               " redirects users to the configured port using HTTPS.")
    )
    define(
        "url_prefix",
        default="/",
        help=_("An optional prefix to place before all Gate One URLs. e.g. "
               "'/gateone/'.  Use this if Gate One will be running behind a "
               "reverse proxy where you want it to be located at some sub-"
               "URL path."),
        type=basestring
    )
    define(
        "origins",
        default=default_origins,
        help=_("A semicolon-separated list of origins you wish to allow access "
               "to your Gate One server over the WebSocket.  This value must "
               "contain the hostnames and FQDNs (e.g. foo;foo.bar;) users will"
               " use to connect to your Gate One server as well as the "
               "hostnames/FQDNs of any sites that will be embedding Gate One. "
               "Here's the default on your system: '%s'. "
               "Alternatively, '*' may be  specified to allow access from "
               "anywhere." % default_origins),
        type=basestring
    )
    define(
        "pid_file",
        default="/tmp/gateone.pid",
        help=_(
            "Define the path to the pid file.  Default: /tmp/gateone.pid"),
        type=basestring
    )
    define(
        "uid",
        default=str(os.getuid()),
        help=_(
            "Drop privileges and run Gate One as this user/uid."),
        type=basestring
    )
    define(
        "gid",
        default=str(os.getgid()),
        help=_(
            "Drop privileges and run Gate One as this group/gid."),
        type=basestring
    )
    define(
        "api_keys",
        default="",
        help=_("The 'key:secret,...' API key pairs you wish to use (only "
               "applies if using API authentication)"),
        type=basestring
    )
    define(
        "combine_js",
        default="",
        help=_(
            "Combines all of Gate One's JavaScript files into one big file and "
            "saves it at the given path (e.g. ./gateone.py "
            "--combine_js=/tmp/gateone.js)"),
        type=basestring
    )

def main():
    global _
    global PLUGINS
    global APPLICATIONS
    define_options()
    # Before we do anything else we need the get the settings_dir argument (if
    # given) so we can make sure we're handling things accordingly.
    settings_dir = os.path.join(GATEONE_DIR, 'settings')
    for arg in sys.argv:
        if arg.startswith('--settings_dir'):
            settings_dir = arg.split('=', 1)[1]
    if not os.path.exists(settings_dir):
        # Try to create it
        try:
            mkdir_p(settings_dir)
        except:
            logging.error(_(
               "Could not find/create settings directory at %s" % settings_dir))
            sys.exit(1)
    all_settings = get_settings(settings_dir)
    enabled_plugins = []
    enabled_applications = []
    if 'gateone' in all_settings:
        # The check above will fail in first-run situations
        enabled_plugins = all_settings['*']['gateone'].get(
            'enabled_plugins', [])
        enabled_applications = all_settings['*']['gateone'].get(
            'enabled_applications', [])
    PLUGINS = get_plugins(os.path.join(GATEONE_DIR, 'plugins'), enabled_plugins)
    imported = load_modules(PLUGINS['py'])
    for plugin in imported:
        try:
            PLUGIN_HOOKS.update({plugin.__name__: plugin.hooks})
        except AttributeError:
            pass # No hooks--probably just a supporting .py file.
    APPLICATIONS = get_applications(
        os.path.join(GATEONE_DIR, 'applications'), enabled_applications)
    app_modules = load_modules(APPLICATIONS)
    # Having parse_command_line() after loading applications in case an
    # application has additional calls to define().
    tornado.options.parse_command_line()
    APPLICATIONS = [] # Replace it with a list of actual class instances
    web_handlers = []
    for module in app_modules:
        module.SESSIONS = SESSIONS
        try:
            APPLICATIONS.extend(module.apps)
            if hasattr(module, 'init'):
                module.init(all_settings)
            if hasattr(module, 'web_handlers'):
                web_handlers.extend(module.web_handlers)
        except AttributeError:
            pass # No apps--probably just a supporting .py file.
    logging.debug(_("Imported applications: %s" % APPLICATIONS))
    authentication_options = [
        # These are here only for logical separation in the .conf files
        'api_timestamp_window', 'auth', 'pam_realm', 'pam_service',
        'sso_realm', 'sso_service'
    ]
    terminal_options = [ # These are now terminal-app-specific setttings
        'command', 'dtach', 'session_logging', 'session_logs_max_age',
        'syslog_session_logging'
    ]
    non_options = [
        # These are things that don't really belong in settings
        'new_api_key', 'help', 'kill', 'config'
    ]
    # Convert the old server.conf to the new settings file format and save it
    # as a number of distinct .conf files to keep things better organized.
    # NOTE: This logic will go away some day as it only applies when moving from
    #       Gate One 1.1 (or older) to newer versions.
    if os.path.exists(options.config):
        from utils import settings_template, RUDict
        settings = RUDict()
        auth_settings = RUDict()
        terminal_settings = RUDict()
        api_keys = RUDict({"*": {"gateone": {"api_keys": {}}}})
        with open(options.config) as f:
            # Regular server-wide settings will go in 10server.conf by default.
            # These settings can actually be spread out into any number of .conf
            # files in the settings directory using whatever naming convention
            # you want.
            settings_path = os.path.join(GATEONE_DIR, 'settings')
            server_conf_path = os.path.join(settings_path, '10server.conf')
            # Using 20authentication.conf for authentication settings
            auth_conf_path = os.path.join(
                settings_path, '20authentication.conf')
            terminal_conf_path = os.path.join(settings_path, '50terminal.conf')
            api_keys_conf = os.path.join(settings_path, '20api_keys.conf')
            # NOTE: Using a separate file for authentication stuff for no other
            #       reason than it seems like a good idea.  Don't want one
            #       gigantic config file for everything (by default, anyway).
            logging.info(_(
                "Old server.conf file found.  Converting to the new format as "
                "%s, %s, and %s" % (
                    server_conf_path, auth_conf_path, terminal_conf_path)))
            for line in f:
                if line.startswith('#'):
                    continue
                key = line.split('=', 1)[0].strip()
                value = eval(line.split('=', 1)[1].strip())
                if key in terminal_options:
                    if key == 'command':
                        # Fix the path to ssh_connect.py if present
                        if 'ssh_connect.py' in value:
                            value = value.replace(
                                '/plugins/', '/applications/terminal/plugins/')
                    if key == 'session_logs_max_age':
                        # This is now user_logs_max_age.  Put it in 'gateone'
                        settings.update({'user_logs_max_age': value})
                    terminal_settings.update({key: value})
                elif key in authentication_options:
                    auth_settings.update({key: value})
                elif key == 'origins':
                    # Convert to the new format (a list with no http://)
                    origins = value.split(';')
                    converted_origins = []
                    for origin in origins:
                        # The new format doesn't bother with http:// or https://
                        origin = origin.split('://')[1]
                        if origin not in converted_origins:
                            converted_origins.append(origin)
                    settings.update({key: converted_origins})
                elif key == 'api_keys':
                    # Move these to the new location/format (20api_keys.conf)
                    for pair in value.split(','):
                        api_key, secret = pair.split(':')
                        if bytes == str:
                            api_key = api_key.decode('UTF-8')
                            secret = secret.decode('UTF-8')
                        api_keys['*']['gateone']['api_keys'].update(
                            {api_key: secret})
                    # API keys can be written right away
                    with open(api_keys_conf, 'w') as conf:
                        msg = _(
                            "// This file contains the key and secret pairs "
                            "used by Gate One's API authentication method.\n")
                        conf.write(msg)
                        conf.write(str(api_keys))
                else:
                    settings.update({key: value})
            template_path = os.path.join(
                GATEONE_DIR, 'templates', 'settings', '10server.conf')
            new_settings = settings_template(template_path, settings=settings)
            if not os.path.exists(server_conf_path):
                with open(server_conf_path, 'w') as s:
                    s.write(_("// This is Gate One's main settings file.\n"))
                    s.write(new_settings)
            new_auth_settings = settings_template(
                template_path, settings=auth_settings)
            if not os.path.exists(auth_conf_path):
                with open(auth_conf_path, 'w') as s:
                    s.write(_(
                       "// This is Gate One's authentication settings file.\n"))
                    s.write(new_auth_settings)
            # Terminal uses a slightly different template; it converts 'command'
            # to the new 'commands' format.
            template_path = os.path.join(
                GATEONE_DIR, 'templates', 'settings', '50terminal.conf')
            new_term_settings = settings_template(
                template_path, settings=terminal_settings)
            if not os.path.exists(terminal_conf_path):
                with open(terminal_conf_path, 'w') as s:
                    s.write(_(
                        "// This is Gate One's Terminal application settings "
                        "file.\n"))
                    s.write(new_term_settings)
        # Rename the old server.conf so this logic doesn't happen again
        os.rename(options.config, "%s.old" % options.config)
    all_settings = get_settings(settings_dir)
    if 'gateone' not in all_settings['*']:
        # User has yet to create a 10server.conf (or equivalent)
        all_settings['*']['gateone'] = {} # Will be filled out below
    # Double check that we have all the necessary settings
    go_settings = all_settings['*']['gateone']
    # If you want any missing config file entries re-generated just delete the
    # cookie_secret line...
    if 'cookie_secret' not in go_settings or not go_settings['cookie_secret']:
        # Generate a default 10server.conf with a random cookie secret
        # NOTE: This will also generate a new 10server.conf if it is missing.
        logging.info(_(
            "Gate One settings are incomplete.  A new settings/10server.conf"
            " will be generated."))
        from utils import options_to_settings
        auth_settings = {} # Auth stuff goes in 20authentication.conf
        all_setttings = options_to_settings(options)
        config_defaults = all_setttings['*']['gateone']
        # Don't need this in the actual settings file:
        del config_defaults['settings_dir']
        # Generate a new cookie_secret
        config_defaults['cookie_secret'] = generate_session_id()
        # Separate out the authentication settings
        for key, value in config_defaults.items():
            if key in authentication_options:
                auth_settings.update({key: value})
                del config_defaults[key]
        # Make sure we have a valid log_file_prefix
        if config_defaults['log_file_prefix'] == None:
            web_log_dir = os.path.join(GATEONE_DIR, 'logs')
            web_log_path = os.path.join(web_log_dir, 'webserver.log')
            config_defaults['log_file_prefix'] = web_log_path
        else:
            web_log_dir = os.path.split(config_defaults['log_file_prefix'])[0]
        if not os.path.exists(web_log_dir):
            # Make sure the directory exists
            mkdir_p(web_log_dir)
        if not os.path.exists(config_defaults['log_file_prefix']):
            # Make sure the file is present
            open(config_defaults['log_file_prefix'], 'w').write('')
        settings_path = os.path.join(GATEONE_DIR, 'settings')
        server_conf_path = os.path.join(settings_path, '10server.conf')
        auth_conf_path = os.path.join(settings_path, '20authentication.conf')
        template_path = os.path.join(
            GATEONE_DIR, 'templates', 'settings', '10server.conf')
        from utils import settings_template
        new_settings = settings_template(
            template_path, settings=config_defaults)
        template_path = os.path.join(
            GATEONE_DIR, 'templates', 'settings', '10server.conf')
        with open(server_conf_path, 'w') as s:
            s.write(_("// This is Gate One's main settings file.\n"))
            s.write(new_settings)
        new_auth_settings = settings_template(
            template_path, settings=auth_settings)
        with open(auth_conf_path, 'w') as s:
            s.write(_("// This is Gate One's authentication settings file.\n"))
            s.write(new_auth_settings)
        # Make sure these values get updated
        all_settings = get_settings(options.settings_dir)
        go_settings = all_settings['*']['gateone']
    # Figure out which options are being overridden on the command line
    arguments = []
    for arg in list(sys.argv)[1:]:
        if not arg.startswith('-'):
            break
        else:
            arguments.append(arg.lstrip('-').split('=', 1)[0])
    for argument in arguments:
        if argument in non_options:
            continue
        elif argument in options.keys():
            go_settings[argument] = options[argument].value()
    # Update Tornado's options from our settings
    options['cookie_secret'].set(go_settings['cookie_secret'])
    options['logging'].set(str(go_settings['logging']))
    options['log_file_prefix'].set(str(go_settings['log_file_prefix']))
    # Change the uid/gid strings into integers
    try:
        uid = int(go_settings['uid'])
    except ValueError:
        import pwd
        # Assume it's a username and grab its uid
        uid = pwd.getpwnam(go_settings['uid']).pw_uid
    try:
        gid = int(go_settings['gid'])
    except ValueError:
        import grp
        # Assume it's a group name and grab its gid
        gid = grp.getgrnam(go_settings['gid']).gr_gid
    if not os.path.exists(go_settings['user_dir']): # Make our user_dir
        try:
            mkdir_p(go_settings['user_dir'])
        except OSError:
            import pwd
            logging.error(_(
                "Error: Gate One could not create %s.  Please ensure that user,"
                " %s has permission to create this directory or create it "
                "yourself and make user, %s its owner." % (go_settings['user_dir'],
                repr(pwd.getpwuid(os.geteuid())[0]),
                repr(pwd.getpwuid(os.geteuid())[0]))))
            sys.exit(1)
        # If we could create it we should be able to adjust its permissions:
        os.chmod(go_settings['user_dir'], 0o770)
    if not check_write_permissions(uid, go_settings['user_dir']):
        # Try correcting this first
        try:
            recursive_chown(go_settings['user_dir'], uid, gid)
        except (ChownError, OSError) as e:
            logging.error("user_dir: %s, uid: %s, gid: %s" % (
                go_settings['user_dir'], uid, gid))
            logging.error(e)
            sys.exit(1)
    if not os.path.exists(go_settings['session_dir']): # Make our session_dir
        try:
            mkdir_p(go_settings['session_dir'])
        except OSError:
            logging.error(_(
                "Error: Gate One could not create %s.  Please ensure that user,"
                " %s has permission to create this directory or create it "
                "yourself and make user, %s its owner." % (
                go_settings['session_dir'],
                repr(pwd.getpwuid(os.geteuid())[0]),
                repr(pwd.getpwuid(os.geteuid())[0]))))
            sys.exit(1)
        os.chmod(go_settings['session_dir'], 0o770)
    if not check_write_permissions(uid, go_settings['session_dir']):
        # Try correcting it
        try:
            recursive_chown(go_settings['session_dir'], uid, gid)
        except (ChownError, OSError) as e:
            logging.error("session_dir: %s, uid: %s, gid: %s" % (
                go_settings['session_dir'], uid, gid))
            logging.error(e)
            sys.exit(1)
    # Re-do the locale in case the user supplied something as --locale
    user_locale = locale.get(go_settings['locale'])
    _ = user_locale.translate # Also replaces our wrapper so no more .encode()
    # Create the log dir if not already present (NOTE: Assumes we're root)
    log_dir = os.path.split(go_settings['log_file_prefix'])[0]
    if not os.path.exists(log_dir):
        try:
            mkdir_p(log_dir)
        except OSError:
            logging.error(_("\x1b[1;31mERROR:\x1b[0m Could not create %s for "
                "log_file_prefix: %s" % (log_dir, go_settings['log_file_prefix']
            )))
            logging.error(_("You probably want to change this option, run Gate "
                  "One as root, or create that directory and give the proper "
                  "user ownership of it."))
            sys.exit(1)
    if not check_write_permissions(uid, log_dir):
        # Try to correct it
        try:
            recursive_chown(log_dir, uid, gid)
        except (ChownError, OSError) as e:
            logging.error("log_dir: %s, uid: %s, gid: %s" % (log_dir, uid, gid))
            logging.error(e)
            sys.exit(1)
    if options.new_api_key:
        # Generate a new API key for an application to use and save it to
        # settings/20api_keys.conf.
        from utils import RUDict
        api_key = generate_session_id()
        # Generate a new secret
        secret = generate_session_id()
        api_keys_conf = os.path.join(GATEONE_DIR, 'settings', '20api_keys.conf')
        new_keys = {api_key: secret}
        api_keys = RUDict({"*": {"gateone": {"api_keys": {}}}})
        if os.path.exists(api_keys_conf):
            api_keys = get_settings(api_keys_conf)
        api_keys.update({"*": {"gateone": {"api_keys": new_keys}}})
        with open(api_keys_conf, 'w') as conf:
            msg = _(
                "// This file contains the key and secret pairs used by Gate "
                "One's API authentication method.\n")
            conf.write(msg)
            conf.write(str(api_keys))
        logging.info(_("A new API key has been generated: %s" % api_key))
        logging.info(_("This key can now be used to embed Gate One into other "
                "applications."))
        sys.exit(0)
    if options.combine_js:
        # Combine all JavaScript files into one big one.
        plugins_dir = os.path.join(GATEONE_DIR, 'plugins')
        pluginslist = os.listdir(plugins_dir)
        pluginslist.sort()
        applications_dir = os.path.join(GATEONE_DIR, 'applications')
        appslist = os.listdir(applications_dir)
        appslist.sort()
        with open(options.combine_js, 'w') as f:
            # Start by adding gateone.js
            gateone_js = os.path.join(GATEONE_DIR, 'static', 'gateone.js')
            with open(gateone_js) as go_js:
                f.write(go_js.read() + '\n')
            # Gate One plugins
            for plugin in pluginslist:
                if enabled_plugins and plugin not in enabled_plugins:
                    continue
                static_dir = os.path.join(plugins_dir, plugin, 'static')
                if os.path.isdir(static_dir):
                    filelist = os.listdir(static_dir)
                    filelist.sort()
                    for filename in filelist:
                        filepath = os.path.join(static_dir, filename)
                        if filename.endswith('.js'):
                            with open(filepath) as js_file:
                                f.write(js_file.read() + '\n')
            # Gate One applications
            for application in appslist:
                if enabled_applications:
                    # Only export JS of enabled apps
                    if application not in enabled_applications:
                        continue
                static_dir = os.path.join(plugins_dir, application, 'static')
                plugins_dir = os.path.join(
                    applications_dir, application, 'plugins')
                if os.path.isdir(static_dir):
                    filelist = os.listdir(static_dir)
                    filelist.sort()
                    for filename in filelist:
                        filepath = os.path.join(static_dir, filename)
                        if filename.endswith('.js'):
                            with open(filepath) as js_file:
                                f.write(js_file.read() + '\n')
                app_settings = all_settings['*'].get(application, None)
                enabled_app_plugins = []
                if app_settings:
                    enabled_app_plugins = app_settings.get(
                        'enabled_plugins', [])
                if os.path.isdir(plugins_dir):
                    pluginslist = os.listdir(plugins_dir)
                    pluginslist.sort()
                    # Gate One application plugins
                    for plugin in pluginslist:
                        # Only export JS of enabled app plugins
                        if enabled_app_plugins:
                            if plugin not in enabled_app_plugins:
                                continue
                        static_dir = os.path.join(plugins_dir, plugin, 'static')
                        if os.path.isdir(static_dir):
                            filelist = os.listdir(static_dir)
                            filelist.sort()
                            for filename in filelist:
                                filepath = os.path.join(static_dir, filename)
                                if filename.endswith('.js'):
                                    with open(filepath) as js_file:
                                        f.write(js_file.read() + '\n')
            f.flush()
        sys.exit(0)
    # Display the version in case someone sends in a log for for support
    logging.info(_("Gate One %s" % __version__))
    logging.info(_("Tornado version %s" % tornado_version))
    # Set our global session timeout
    global TIMEOUT
    TIMEOUT = convert_to_timedelta(go_settings['session_timeout'])
    # Turn any API keys provided on the command line into a dict
    api_keys = {}
    if 'api_keys' in arguments:
        if options.api_keys:
            for pair in options.api_keys.value().split(','):
                api_key, secret = pair.split(':')
                if bytes == str:
                    api_key = api_key.decode('UTF-8')
                    secret = secret.decode('UTF-8')
                api_keys.update({api_key: secret})
        go_settings['api_keys'] = api_keys
    # Fix the url_prefix if the user forgot the trailing slash
    if not go_settings['url_prefix'].endswith('/'):
        go_settings['url_prefix'] += '/'
    # Convert the origins into a list if overridden via the command line
    if 'origins' in arguments:
        if ';' in options.origins:
            origins = options.origins.value().lower().split(';')
            real_origins = []
            for origin in origins:
                if '://' in origin:
                    origin = origin.split('://')[1]
                if origin not in real_origins:
                    real_origins.append(origin)
            go_settings['origins'] = real_origins
    logging.info("Connections to this server will be allowed from the following"
                 " origins: '%s'" % " ".join(go_settings['origins']))
    # Normalize settings
    api_timestamp_window = convert_to_timedelta(
        go_settings['api_timestamp_window'])
    go_settings['auth'] = none_fix(go_settings['auth'])
    go_settings['settings_dir'] = settings_dir
    # Check to make sure we have a certificate and keyfile and generate fresh
    # ones if not.
    if go_settings['keyfile'] == "keyfile.pem":
        # If set to the default we'll assume they want to use the one in the
        # gateone_dir
        go_settings['keyfile'] = "%s/keyfile.pem" % GATEONE_DIR
    if go_settings['certificate'] == "certificate.pem":
        # Just like the keyfile, assume they want to use the one in the
        # gateone_dir
        go_settings['certificate'] = "%s/certificate.pem" % GATEONE_DIR
    if not go_settings['disable_ssl']:
        if not os.path.exists(go_settings['keyfile']):
            logging.info(_("No SSL private key found.  One will be generated."))
            gen_self_signed_ssl(path=GATEONE_DIR)
        if not os.path.exists(go_settings['certificate']):
            logging.info(_("No SSL certificate found.  One will be generated."))
            gen_self_signed_ssl(path=GATEONE_DIR)
    # When logging=="debug" it will display all user's keystrokes so make sure
    # we warn about this.
    if go_settings['logging'] == "debug":
        logging.warning(_(
            "Logging is set to DEBUG.  Be aware that this will record the "
            "keystrokes of all users.  Don't be evil!"))
    if go_settings['ssl_auth'].lower() == 'required':
        # Convert to an integer using the ssl module
        cert_reqs = ssl.CERT_REQUIRED
    elif go_settings['ssl_auth'].lower() == 'optional':
        cert_reqs = ssl.CERT_OPTIONAL
    else:
        cert_reqs = ssl.CERT_NONE
    # Instantiate our Tornado web server
    ssl_options = {
        "certfile": go_settings['certificate'],
        "keyfile": go_settings['keyfile'],
        "ca_certs": go_settings['ca_certs'],
        "cert_reqs": cert_reqs
    }
    if go_settings['disable_ssl']:
        proto = "http://"
        ssl_options = None
    else:
        proto = "https://"
    https_server = tornado.httpserver.HTTPServer(
        GateOneApp(settings=go_settings, web_handlers=web_handlers),
        ssl_options=ssl_options)
    https_redirect = tornado.web.Application(
        [(r".*", HTTPSRedirectHandler),],
        port=go_settings['port'],
        url_prefix=go_settings['url_prefix']
    )
    tornado.web.ErrorHandler = ErrorHandler
    if go_settings['auth'] == 'pam':
        if uid != 0 or os.getuid() != 0:
            logging.warning(_(
                "PAM authentication is configured but you are not running Gate"
                " One as root.  If the pam_service you've selected (%s) is "
                "configured to use pam_unix.so for 'auth' (i.e. authenticating "
                "against /etc/passwd and /etc/shadow) Gate One will not be able"
                " to authenticate all users.  It will only be able to "
                "authenticate the user that owns the gateone.py process." %
                go_settings['pam_service']))
    try: # Start your engines!
        if go_settings['enable_unix_socket']:
            https_server.add_socket(
                tornado.netutil.bind_unix_socket(
                    go_settings['unix_socket_path']))
            logging.info(_("Listening on Unix socket '{socketpath}'".format(
                socketpath=go_settings['unix_socket_path'])))
        address = none_fix(go_settings['address'])
        if address:
            for addr in address.split(';'):
                if addr: # Listen on all given addresses
                    if go_settings['https_redirect']:
                        if go_settings['disable_ssl']:
                            logging.error(_(
                            "You have https_redirect *and* disable_ssl enabled."
                            "  Please pick one or the other."))
                            sys.exit(1)
                        logging.info(_(
                            "http://{addr}:80/ will be redirected to...".format(
                                addr=addr)
                        ))
                        https_redirect.listen(port=80, address=addr)
                    logging.info(_(
                        "Listening on {proto}{address}:{port}/".format(
                            proto=proto, address=addr, port=go_settings['port'])
                    ))
                    https_server.listen(port=go_settings['port'], address=addr)
        elif address == '':
            # Listen on all addresses (including IPv6)
            if go_settings['https_redirect']:
                if go_settings['disable_ssl']:
                    logging.error(_(
                        "You have https_redirect *and* disable_ssl enabled."
                        "  Please pick one or the other."))
                    sys.exit(1)
                logging.info(_("http://*:80/ will be redirected to..."))
                https_redirect.listen(port=80, address="")
            logging.info(_(
                "Listening on {proto}*:{port}/".format(
                    proto=proto, port=go_settings['port'])))
            https_server.listen(port=go_settings['port'], address="")
        # NOTE:  To have Gate One *not* listen on a TCP/IP address you may set
        #        address=None
        write_pid(go_settings['pid_file'])
        pid = read_pid(go_settings['pid_file'])
        logging.info(_("Process running with pid " + pid))
        # Check to see what group owns /dev/pts and use that for supl_groups
        # First we have to make sure there's at least one pty present
        tempfd1, tempfd2 = pty.openpty()
        # Now check the owning group (doesn't matter which one so we use 0)
        tty_gid = os.stat('/dev/ptmx').st_gid
        # Close our temmporary pty/fds so we're not wasting them
        os.close(tempfd1)
        os.close(tempfd2)
        if uid != os.getuid():
            drop_privileges(uid, gid, [tty_gid])
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: # ctrl-c
        logging.info(_("Caught KeyboardInterrupt.  Killing sessions..."))
    finally:
        tornado.ioloop.IOLoop.instance().stop()
        remove_pid(go_settings['pid_file'])
        logging.info(_("pid file removed."))
        # TODO: Move this dtach stuff to app_terminal.py
        if not all_settings['*']['terminal']['dtach']:
            # If we're not using dtach play it safe by cleaning up any leftover
            # processes.  When passwords are used with the ssh_conenct.py script
            # it runs os.setsid() on the child process which means it won't die
            # when Gate One is closed.  This is primarily to handle that
            # specific situation.
            killall(go_settings['session_dir'], go_settings['pid_file'])
            # Cleanup the session_dir (it's supposed to only contain temp stuff)
            import shutil
            shutil.rmtree(go_settings['session_dir'], ignore_errors=True)

if __name__ == "__main__":
    main()
