#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import unittest

from smartystreets.data import Address, AddressCollection


class TestAddress(unittest.TestCase):

    def test_empty(self):
        addr = Address([])
        self.assertIsNone(addr.location)

    def test_location(self):
        addr = Address({'metadata': {'latitude': 12, 'longitude': 13}})
        self.assertEqual(addr.location, (12, 13))

    def test_id(self):
        addr = Address({'input_id': 'test1'})
        self.assertEqual(addr.id, 'test1')

    def test_index(self):
        addr = Address({'input_id': 'test1', 'input_index': 4})
        self.assertEqual(addr.index, 4)


class TestCollection(unittest.TestCase):

    def test_get_by_id(self):
        """Ensure an address can be found by input_id"""
        collection = AddressCollection([
            {'input_index': 3, 'input_id': 'A'},
            {'input_index': 5, 'input_id': 'h'},
            {'input_index': 8, 'input_id': 'X'},
        ])
        self.assertEqual(collection.get('A').index, 3)
        self.assertEqual(collection.get('h').index, 5)
        self.assertEqual(collection.get('X').index, 8)

        self.assertRaises(KeyError, collection.get_index, 'kj')

    def test_get_by_index(self):
        """Ensure an address can be found by input index"""
        collection = AddressCollection([
            {'input_index': 3, 'input_id': 'A'},
            {'input_index': 5, 'input_id': 'h'},
            {'input_index': 8, 'input_id': 'X'},
        ])
        self.assertEqual(collection.get_index(3).id, 'A')
        self.assertEqual(collection.get_index(5).id, 'h')
        self.assertEqual(collection.get_index(8).id, 'X')

        self.assertRaises(KeyError, collection.get_index, 10)

    def test_get_by_list_index(self):
        """Normal list indexing is unaffected"""
        collection = AddressCollection([
            {'input_index': 0, 'input_id': 'A'},
            {'input_index': 1, 'input_id': 'h'},
            {'input_index': 2, 'input_id': 'X'},
        ])
        self.assertEqual(collection[0].id, 'A')
        self.assertEqual(collection[1].id, 'h')
        self.assertEqual(collection[2].id, 'X')


if __name__ == '__main__':
    unittest.main()
