================
SmartyStreets.py
================

.. image:: https://badge.fury.io/py/smartystreets.py.svg
    :target: http://badge.fury.io/py/smartystreets.py

.. image:: https://github.com/bennylope/smartystreets.py/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/bennylope/smartystreets.py/actions

.. image:: https://pypip.in/d/smartystreets.py/badge.svg
        :target: https://pypi.python.org/pypi/smartystreets.py


A wrapper for the SmartyStreets address validation and geolocation API.

Other Python libraries exist but skip out on multiple address submission
and make opinionated decisions about how to transform the return data.

.. note::
    This project is not affiliated with the SmartyStreets service or company in any
    way.

* Free software: BSD license
* Documentation: https://smartystreetspy.readthedocs.org.

Features
========

SmartyStreets.py aims to provide a sane, tested, and feature complete wrapper
to the SmartyStreets LiveAddress API, including address lookup for validation
and geolocation, as well as zipcode lookup and validation.

Installation
============

SmartyStreets.py requires the `requests library
<http://docs.python-requests.org/en/latest/>`_ and will install it if it is
found missing. **Installed versions < 2.0 will be upgraded.**::

    pip install smartystreets.py

Basic usage
===========

API client
----------

Create a client instance with your key::

    from smartystreets import Client
    client = Client(AUTH_ID, AUTH_TOKEN)

Create a client instance with SmartyStreets configuration options::

    client = Client(AUTH_ID, AUTH_TOKEN, standardize=True, invalid=False,
                logging=False)

These options correspond to the `x-standardize-only`, `x-include-invalid`, and
`x-suppress-logging` headers for opening up results to standardized but not
necessarily deliverable addresses, including invalid delivery addresses, and
toggling SmartyStreets API logging, respectively.

Since the SmartyStreets API only permits up to 100 addresses to be looked up at
once the client will raise an exception if more than 100 are provided. You can
turn off this functionality using the `truncate_addresses` option, which will
silently truncate the list to the first 100 addresses::

    client = Client(AUTH_ID, AUTH_TOKEN, truncate_addresses=True)

Address lookup
--------------

Simple address lookup::

    client.street_address("100 Main St Richmond, VA")

Multiple simple street addresses::

    client.street_addresses(["100 Main St Richmond, VA", "100 Main St Richmond, VA"])

**Note that these are different function names.**

You can also use dictionaries including detailed data::

    client.street_address({
        'input_id': 'k1d8j',
        'street': '100 Main st',
        'city': 'Richmond',
        'state': 'VA',
        'candidates': 2,
    })

And multiple detailed lookups::

    client.street_addresses([
        {
            'input_id': 'k1d8j',
            'street': '100 Main st',
            'city': 'Richmond',
            'state': 'VA',
            'candidates': 2,
        }, {
            'input_id': 'z29ir',
            'street': '400 Main st',
            'city': 'Richmond',
            'state': 'VA',
            'candidates': 2,
        }
    ])

.. note::
    You cannot mix the simple street lookup style and the detailed dictionary
    lookup style in the same API call. This is a library restriction.

Return data
-----------

Just as important as a clean interface for working with the API is a helpful
way of working with the returned data.

Returned data is presented as either a single `SmartyAddress` or a
`SmartyAddresses` collection. Each is based on builtin types so that you always
have access to the underlying data exactly as it was returned, but with
added convenience methods.

Address geolocation
~~~~~~~~~~~~~~~~~~~

Where is it?::

    >>> address = client.street_address("100 Main St Richmond, VA")
    >>> address.location
    (37.5436,-77.4453)

Accuracy is subject to address inputs and available data.

Address verification
~~~~~~~~~~~~~~~~~~~~

Is this a deliverable address?::

    >>> address.confirmed
    True

The value here does not necessarily mean this is an exact mail address
(e.g. with apartment number). The SmartyStreets API will return a code
indicating the complete DPV status.

Multiple addresses: input ID lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can look up an address by the `input_id` parameter (provided you include
one in the request)::

    >>> addresses = client.street_address([{'input_id': '123', 'street': ...}])
    >>> addresses.get('123')
    {'input_id': '123', 'street': ... }

The `get` method is used because the `SmartyAddresses` object's default lookup
is against the list index.

Zipcode lookup
--------------

`TODO`

Response errors
---------------

The following documented response codes raise specific exceptions based on a
`SmaryStreetsError` class.

- 400 Bad input. Required fields missing from input or are malformed.
- 401 Unauthorized. Addressuthentication failure; invalid credentials.
- 402 Payment required. No Addressuthenticationctive subscription found.
- 500 Internal server error. General service foundailure; retry request.
