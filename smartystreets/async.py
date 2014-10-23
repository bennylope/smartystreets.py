"""
Uses gevent to make concurrent requests.
"""

import grequests
import json
import logging

from .client import Client, validate_args
from .data import AddressCollection

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
        yield l[i:i+n]


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

    You are strongly recommended to use the input_id parameter as the input_index values will be
    all but worthless.
    """
    def post(self, endpoint, data, parallelism=5):
        """
        Executes most of the request.

        The parallelism parameter is useful to avoid swamping the API service with calls. Thus
        the entire set of requests won't be all made at once, but in chunked groups.

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
        url = self.BASE_URL + endpoint

        rs = (
            grequests.post(
                url=url,
                data=json.dumps(data_chunk),
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

        # If a request results in an exception this should be logged, but ignored unless *all*
        # responses result in an exception
        return addresses, status_codes

    @validate_args
    def street_addresses(self, addresses):
        """
        Provides a consistent API across client types

        :param addresses: a list of addresses in dictionary format
        :return: a tuple of an AddressCollection and a dictionary of the response codes and the
        """
        return self.post("street-address", addresses)

    def street_address(self, address):
        raise NotImplementedError(
            "The street_address method is not implemented for the AsyncClient")
