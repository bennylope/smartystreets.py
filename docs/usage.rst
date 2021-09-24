=====
Usage
=====

Client
======

SmartyStreets.py provides one client class, a synchronous `Client` class.

For typical use cases::

    from smartystreets import Client

You'll need to provide your `AUTH_ID` and `AUTH_TOKEN` to create a client instance::

    myclient = Client(auth_id='jkjdakjdkfjkaj', auth_token='kjakj1kjd')

You'll use either the `street_address` or `street_addresses` method depending on
*what kind of data you want back*. The first method takes only one address as an
argument, and returns either a single `Address` instance or `None`. The pluralized
`street_addresses` will take a list of 1 or more address inputs and return an
`AddressCollection` regardless of how many addresses are submitted or returned.

Verifying street addresses
==========================

To verify or geolocate a single address::

    >>> myclient.street_address({"street": "1600 pennsylvania ave",
            "city": "washington", "state": "dc"})

To verify or geolocate multiple addresses::

    >>> myclient.street_address([{"street": "1600 pennsylvania ave",
            "city": "washington", "state": "dc"}, {"street": "100 main st",
            "city": "peoria", "state": "IL"}])

.. note::
    The library here supports the one line street address format of address input
    described by the `Smarty Streets documentation <http://smartystreets.com/kb/faq/parse-and-verify-freeform-street-addresses>`_
    in the way described in that
    documentation, however the API does not seem to work as described in the
    Smarty Streets documentation. Addresses using only the 'street address' parameter
    result in 400 errors, regardless of how much information is in the street
    address string.
