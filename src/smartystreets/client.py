"""
Client module for connecting to and interacting with SmartyStreets API
"""

import httpx

from smartystreets.data import Address, AddressCollection
from smartystreets.decorators import validate_args, truncate_args
from smartystreets.exceptions import SmartyStreetsError, ERROR_CODES


class Client:
    """
    Client class for interacting with the SmartyStreets API
    """

    BASE_URL = "https://api.smartystreets.com/"

    def __init__(
        self,
        auth_id,
        auth_token,
        standardize=False,
        invalid=False,
        logging=True,
        accept_keypair=False,
        truncate_addresses=False,
        timeout=None,
    ):
        """
        Constructs the client

        :param auth_id: authentication ID from SmartyStreets
        :param auth_token: authentication token
        :param standardize: boolean include addresses that match zip+4 in addition to DPV confirmed
                addresses
        :param invalid: boolean to include address candidates that may not be deliverable
        :param logging: boolean to allow SmartyStreets to log requests
        :param accept_keypair: boolean to toggle default keypair behavior
        :param truncate_addresses: boolean to silently truncate address lists in excess of the
                SmartyStreets maximum rather than raise an error.
        :param timeout: optional timeout value in seconds for requests.
        :return: the configured client object
        """
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.standardize = standardize
        self.invalid = invalid
        self.logging = logging
        self.accept_keypair = accept_keypair
        self.truncate_addresses = truncate_addresses
        self.timeout = timeout
        self.session = httpx.Client(base_url=self.BASE_URL)
        # self.session.mount(self.BASE_URL, requests.adapters.HTTPAdapter(max_retries=5))

    def post(self, endpoint, data):
        """
        Executes the HTTP POST request

        :param endpoint: string indicating the URL component to call
        :param data: the data to submit
        :return: the dumped JSON response content
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-standardize-only": "true" if self.standardize else "false",
            "x-include-invalid": "true" if self.invalid else "false",
            "x-accept-keypair": "true" if self.accept_keypair else "false",
        }
        if not self.logging:
            headers["x-suppress-logging"] = "true"

        params = {"auth-id": self.auth_id, "auth-token": self.auth_token}
        url = self.BASE_URL + endpoint
        response = self.session.post(
            url,
            json=data,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            return response.json()

        raise ERROR_CODES.get(response.status_code, SmartyStreetsError)

    @truncate_args
    @validate_args
    def street_addresses(self, addresses):
        """
        API method for verifying street address and geolocating

        Returns an AddressCollection always for consistency. In common usage it'd be simple and
        sane to return an Address when only one address was searched, however this makes
        populating search addresses from lists of unknown length problematic. If that list
        returns only one address now the code has to check the type of return value to ensure
        that it isn't applying behavior for an expected list type rather than a single dictionary.

        >>> client.street_addresses(["100 Main St, Anywhere, USA"], ["6 S Blvd, Richmond, VA"])
        >>> client.street_addresses([{"street": "100 Main St, anywhere USA"}, ... ])

        :param addresses: 1 or more addresses in string or dict format
        :return: an AddressCollection
        """

        # While it's okay in theory to accept freeform addresses they do need to be submitted in
        # a dictionary format.
        if not isinstance(addresses[0], dict):
            addresses = [{"street": arg for arg in addresses}]

        return AddressCollection(self.post("street-address", data=addresses))

    def street_address(self, address):
        """
        Geocode one and only address, get a single Address object back

        >>> client.street_address("100 Main St, Anywhere, USA")
        >>> client.street_address({"street": "100 Main St, anywhere USA"})

        :param address: string or dictionary with street address information
        :return: an Address object or None for no match
        """
        address = self.street_addresses([address])
        if not len(address):
            return None

        return Address(address[0])

    def zipcode(self, *args):
        raise NotImplementedError("You cannot lookup zipcodes yet")
