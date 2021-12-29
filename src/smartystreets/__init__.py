# -*- coding: utf-8 -*-

__author__ = "Ben Lopatin"
__email__ = "ben@benlopatin.com"
__version__ = "1.2.0"


from smartystreets.client import Client  # noqa
from smartystreets.async_client import AsyncClient  # noqa

__all__ = ["Client", "AsyncClient"]
