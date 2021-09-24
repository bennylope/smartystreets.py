# -*- coding: utf-8 -*-

"""
Tests for decorators

The decorator functions provide some safety around the parameters provided to API calls
"""
import pytest
from smartystreets.client import validate_args, truncate_args


def test_truncate_args(mocker):

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


def test_validate_args(mocker):
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
