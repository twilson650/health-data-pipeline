import pytest
from terminology.vsac import VSAC


def test_vsac(mock_vsac_api):
    """Test retrieving valuesets from VSAC API with mocked calls."""
    vsac = VSAC()
    valuesets = vsac.get_valuesets()
    assert valuesets is not None
    assert valuesets.__class__.__name__ == "Bundle"
    assert valuesets.type == "searchset"
    assert valuesets.total == 2
    assert len(valuesets.entry) == 2
    print(valuesets)