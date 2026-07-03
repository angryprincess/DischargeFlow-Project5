from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional

# Create the Pharmacy FastMCP server
mcp = FastMCP("pharmacy_server")

# Load synthetic Pharmacy Data from synthetic_pharmacy_records.json
import json
import os
import sys

BRAND_TO_GENERIC = {}
PHARMACY_INVENTORY = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "synthetic_pharmacy_records.json")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        pharm_data = json.load(f)
        for mapping in pharm_data.get("brand_to_generic", []):
            brand = mapping.get("brand_name")
            generic = mapping.get("generic_name")
            if brand and generic:
                BRAND_TO_GENERIC[brand.lower()] = generic.lower()
                
        for item in pharm_data.get("inventory", []):
            gen_name = item.get("generic_name")
            if gen_name:
                gen_name_lower = gen_name.lower()
                if gen_name_lower not in PHARMACY_INVENTORY:
                    PHARMACY_INVENTORY[gen_name_lower] = []
                PHARMACY_INVENTORY[gen_name_lower].append({
                    "strength": item.get("strength"),
                    "stock": item.get("stock", 0),
                    "alternatives": item.get("alternatives", []),
                    "drug_class": item.get("drug_class", "")
                })
except Exception as e:
    print(f"Error loading synthetic_pharmacy_records.json: {e}", file=sys.stderr)

@mcp.tool()
def resolve_generic(brand_name: str, context_role: str = "pharmacy") -> str:
    """Converts a brand name to a generic name. Allowed for pharmacy and discharge roles."""
    if context_role not in ["pharmacy", "discharge"]:
        return "ERROR: Access denied."
    
    # Check if the name is already a known generic in inventory
    if brand_name.lower() in PHARMACY_INVENTORY:
        return brand_name.lower()
        
    generic = BRAND_TO_GENERIC.get(brand_name.lower())
    if not generic:
        return f"Unknown brand: {brand_name}"
    return generic

@mcp.tool()
def check_stock(generic_name: str, strength: str, context_role: str = "pharmacy") -> str:
    """Checks inventory stock for a generic medication and strength. Allowed for pharmacy and discharge roles."""
    import json
    if context_role not in ["pharmacy", "discharge"]:
        return json.dumps({"error": "Access denied."})
    
    items = PHARMACY_INVENTORY.get(generic_name.lower(), [])
    for item in items:
        # Simple match, could be more robust in real world
        if item["strength"].lower() == strength.lower():
            return json.dumps({
                "generic_name": generic_name,
                "strength": strength,
                "in_stock": item["stock"] > 0,
                "stock_count": item["stock"]
            })
    return json.dumps({"error": "Medication or strength not found in inventory."})

@mcp.tool()
def suggest_alternative(generic_name: str, strength: str, context_role: str = "pharmacy") -> str:
    """Suggests an alternative if the requested medication/strength is out of stock."""
    import json
    if context_role not in ["pharmacy", "discharge"]:
        return json.dumps(["ERROR: Access denied."])
    
    items = PHARMACY_INVENTORY.get(generic_name.lower(), [])
    for item in items:
        if item["strength"].lower() == strength.lower():
            return json.dumps(item.get("alternatives", []))
    return json.dumps([])

if __name__ == "__main__":
    mcp.run()
