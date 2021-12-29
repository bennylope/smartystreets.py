#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import pytest
import httpx

from smartystreets.async_client import AsyncClient
from smartystreets import data
from smartystreets import exceptions


@pytest.fixture
def async_client():
    yield AsyncClient(auth_id="blah", auth_token="blibbidy")


@pytest.mark.asyncio
@pytest.mark.respx(base_url="https://api.smartystreets.com")
async def test_input_error(async_client, respx_mock):
    respx_mock.post("/street-address", data="").mock(return_value=httpx.Response(400))
    with pytest.raises(exceptions.SmartyStreetsInputError):
        await async_client.street_addresses([{}, {}])


@pytest.mark.asyncio
@pytest.mark.respx(base_url="https://api.smartystreets.com")
async def test_auth_error(async_client, respx_mock):
    respx_mock.post("/street-address", data="").mock(return_value=httpx.Response(401))
    with pytest.raises(exceptions.SmartyStreetsAuthError):
        await async_client.street_addresses([{}, {}])


@pytest.mark.asyncio
@pytest.mark.respx(base_url="https://api.smartystreets.com")
async def test_payment_error(async_client, respx_mock):
    respx_mock.post("/street-address", data="").mock(return_value=httpx.Response(402))
    with pytest.raises(exceptions.SmartyStreetsPaymentError):
        await async_client.street_addresses([{}, {}])


@pytest.mark.asyncio
@pytest.mark.respx(base_url="https://api.smartystreets.com")
async def test_server_error(async_client, respx_mock):
    respx_mock.post("/street-address", data="").mock(return_value=httpx.Response(500))
    with pytest.raises(exceptions.SmartyStreetsServerError):
        await async_client.street_addresses([{}, {}])


@pytest.mark.asyncio
@pytest.mark.respx(base_url="https://api.smartystreets.com")
async def test_one_address(async_client, respx_mock):
    """Ensure singluar street address method returns an Address"""
    respx_mock.post("/street-address", data="").mock(
        return_value=httpx.Response(200, json=[{"street_address": "100 Main St"}]),
    )
    response = await async_client.street_address({"street": "100 Main st"})
    assert isinstance(response, data.Address)


@pytest.mark.asyncio
async def test_addresses_response(async_client, respx_mock):
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
    response = await async_client.street_addresses(
        [{"street": "100 Main st"}, {"street": "200 Main St"}]
    )
    assert isinstance(response, data.AddressCollection)
    assert len(response) == 2
