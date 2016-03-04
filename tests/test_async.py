#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.

Note that for now async behavior is provided via grequests, which uses gevent, which
in packaged form is only supported on Python 2.7. As such this functionality is not
expected to work on Python 3 (for now) which means the tests here are skipped for
Python 3. This is a sad.
"""
import responses
import sys
import unittest
from mock import MagicMock

from smartystreets.data import Address, AddressCollection
from smartystreets.exceptions import (SmartyStreetsInputError, SmartyStreetsAuthError,
                                      SmartyStreetsPaymentError, SmartyStreetsServerError)

skip = False

try:
    import grequests
except ImportError:
    # We will skip these tests if we can't find grequests.  The sync. client
    # returns data in a slightly different format, so these tests fail if we
    # try to substiute the sync. for the async. client.
    skip = True
else:
    from smartystreets.async import AsyncClient


@unittest.skipIf(skip, "No grequests support found")
class TestAsyncClient(unittest.TestCase):

    def setUp(self):
        self.client = AsyncClient(auth_id='blah', auth_token='blibbidy')

    @responses.activate
    def test_input_error(self):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=400,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsInputError, self.client.street_addresses, [{}, {}])

    @responses.activate
    def test_auth_error(self):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=401,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsAuthError, self.client.street_addresses, [{}, {}])

    @responses.activate
    def test_payment_error(self):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=402,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsPaymentError, self.client.street_addresses, [{}, {}])

    @responses.activate
    def test_server_error(self):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=500,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsServerError, self.client.street_addresses, [{}, {}])

    @responses.activate
    def test_addresses_response(self):
        """Ensure address return an AddressCollection"""
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='[{"street_address": "100 Main St"}, {"street_address": "200 Main St"}]',
                      status=200, content_type='application/json')
        response = self.client.street_addresses([{"street": "100 Main st"},
                                                 {"street": "200 Main St"}])
        self.assertIsInstance(response[0], AddressCollection)
        self.assertEqual(2, len(response[0]))
