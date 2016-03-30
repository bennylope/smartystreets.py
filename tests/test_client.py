#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import responses
import unittest
from mock import MagicMock

from smartystreets.client import Client, validate_args, truncate_args, stringify
from smartystreets.data import Address, AddressCollection
from smartystreets.data import Zipcode, ZipcodeCollection
from smartystreets.exceptions import (SmartyStreetsInputError, SmartyStreetsAuthError,
                                      SmartyStreetsPaymentError, SmartyStreetsServerError)


class TestDecorators(unittest.TestCase):
    """
    The decorator functions provide some safety around the parameters provided to API calls
    """

    def test_truncate_args(self):

        selfarg = MagicMock()
        myargs = [i for i in range(104)]

        def somefunc(myself, args):
            return len(args)

        selfarg.truncate_addresses = True
        self.assertEqual(truncate_args(somefunc)(selfarg, myargs), 100)

        selfarg.truncate_addresses = False
        modified_func = truncate_args(somefunc)
        self.assertRaises(ValueError, modified_func, selfarg, myargs)

    def test_validate_args(self):

        def somefunc(myself, args):
            return len(args)

        selfarg = MagicMock()

        myargs = ["1", "2", "3"]
        self.assertEqual(validate_args(somefunc)(selfarg, myargs), 3)

        myargs = [1, 2, 3]
        modified_func = validate_args(somefunc)
        self.assertRaises(TypeError, modified_func, selfarg, myargs)

        myargs = [{}, "?"]
        modified_func = validate_args(somefunc)
        self.assertRaises(TypeError, modified_func, selfarg, myargs)


class TestStreetAddress(unittest.TestCase):

    def setUp(self):
        self.client = Client(auth_id='blah', auth_token='blibbidy')

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
    def test_one_address(self):
        """Ensure singluar street address method returns an Address"""
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='[{"street_address": "100 Main St"}]',
                      status=200, content_type='application/json')
        response = self.client.street_address({"street": "100 Main st"})
        self.assertIsInstance(response, Address)

    @responses.activate
    def test_addresses_response(self):
        """Ensure address return an AddressCollection"""
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='[{"street_address": "100 Main St"}, {"street_address": "200 Main St"}]',
                      status=200, content_type='application/json')
        response = self.client.street_addresses([{"street": "100 Main st"},
                                                 {"street": "200 Main St"}])
        self.assertIsInstance(response, AddressCollection)
        self.assertEqual(2, len(response))


class TestZipcode(unittest.TestCase):

    def setUp(self):
        self.client = Client(auth_id='blah', auth_token='blibbidy')

    @responses.activate
    def test_input_error(self):
        responses.add(responses.POST, 'https://us-zipcode.api.smartystreets.com/lookup',
                  body='', status=400,
                  content_type='application/json')
        self.assertRaises(SmartyStreetsInputError, self.client.zipcodes, [{}, {}])

    @responses.activate
    def test_auth_error(self):
        responses.add(responses.POST, 'https://us-zipcode.api.smartystreets.com/lookup',
                      body='', status=401,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsAuthError, self.client.zipcodes, [{}, {}])

    @responses.activate
    def test_payment_error(self):
        responses.add(responses.POST, 'https://us-zipcode.api.smartystreets.com/lookup',
                      body='', status=402,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsPaymentError, self.client.zipcodes, [{}, {}])

    @responses.activate
    def test_server_error(self):
        responses.add(responses.POST, 'https://us-zipcode.api.smartystreets.com/lookup',
                      body='', status=500,
                      content_type='application/json')
        self.assertRaises(SmartyStreetsServerError, self.client.zipcodes, [{}, {}])

    @responses.activate
    def test_one_zipcode(self):
        """Ensure singular zipcode method returns a Zipcode"""
        responses.add(responses.POST, 'https://us-zipcode.api.smartystreets.com/lookup',
                      body='[{"city_states": [{"mailable_city": true, "city": "New York", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "Empire State", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "Gpo", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "Greeley Square", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "Macys Finance", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "Manhattan", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "New York City", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "NY", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "NY City", "state": "New York", "state_abbreviation": "NY"}, {"mailable_city": false, "city": "Nyc", "state": "New York", "state_abbreviation": "NY"}], "input_index": 0, "zipcodes": [{"county_fips": "36061", "zipcode_type": "S", "county_name": "New York", "zipcode": "10001", "longitude": -73.98935, "precision": "Zip5", "default_city": "New York", "latitude": 40.74949}]}]',
                      status=200, content_type='application/json')
        response = self.client.zipcode({"zipcode": "10001"})
        self.assertIsInstance(response, Zipcode)

    @responses.activate
    def test_zipcodes_response(self):
        """Ensure zipcodes return a ZipcodeCollection"""
        responses.add(responses.POST, 'https://us-zipcode.api.smartystreets.com/lookup',
                      body='[{"zipcode": "10001"}, {"zipcode": "10002"}]',
                      status=200, content_type='application/json')
        response = self.client.zipcodes([{"zipcode": "10001"},
                                                 {"zipcode": "10002"}])
        self.assertIsInstance(response, ZipcodeCollection)
        self.assertEqual(2, len(response))


class TestDataValidation(unittest.TestCase):
    """
    SmartyStreets expects JSON values as strings - test that all data is
    updated that way
    """

    def test_stringify(self):
        self.assertEqual(
            stringify([{"input_id": 123, "zipcode": 20120, "candidates": "9"}]),
            [{"input_id": "123", "zipcode": "20120", "candidates": 9}],
        )

    def test_padded_integer(self):
        self.assertEqual(
            stringify([{"input_id": 123, "zipcode": 120, "candidates": "9"}]),
            [{"input_id": "123", "zipcode": "00120", "candidates": 9}],
        )
