'''
CrunchBase is the free database of technology companies, people, and
investors that anyone can edit. This is a proxy for the Crunchbase API.
This is good for people looking for jobs in technology. Keep an eye
open for other data sources for different disciplines.

http://api.crunchbase.com/v/1/<namespace>/<permalink>.js?api_key=(your_acess_key)

crunchbase has the following namespaces:
    company
    person
    financial-organization
    product
    service-provider

With the company namespace, the permalink is generally a company name.

For the implementation we just need.
results['name']
results['offices']  # list of addresses.
results['crunchbase_url']
results['homepage_url']
results['overview']

An error looks like
{"error": "Sorry, we could not find the record you were looking for."}

'''

import os
import json
import urllib
import urllib2


class CrunchProxy():
    '''
    This class does the heavy lifting.
    '''
    def __init__(self):
        self.base_url = "http://api.crunchbase.com/v/1/"
        self.api_key = os.environ['CRUNCHBASE_KEY']

    def get_company_details(self, company):
        """
        This method returns dict based on json data from crunchbase.
        If the api is reporting an error, check for an error key.
        This method can throw an exception. Caller should handle it.
        """
        permalink = "company"
        url_request_co = (self.base_url + permalink + "/"
                          + urllib.quote_plus(company)
                          + ".js?api_key=" + self.api_key)
        results = json.loads(urllib2.urlopen(url_request_co).read())
        return results

    def generic_query(self, term):
        """
        Given a term, search through the crunchbase database. This returns a
        list of dictionaries. The 'namespace' key tells you if is a company,
        product, etc. This method can raise exceptions. Caller should handle
        that.
        """
        url_request_query = (self.base_url + "search.js?query="
                             + urllib.quote_plus(term)
                             + "&api_key=" + self.api_key)
        results = json.loads(urllib2.urlopen(url_request_query).read())
        return results['results']
