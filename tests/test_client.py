#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import pytest
import httpx

from smartystreets.client import Client
from smartystreets import data
from smartystreets import exceptions


@pytest.fixture
def smarty_client():
    yield Client(auth_id="blah", auth_token="blibbidy")


class TestClient:
    @pytest.mark.respx(base_url="https://api.smartystreets.com")
    def test_input_error(self, smarty_client, respx_mock):
        respx_mock.post("/street-address", data="").mock(
            return_value=httpx.Response(400)
        )
        with pytest.raises(exceptions.SmartyStreetsInputError):
            smarty_client.street_addresses([{}, {}])

    @pytest.mark.respx(base_url="https://api.smartystreets.com")
    def test_auth_error(self, smarty_client, respx_mock):
        respx_mock.post("/street-address", data="").mock(
            return_value=httpx.Response(401)
        )
        with pytest.raises(exceptions.SmartyStreetsAuthError):
            smarty_client.street_addresses([{}, {}])

    @pytest.mark.respx(base_url="https://api.smartystreets.com")
    def test_payment_error(self, smarty_client, respx_mock):
        respx_mock.post("/street-address", data="").mock(
            return_value=httpx.Response(402)
        )
        with pytest.raises(exceptions.SmartyStreetsPaymentError):
            smarty_client.street_addresses([{}, {}])

    @pytest.mark.respx(base_url="https://api.smartystreets.com")
    def test_server_error(self, smarty_client, respx_mock):
        respx_mock.post("/street-address", data="").mock(
            return_value=httpx.Response(500)
        )
        with pytest.raises(exceptions.SmartyStreetsServerError):
            smarty_client.street_addresses([{}, {}])

    @pytest.mark.respx(base_url="https://api.smartystreets.com")
    def test_one_address(self, smarty_client, respx_mock):
        """Ensure singluar street address method returns an Address"""
        respx_mock.post("/street-address", data="").mock(
            return_value=httpx.Response(200, json=[{"street_address": "100 Main St"}]),
        )
        response = smarty_client.street_address({"street": "100 Main st"})
        assert isinstance(response, data.Address)

    def test_addresses_response(self, smarty_client, respx_mock):
        """Ensure address return an AddressCollection"""
        respx_mock.post("/street-address", data="").mock(
            return_value=httpx.Response(
                200,
                json=[
                    {"street_address": "100 Main St"},
                    {"street_address": "200 Main St"},
                ],
            )
        ),
        response = smarty_client.street_addresses(
            [{"street": "100 Main st"}, {"street": "200 Main St"}]
        )
        assert isinstance(response, data.AddressCollection)
        assert len(response) == 2
