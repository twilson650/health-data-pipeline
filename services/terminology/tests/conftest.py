"""Shared pytest fixtures for terminology service tests."""
import json
from unittest.mock import Mock, patch
import pytest


@pytest.fixture
def mock_vsac_api():
    """Fixture to mock VSAC API calls to nih.gov."""
    def create_mock_response(valueset_data: dict):
        """Create a mock response object with the given JSON data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = valueset_data
        mock_response.text = json.dumps(valueset_data)
        return mock_response
    
    def mock_get(url, **kwargs):
        """Mock function for session.get that returns appropriate FHIR responses."""
        # Handle Bundle endpoint (get_valuesets)
        if url.endswith("/ValueSet") or url.endswith("/ValueSet/"):
            # Create a FHIR Bundle response with ValueSet entries
            bundle_data = {
                "resourceType": "Bundle",
                "type": "searchset",
                "total": 2,
                "entry": [
                    {
                        "resource": {
                            "resourceType": "ValueSet",
                            "id": "test-valueset-1",
                            "url": "http://cts.nlm.nih.gov/fhir/ValueSet/test-valueset-1",
                            "name": "Test ValueSet 1",
                            "title": "Test ValueSet 1",
                            "status": "active"
                        }
                    },
                    {
                        "resource": {
                            "resourceType": "ValueSet",
                            "id": "test-valueset-2",
                            "url": "http://cts.nlm.nih.gov/fhir/ValueSet/test-valueset-2",
                            "name": "Test ValueSet 2",
                            "title": "Test ValueSet 2",
                            "status": "active"
                        }
                    }
                ]
            }
            return create_mock_response(bundle_data)
        
        # Handle single ValueSet endpoint (get_valueset_by_oid)
        # Extract OID from URL
        oid = url.split("/ValueSet/")[-1] if "/ValueSet/" in url else None
        
        # Create a minimal FHIR ValueSet response
        valueset_data = {
            "resourceType": "ValueSet",
            "id": oid or "test-valueset",
            "url": f"http://cts.nlm.nih.gov/fhir/ValueSet/{oid or 'test-valueset'}",
            "name": "Test ValueSet",
            "title": "Test ValueSet",
            "status": "active",
            "experimental": False,
            "publisher": "Test Publisher",
            "compose": {
                "include": [
                    {
                        "system": "http://snomed.info/sct",
                        "concept": []
                    }
                ]
            }
        }
        
        return create_mock_response(valueset_data)
    
    with patch('requests.Session.get', side_effect=mock_get):
        yield

