===================================
City, state, & zipcode verification
===================================

The city, state, and zipcode verification service works fittingly at the level
of zipcodes, cities, and states.

::

    from smartystreets import Client
    myclient = Client(auth_id='jkjdakjdkfjkaj', auth_token='kjakj1kjd')
    myclient.city_state_zip(
