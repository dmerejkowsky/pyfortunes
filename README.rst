PyFortunes
==========


An XML RPC Client/Server for a fortune database

By fortune I mean `this software
<http://en.wikipedia.org/wiki/Fortune_%28Unix%29>`_

WARNING: This is still mostly a work in progress. Please be careful...


Description
-----------

This software is useful when you want to manage your own
fortune database.

Basically, a fortune database is just a bunch of plain text files in a
directory
(e.g */usr/share/fortune/*)

Nothing prevents you from creating you own database. Just create a directory
(e.g *~/.fortune*), and put your fortunes in plain text files, separating each
fortune with `%` on a single line.

For instance, if you want to start a collection of fortunes about famous quotes
from movies, just create a file *~/.fortune/movies* looking like::

  Steve McCroskey: Looks like I picked the wrong week to quit sniffing glue.
    -- Airplane !
  %
  Ted Striker: Because of my mistake, six men didn't return from that raid.
  Elaine Dickinson: Seven. Lieutenant Zip died this morning.
      Airplane !

Requirements
------------

Python3 is the only dependency.

The fortune files must be encoded as **UTF-8**, the server responses
are also always encoded in **UTF-8**, regardless of the OS
settings.

Usage
-----

First, start the daemon:
* On unix
  * Edit /etc/pyfd.conf, and run /usr/bin/pyfd

* On windows
  * Edit c:\Python32\Lib\site-packages\pyfortunes\pyfd.conf
  * Run c:\Python32\Scripts\install_pyfd_service.bat as administrator

Now you can run::

  pyf-get
  (to get a fortune at random)

   pyf-add
  (to add a new fotune to the database)


Bugs
----

Probably many. Please use github bug tracker if you find one.

