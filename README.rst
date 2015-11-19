A Bugzilla plugin for helga chat bot
====================================

.. image:: https://travis-ci.org/ktdreyer/helga-bugzilla.svg?branch=master
       :target: https://travis-ci.org/ktdreyer/helga-bugzilla

.. image:: https://badge.fury.io/py/helga-bugzilla.svg
       :target: https://badge.fury.io/py/helga-bugzilla

About
-----

Helga is a Python chat bot. Full documentation can be found at
http://helga.readthedocs.org.

This Bugzilla plugin allows Helga to respond to Bugzilla ticket numbers in IRC
and print information about the tickets. For example::

  03:14 < ktdreyer> bz 1217809
  03:14 < helgabot> ktdreyer might be talking about
                    https://bugzilla.redhat.com/show_bug.cgi?id=1217809
                    [[TRACKER] SELinux support]

Installation
------------
This Bugzilla plugin is `available from PyPI
<https://pypi.python.org/pypi/helga-bugzilla>`_, so you can simply install it
with ``pip``::

  pip install helga-bugzilla

If you want to hack on the helga-bugzilla source code, in your virtualenv where
you are running Helga, clone a copy of this repository from GitHub and run
``python setup.py develop``.

Configuration
-------------
In your ``settings.py`` file (or whatever you pass to ``helga --settings``),
you must specify a ``BUGZILLA_XMLRPC_URL``. For example::

  BUGZILLA_XMLRPC_URL = 'https://bugzilla.redhat.com/xmlrpc.cgi'

Optionally you can also specify a short URL format::

  BUGZILLA_TICKET_URL = "https://bugzilla.redhat.com/%(ticket)s"

The ``%(ticket)s`` format string will be replaced with the bug number.

Optional: Authenticated access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, Helga only reads tickets that are publicly accessible. You may
optionally give Helga privilieged access to Bugzilla and allow Helga to read
private bugs by setting up a python-bugzilla credential::

  $ bugzilla login
  (enter your username and password)

(Use the ``--bugzilla=https://bugzilla.example.com/xmlrpc.cgi`` argument here
if the XMLRPC URI is not the default, https://bugzilla.redhat.com/xmlrpc.cgi)

This ``bugzilla login`` command will save your login credential to
``.bugzillacookies`` or ``.bugzillatoken``. When this is set, Helga will be
able to read private bugs with using the permissions of the user to whom the
API key belongs.

**Note**: This authentication feature can expose private information (ticket
subjects) about your Bugzilla bugs. If you use this feature, be sure that the
networks to which Helga connects are restricted. Everyone in Helga's channels
will see the private information, so the assumption is that they already have
rights to read the private bugs.
