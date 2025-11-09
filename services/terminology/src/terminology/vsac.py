"""
This module provides a class for interacting with the VSAC API.

It provides the following functionality:
- Retrieving a list of VSAC valuesets
- Retrieving a list of VSAC codes within a valueset

This module uses the FHIR Terminology Service for VSAC Resources.
More information can be found here:
https://www.nlm.nih.gov/vsac/support/usingvsac/vsacfhirapi.html

FHIR ValueSet spec:
https://www.hl7.org/fhir/valueset.html

"""
import os
import json
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
from fhir.resources.R4B.valueset import ValueSet
from fhir.resources.R4B.bundle import Bundle
from fhir.resources.R4B.domainresource import DomainResource




BASE_URL = "https://cts.nlm.nih.gov/fhir/"
TEST_BASE_URL = "https://uat-cts.nlm.nih.gov/fhir/"


class VSAC:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("VSAC_API_KEY", "")
        self.base_url = BASE_URL
        self.test_base_url = TEST_BASE_URL  
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })
        # Use HTTP Basic Auth with username 'apikey' and the API key as the password
        self.session.auth = HTTPBasicAuth("apikey", self.api_key)

        
    def get_valuesets(self) -> Bundle:
        response = self.make_request(f"{self.base_url}/ValueSet")
        return Bundle(**response.json())

    def get_valueset(self, valueset_id: str) -> ValueSet:
        response = self.make_request(f"{self.base_url}/ValueSet/{valueset_id}")
        return ValueSet(**response.json())

    def get_valueset_by_oid(self, oid: str) -> ValueSet:
        if oid.startswith("urn:oid:"):
            oid = oid[len("urn:oid:"):]
        response = self.make_request(f"{self.base_url}/ValueSet/{oid}")
        return ValueSet(**response.json())

    def get_codes(self, valueset_id):
        pass

    def make_request(self, url: str) -> requests.Response:
        """
        Make a REST call to the VSAC API and return the response.
        The response could be an OperationOutcome or a FHIR resource.
        If the response is an OperationOutcome, raise an exception and log the error.
        If the response is a FHIR resource, return the resource.
        """
        response = self.session.get(url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error making request to {url}: {response.status_code} {response.text}")


def extract_valuesets(Bundle):
    return [entry.resource for entry in Bundle.entry]


def main():
    vsac = VSAC()
    valueset_bundle = vsac.get_valuesets()
    entry = valueset_bundle.entry[0]
    valueset = entry.resource
    print(f"Name: {valueset.name}")
    print(f"Publisher: {valueset.publisher}")
    print(f"Title: {valueset.title}")
    print(f"Status: {valueset.status}")
    print(f"Experimental: {valueset.experimental}")
    total_found = valueset_bundle.total
    print(f"Total valuesets found: {total_found}")


if __name__ == "__main__":
    main()

