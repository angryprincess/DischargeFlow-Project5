from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any

# Create the Billing FastMCP server
mcp = FastMCP("billing_server")

# Load synthetic Billing Data from synthetic_billing_records.json
import json
import os
import sys

BILLING_CATALOG = {}
INVOICE_DB = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "synthetic_billing_records.json")

try:
    with open(json_path, "r", encoding="utf-8") as f:
        billing_data = json.load(f)
        for item in billing_data.get("billing_catalog", []):
            name = item.get("item_name")
            if name:
                BILLING_CATALOG[name.lower()] = {
                    "code": item.get("code"),
                    "price": item.get("price")
                }
except Exception as e:
    print(f"Error loading synthetic_billing_records.json: {e}", file=sys.stderr)

@mcp.tool()
def get_billing_code(item_name: str, context_role: str = "billing") -> str:
    """Retrieves the billing code and price for a specific item. Allowed for billing and discharge roles."""
    import json
    if context_role not in ["billing", "discharge"]:
        return json.dumps({"error": "Access denied."})
    
    item_info = BILLING_CATALOG.get(item_name.lower())
    if not item_info:
        return json.dumps({"error": f"Item '{item_name}' not found in billing catalog."})
    return json.dumps(item_info)

@mcp.tool()
def create_invoice(patient_id: str, billable_items: List[Dict[str, Any]], context_role: str = "billing") -> str:
    """
    Creates an invoice.
    Warning: This tool strictly expects billable items only. 
    It will fail if unexpected PHI or clinical data is included in the payload.
    """
    import json
    if context_role not in ["billing", "discharge"]:
        return json.dumps({"error": "Access denied."})
        
    total_amount = 0.0
    validated_items = []
    
    for item in billable_items:
        # Prevent clinical notes from being submitted
        if "diagnosis" in str(item).lower() or "clinical" in str(item).lower():
            return json.dumps({"error": "PHI LEAKAGE DETECTED: Clinical data found in billing payload. Request rejected."})
            
        name = item.get("item", "").lower()
        qty = item.get("quantity", 1)
        
        catalog_info = BILLING_CATALOG.get(name)
        if catalog_info:
            line_total = catalog_info["price"] * qty
            total_amount += line_total
            validated_items.append({
                "item": name,
                "code": catalog_info["code"],
                "quantity": qty,
                "unit_price": catalog_info["price"],
                "total": line_total
            })
        else:
            return json.dumps({"error": f"Item '{name}' not found in billing catalog."})
            
    invoice = {
        "patient_id": patient_id,
        "items": validated_items,
        "total_amount": total_amount,
        "status": "created"
    }
    INVOICE_DB[patient_id] = invoice
    return json.dumps(invoice)

@mcp.tool()
def validate_invoice(patient_id: str, context_role: str = "billing") -> str:
    """Validates if an invoice exists and returns its summary."""
    import json
    if context_role not in ["billing", "discharge"]:
        return json.dumps({"error": "Access denied."})
        
    invoice = INVOICE_DB.get(patient_id)
    if not invoice:
        return json.dumps({"error": "Invoice not found."})
    
    invoice["status"] = "validated"
    return json.dumps(invoice)

if __name__ == "__main__":
    mcp.run()
