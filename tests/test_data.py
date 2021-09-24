#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import pytest
from smartystreets.data import Address, AddressCollection


class TestAddress:
    def test_empty(self):
        addr = Address([])
        assert addr.location is None

    def test_location(self):
        addr = Address({"metadata": {"latitude": 12, "longitude": 13}})
        assert addr.location == (12, 13)

    def test_id(self):
        addr = Address({"input_id": "test1"})
        assert addr.id == "test1"

    def test_index(self):
        addr = Address({"input_id": "test1", "input_index": 4})
        assert addr.index == 4


class TestAddressCollection:
    def test_get_by_id(self):
        """Ensure an address can be found by input_id"""
        collection = AddressCollection(
            [
                {"input_index": 3, "input_id": "A"},
                {"input_index": 5, "input_id": "h"},
                {"input_index": 8, "input_id": "X"},
            ]
        )
        assert collection.get("A").index == 3
        assert collection.get("h").index == 5
        assert collection.get("X").index == 8

        with pytest.raises(KeyError):
            collection.get_index("kj")

    def test_get_by_index(self):
        """Ensure an address can be found by input index"""
        collection = AddressCollection(
            [
                {"input_index": 3, "input_id": "A"},
                {"input_index": 5, "input_id": "h"},
                {"input_index": 8, "input_id": "X"},
            ]
        )
        assert collection.get_index(3).id == "A"
        assert collection.get_index(5).id == "h"
        assert collection.get_index(8).id == "X"

        with pytest.raises(KeyError):
            collection.get_index(10)

    def test_get_by_list_index(self):
        """Normal list indexing is unaffected"""
        collection = AddressCollection(
            [
                {"input_index": 0, "input_id": "A"},
                {"input_index": 1, "input_id": "h"},
                {"input_index": 2, "input_id": "X"},
            ]
        )
        assert collection[0].id == "A"
        assert collection[1].id == "h"
        assert collection[2].id == "X"
