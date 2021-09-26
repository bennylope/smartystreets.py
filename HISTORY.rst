.. :changelog:

History
-------

1.1.0 (2021-09-26)
------------------

* Replace requests with httpx for transport

1.0.0 (2021-09-24)
------------------

* BREAKING!!! Remove Python 2 support and remove grequests based AsyncClient
* SmartyStreets.py is now tested against Python 3.7, 3.8, and 3.9

0.4.0 (2016-03-25)
------------------

* Add optional timeout value for client (pmkane!)

0.3.0 (2016-03-10)
------------------

* Ensure keep-alive is used for client connections (pmkane!)
* Testing updates (pmkane!)

0.2.4 (2015-03-15)
------------------

* Adds strict JSON serialization to async client as well

0.2.3 (2015-03-15)
------------------

* Bugfix in logging suppression header

0.2.2 (2015-01-29)
------------------

* Adds strict JSON serialization to ensure all-but-specified fields are
  serialized into strings.

0.2.1 (2014-11-17)
------------------

* Bugfix in plain string address input handling

0.2.0 (2014-10-23)
------------------

* Added experimental async client

0.1.0 (2014-10-21)
------------------

* First release on PyPI.
