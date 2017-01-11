"""
Data structures module for SmartyStreets API.

These structures simply wrap Python built in data structures that match the API's JSON responses,
including some convenience methods for simple access.
"""


class Address(dict):
    """
    Class for handling a single address response
    """

    @property
    def location(self):
        """
        Returns the geolocation as a lat/lng pair
        """
        try:
            lat, lng = self['metadata']['latitude'], self['metadata']['longitude']
        except KeyError:
            return None
        if not lat or not lng:
            return None
        return lat, lng

    @property
    def confirmed(self):
        """
        Returns a boolean whether this address is DPV confirmed
        The property does not specify *how* or what extent.
        """
        valid = ['Y', 'S', 'D']
        match_code = self.get('analysis', {}).get('dpv_match_code', '')
        return match_code in valid

    @property
    def id(self):
        """
        Returns the input id
        """
        try:
            return self['input_id']
        except KeyError:
            return None

    @property
    def index(self):
        """
        Returns the input_index
        """
        try:
            return self['input_index']
        except KeyError:
            return None

    @property
    def vacant_raw(self):
        """Returns dpv_vacant"""
        if self.has_key('analysis'):
            if self['analysis'].has_key('dpv_vacant'):
                return self['analysis']['dpv_vacant']
        return None

    @property
    def vacant(self):
        if self['analysis'].has_key('dpv_vacant'):
            return 1 if self['analysis']['dpv_vacant'] == 'Y' else 0
        return None

    @property
    def addressee(self):
        """Returns addressee"""
        if self.has_key('addressee'):
            return self['addressee']
        return None

    @property
    def delivery_line_1(self):
        if self.has_key('delivery_line_1'):
            return self['delivery_line_1']
        return None

    @property
    def delivery_line_2(self):
        if self.has_key('delivery_line_2'):
            return self['delivery_line_2']
        return None

    @property
    def last_line(self):
        if self.has_key('last_line'):
            return self['last_line']
        return None

    @property
    def footnotes(self):
        if self['analysis'].has_key('footnotes'):
            return self['analysis']['footnotes']
        return None

    @property
    def components_street_suffix(self):
        if self['components'].has_key('street_suffix'):
            return self['components']['street_suffix']
        return None

class AddressCollection(list):
    """
    Class for handling multiple responses.
    """
    id_lookup = {}  # For user supplied input_id
    index_lookup = {}  # For SmartyStreets input_index

    def __init__(self, results):
        """
        Constructor for an AddressCollection

        :param addresses: a list of dictionaries providing address information
        :return:
        """
        addresses = []
        for index, result in enumerate(results):
            address = Address(result)
            addresses.append(address)
            self.index_lookup[address.index] = index
            if address.id:
                self.id_lookup[address.id] = index
        super(AddressCollection, self).__init__(addresses)

    def get(self, key):
        """
        Returns an address by user controlled input ID

        :param key: an input_id used to tag a lookup address
        :return: a matching Address
        """
        try:
            return self[self.id_lookup.get(key)]
        except TypeError:
            raise KeyError

    def get_index(self, key):
        """
        Returns an address by input index, a value that matches the list index of the provided
        lookup value, not necessarily the result.

        :param key: an input_index matching the index of the provided address
        :return: a matching Address
        """
        try:
            return self[self.index_lookup.get(key)]
        except TypeError:
            raise KeyError
