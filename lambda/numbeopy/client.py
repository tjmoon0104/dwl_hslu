"""
Base class sharing common properties and methods that can be reused for all endpoints.
The root url for all Numbeo API requests is https://www.numbeo.com/api/
"""

import os
import json
import requests
from iso3166 import countries
from requests.exceptions import ReadTimeout
from typing import Dict


class NumbeoClient:
    """
    Base API properties for all endpoints
    """

    def __init__(self, api_key: str = None):
        """
        :param api_key: api key from numbeo
        """
        self.url = "https://www.numbeo.com/api/"
        self.api_key = api_key

        if api_key is None:
            with open('apikey.json') as f:
                self.api_key = json.load(f)['api_key']

    def request(self, path: str, params: dict = None) -> dict:
        """
        API request method
        Args:
            path (str): API resource path
            params (dict): query parameters dictionary for passed-in path
        Returns:
            response (dict): parsed JSON response
        """
        if not params:
            params = dict()
        url = f"{self.url}/{path}"
        params['api_key'] = self.api_key
        response = requests.get(url=url, params=params)
        return response.json()

    def cities(self, country: str = None) -> dict:
        """
        Description: Returns cities in the database. Omits cities for which there are no data.

        :param country: Country name (as in numbeo database or ISO 3166 code)
        :return: json response
        """
        # country = countries.get(country)
        return self.request(path='cities', params={'country': country})

    def price_items(self) -> dict:
        """
        Description: Returns items in our main cost of living section

        :return: json response
        """
        return self.request(path='price_items')

    def currency_exchange_rates(self):
        """
        Description: Returns our current exchange rates we are using

        :return: json response
        """
        return self.request(path='currency_exchange_rates')

    def city_prices(self, query: str = None, city: str = None, country: str = None, city_id: str = None,
                    currency: str = None, use_estimated: str = None):
        """
        Description: Returns current prices in a city. Location can be specified with a query containing name or
        latitude,longitude (with comma separator).

        :return:
        """
        # if country:
        #     country = countries.get(country)
        return self.request(path='city_prices',
                            params={
                                'query': query,
                                'city': city,
                                'country': country,
                                'city_id': city_id,
                                'currency': currency,
                                'use_estimated': use_estimated
                            })

    def country_prices(self, country: str = None, currency: str = None):
        """
        Description: Returns current country prices

        :param country: country name
        :param currency: Currency you want the data to be estimated
        :return:
        """
        # if country:
        #     country = countries.get(country)
        return self.request(path='country_prices', params={'country': country, 'currency': currency})

    def close_cities_with_prices(self, query: str = None, max_distance: int = None, min_contributors: int = None):
        """
        Description: Returns close cities for a given query (or coordinates) in our database.

        :param min_contributors:
        :param max_distance:
        :param query:
        :return:
        """
        return self.request(path='close_cities_with_prices',
                            params={'query': query, 'max_distance': max_distance, 'min_contributors': min_contributors})

    def historical_city_prices(self, query: str = None, city: str = None, country: str = None, city_id: str = None,
                               currency: str = None):
        """
        Description: Returns historical average prices (per year) in a city.
        Location can be specified with a query containing name or latitude,longitude (with comma separator).
        :param query:
        :param city:
        :param country:
        :param city_id:
        :param currency:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='historical_city_prices', params=params)

    def historical_country_prices(self, country: str = None, currency: str = None):
        """
        Description: Returns historical average prices (per year) in a country

        :param country:
        :param currency:
        :return:
        """
        # if country:
        #     country = countries.get(country)
        return self.request(path='historical_country_prices', params={'country': country, 'currency': currency})

    def historical_currency_exchange_rates(self, month: int, year: int):
        """
        Description: Returns our historical exchange rates we are using (at the beginning of the month)

        :param month:
        :param year:
        :return:
        """
        return self.request(path='historical_currency_exchange_rates', params={'month': month, 'year': year})

    def city_prices_raw(self, query: str = None, city: str = None, country: str = None, city_id: str = None,
                        since_internal_id: str = None):
        """
        Description: Raw recent data entries for a given city, specified by a query (location or lat,lng)
        or city and country.Some algorithms which detect spam are invoked every ten days.
        In between, some spam is not properly classified.
        So if you use this method, you should consider not to use the data from the last 10 days.

        :param query:
        :param city:
        :param country:
        :param city_id:
        :param since_internal_id:
        :return:
        """
        return self.request(path='city_prices_raw',
                            params={'query': query, 'city': city, 'country': country, 'city_id': city_id,
                                    'since_internal_id': since_internal_id})

    def city_prices_raw_deletion_log(self, since_log_id: int = None):
        """
        Description: Returns ids of entries in city_prices_raw which are retroactively classified as spam and deleted from that table.

        :param since_log_id:
        :return:
        """
        return self.request(path='city_prices_raw_deletion_log', params={'since_log_id': since_log_id})

    def city_prices_archive_raw(self, query: str = None, city: str = None, country: str = None, city_id: str = None,
                                currency: str = None):
        """
        Description: Raw archived data entries for a given city, specified by a query (location or lat,lng)
        or city and country. Our backend processes moves data periodically from the main table to the archive table
        and using this query you can access data from the archive table.

        :param query:
        :param city:
        :param country:
        :param city_id:
        :param currency:
        :return:
        """
        return self.request(path='city_prices_archive_raw',
                            params={'query': query, 'city': city, 'country': country, 'city_id': city_id,
                                    'currency': currency})

    def indices(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns Numbeo's indices for a city. Location can be specified with a query containing name or
        latitude,longitude (with comma separator).

        :param query:
        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='indices', params=params)

    def country_indices(self, country: str = None):
        """
        Description: Returns Numbeo's indices for a country. Location can be specified with a country name.

        :param country:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='country_indices', params=params)
        # return self.request(path='country_indices', params={'country': country})

    def city_crime(self, city: str = None, country: str = None, city_id: str = None):
        """

        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_crime', params=params)

    def city_crime_raw(self, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns raw inputs about crime perceptions in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_crime_raw', params=params)

    def city_healthcare(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_healthcare', params=params)

    def city_healthcare_raw(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param query:
        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_healthcare_raw', params=params)

    def city_pollution(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param query:
        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_pollution', params=params)

    def city_pollution_raw(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param query:
        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_pollution_raw', params=params)

    def city_traffic(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param query:
        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_traffic', params=params)

    def city_traffic_raw(self, query: str = None, city: str = None, country: str = None, city_id: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param query:
        :param city:
        :param country:
        :param city_id:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='city_traffic_raw', params=params)

    def country_crime(self, country: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param country:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='country_crime', params=params)

    def country_healthcare(self, country: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param country:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='country_healthcare', params=params)

    def country_pollution(self, country: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param country:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='country_pollution', params=params)

    def country_traffic(self, country: str = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param country:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='country_traffic', params=params)

    def rankings_by_city_current(self, section: int = None):
        """
        Description: Returns aggregate inputs about healthcare quality perception in a city. Location can be specified with a query containing name or latitude,longitude (with comma separator).

        :param section:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='rankings_by_city_current', params=params)

    def rankings_by_country_historical(self, section: int = None):
        """
        Description: Returns all historical rankings by country for a given section at the website (i.e. cost of living, property, crime).

        :param section:
        :return:
        """
        params = dict((k, v) for k, v in locals().items())
        return self.request(path='rankings_by_country_historical', params=params)
