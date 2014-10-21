=====
Usage
=====

To use SmartyStreets.py in a project::

    from smartystreets.client import Client

You'll need to provide your `AUTH_ID` and `AUTH_TOKEN` to create a client instance::

    myclient = Client(auth_id='jkjdakjdkfjkaj', auth_token='kjakj1kjd')

You'll use either the `street_address` or `street_addresses` method depending on
*what kind of data you want back*. The first method takes only one address as an
argument, and returns either a single `Address` instance or `None`. The pluralized
`street_addresses` will take a list of 1 or more address inputs and return an
`AddressCollection` regardless of how many addresses are submitted or returned.
