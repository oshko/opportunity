
import os 
import json
import urllib2

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

class CrunchProxy():
    
    def __init__(self):
        self.base_url = "http://api.crunchbase.com/v/1/"
        self.api_key = os.environ['CRUNCHBASE_KEY']
    
    # This method returns dict based on json data from crunchbase. 
    # If the api is reporting an error, check for an error key.
    # This method can throw an exception. Caller show handle it. 
    def getCompanyDetails(self, aCompany):
        permalink = "company"
        url_request = self.base_url + permalink + "/" + aCompany + ".js?api_key=" + self.api_key
        results = json.loads(urllib2.urlopen(url_request).read())
        return results

