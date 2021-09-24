#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import pytest
import responses

from smartystreets.client import Client, validate_args, truncate_args, stringify
from smartystreets.data import Address, AddressCollection
from smartystreets.exceptions import (SmartyStreetsInputError, SmartyStreetsAuthError,
                                      SmartyStreetsPaymentError, SmartyStreetsServerError)

@pytest.fixture
def smarty_client():
    yield Client(auth_id='blah', auth_token='blibbidy')


class TestDecorators:
    """
    The decorator functions provide some safety around the parameters provided to API calls
    """

    def test_truncate_args(self, mocker):

        selfarg = mocker.MagicMock()
        myargs = [i for i in range(104)]

        def somefunc(myself, args):
            return len(args)

        selfarg.truncate_addresses = True
        assert truncate_args(somefunc)(selfarg, myargs) == 100

        selfarg.truncate_addresses = False
        modified_func = truncate_args(somefunc)
        with pytest.raises(ValueError):
            modified_func(selfarg, myargs)

    def test_validate_args(self, mocker):

        def somefunc(myself, args):
            return len(args)

        selfarg = mocker.MagicMock()

        myargs = ["1", "2", "3"]
        assert validate_args(somefunc)(selfarg, myargs) == 3

        myargs = [1, 2, 3]
        modified_func = validate_args(somefunc)
        with pytest.raises(TypeError):
            modified_func(selfarg, myargs)

        myargs = [{}, "?"]
        modified_func = validate_args(somefunc)
        with pytest.raises(TypeError):
            modified_func(selfarg, myargs)


class TestClient:

    @responses.activate
    def test_input_error(self, smarty_client):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                  body='', status=400,
                  content_type='application/json')
        with pytest.raises(SmartyStreetsInputError):
            smarty_client.street_addresses([{}, {}])

    @responses.activate
    def test_auth_error(self, smarty_client):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=401,
                      content_type='application/json')
        with pytest.raises(SmartyStreetsAuthError):
            smarty_client.street_addresses([{}, {}])

    @responses.activate
    def test_payment_error(self, smarty_client):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=402,
                      content_type='application/json')
        with pytest.raises(SmartyStreetsPaymentError):
            smarty_client.street_addresses([{}, {}])

    @responses.activate
    def test_server_error(self, smarty_client):
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='', status=500,
                      content_type='application/json')
        with pytest.raises(SmartyStreetsServerError):
            smarty_client.street_addresses([{}, {}])

    @responses.activate
    def test_one_address(self, smarty_client):
        """Ensure singluar street address method returns an Address"""
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='[{"street_address": "100 Main St"}]',
                      status=200, content_type='application/json')
        response = smarty_client.street_address({"street": "100 Main st"})
        assert isinstance(response, Address)

    @responses.activate
    def test_addresses_response(self, smarty_client):
        """Ensure address return an AddressCollection"""
        responses.add(responses.POST, 'https://api.smartystreets.com/street-address',
                      body='[{"street_address": "100 Main St"}, {"street_address": "200 Main St"}]',
                      status=200, content_type='application/json')
        response = smarty_client.street_addresses([{"street": "100 Main st"},
                                                 {"street": "200 Main St"}])
        assert isinstance(response, AddressCollection)
        assert len(response) == 2


class TestDataValidation:
    """
    SmartyStreets expects JSON values as strings - test that all data is updated that way
    """

    def test_stringify(self):
        assert stringify([{"input_id": 123, "zipcode": 20120, "candidates": "9"}]) == [{"input_id": "123", "zipcode": "20120", "candidates": 9}]

    def test_padded_integer(self):
        assert  stringify([{"input_id": 123, "zipcode": 120, "candidates": "9"}]) == [{"input_id": "123", "zipcode": "00120", "candidates": 9}]
