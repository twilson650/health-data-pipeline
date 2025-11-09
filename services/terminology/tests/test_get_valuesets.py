
import json
from pathlib import Path
import re
from typing import List, Dict
from terminology.vsac import VSAC
import logging
logger = logging.getLogger(__name__)

def read_cql_file(filename: str) -> str:
    """Read a CQL file from the resources directory."""
    resources_dir = Path(__file__).parent / "resources" / "value_sets"
    cql_file = resources_dir / filename
    
    with cql_file.open('r', encoding='utf-8') as f:
        return f.read()

def parse_valuesets_with_cql_parser(cql_content: str) -> List[Dict[str, str]]:
    """Parse valuesets using the cqlpy library."""
    logger.error("cqlpy is not supported yet")
    return None


def parse_valuesets_with_regex(cql_content: str) -> List[Dict[str, str]]:
    """Parse valueset definitions from CQL content using regex."""
    # Pattern to match valueset definitions
    pattern = r'valueset\s+"([^"]+)"\s*:\s*[\'"]?([^\s\'\"]+)[\'"]?(?:\s+version\s+[\'"]?([^\s\'\"]+)[\'"]?)?'
    matches = re.findall(pattern, cql_content)
    
    valuesets = []
    for name, oid, version in matches:
        valueset = {"name": name, "oid": oid}
        if version:
            valueset["version"] = version
        valuesets.append(valueset)
    
    return valuesets

def parse_valuesets(cql_content: str) -> List[Dict[str, str]]:
    """Parse valuesets using the best available method."""
    # Try cql-parser first
    valuesets = parse_valuesets_with_cql_parser(cql_content)
    
    # Fall back to regex if cql-parser fails
    if valuesets is None:
        print("Falling back to regex parsing...")
        valuesets = parse_valuesets_with_regex(cql_content)
    
    return valuesets

# Test the parsing
cql_content = read_cql_file("valueset_list.cql")
valuesets = parse_valuesets(cql_content)

print(f"Found {len(valuesets)} valuesets:")

vsac_client = VSAC()

for vs in valuesets[:5]:  # Show first 5
    
    print(f"Name: {vs['name']}, OID: {vs['oid']}")
    #print(json.dumps(vs, indent=2))
    vsac_valueset = vsac_client.get_valueset_by_oid(vs['oid'])
    print(vsac_valueset.model_dump_json(indent=2))
   # print(json.dumps(vsac_valueset, indent=2))




