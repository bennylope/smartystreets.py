#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smartystreets
----------------------------------

Tests for `smartystreets` module.
"""

import unittest
from mock import MagicMock

from smartystreets.client import Client, validate_args, truncate_args


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


class TestClient(unittest.TestCase):

    def test_errors(self):
        """Error status codes should raise specific errors"""
        pass

    def test_one_address(self):
        """Ensure one searched address results in"""
        pass
