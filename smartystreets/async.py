"""
Uses gevent to make concurrent requests.
"""

import grequests
import json
import logging

from .client import Client, validate_args, stringify
from .data import AddressCollection
from .exceptions import SmartyStreetsError, ERROR_CODES

try:
    # Python 2
    ranger = xrange
except NameError:
    # Python 3
    ranger = range


logger = logging.getLogger(__name__)


def chunker(l, n):
    """
    Generates n-sized chunks from the list l
    """
    for i in ranger(0, len(l), n):
        yield l[i:i + n]


def response_error(request, exception):
    """
    Handles a grequest connection error.

    Applies to a feature in non-packaged version of grequests.

    :param request:
    :param exception:
    """
    logger.error("Request exception: {}".format(exception))


class AsyncClient(Client):
    """
    A SmartyStreets client that supports concurrent requests.

    You are strongly recommended to use the input_id parameter as the
    input_index values will be all but worthless.
    """
    def post(self, url, data, parallelism=5):
        """
        Executes most of the request.

        The parallelism parameter is useful to avoid swamping the API service
        with calls. Thus the entire set of requests won't be all made at once,
        but in chunked groups.

        :param endpoint: string indicating the URL component to call
        :param data: the JSON ready data to submit (list of dictionaries of addresses)
        :param parallelism: number of simultaneous requests to make.
        :return: a tuple of an AddressCollection and a dictionary of the response codes and the
                count for each.
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-standardize-only': 'true' if self.standardize else 'false',
            'x-include-invalid': 'true' if self.invalid else 'false',
            'x-accept-keypair': 'true' if self.accept_keypair else 'false',
        }
        if not self.logging:
            headers['x-suppress-logging'] = 'false'

        params = {'auth-id': self.auth_id, 'auth-token': self.auth_token}

        rs = (
            grequests.post(
                url=url,
                data=json.dumps(stringify(data_chunk)),
                params=params,
                headers=headers,
            ) for data_chunk in chunker(data, 100)
        )

        responses = grequests.imap(rs, size=parallelism)
        status_codes = {}
        addresses = AddressCollection([])
        for response in responses:
            if response.status_code not in status_codes.keys():
                status_codes[response.status_code] = 1
            else:
                status_codes[response.status_code] += 1

            if response.status_code == 200:
                addresses[0:0] = AddressCollection(response.json())  # Fast list insertion

            # If an auth error is raised, it's safe to say that this is
            # going to affect every request, so raise the exception immediately..
            elif response.status_code == 401:
                raise ERROR_CODES[401]

        # The return value or exception is simple if it is consistent.
        if len(status_codes.keys()) == 1:
            if 200 in status_codes:
                return addresses, status_codes
            else:
                raise ERROR_CODES.get(status_codes.keys()[0], SmartyStreetsError)

        # For any other mix not really sure of the best way to handle it.
        # If it's a mix of 200 and error codes, then returning the resultant
        # addresses and status code dictionary seems pretty sensible. But if
        # it's a mix of all error codes (could be a mix of payment error,
        # input error, potentially server error) this will probably require
        # careful checking in the code using this interface.
        return addresses, status_codes

    @validate_args
    def street_addresses(self, addresses):
        """
        Provides a consistent API across client types

        :param addresses: a list of addresses in dictionary format
        :return: a tuple of an AddressCollection and a dictionary of the response codes and the
        """
        return self.post(self.STREET_ADDRESS_BASE_URL + "street-address", addresses)

    def street_address(self, address):
        raise NotImplementedError(
            "The street_address method is not implemented for the AsyncClient")
