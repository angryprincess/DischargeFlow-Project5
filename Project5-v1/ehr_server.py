from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import List, Dict, Any

# Create the EHR FastMCP server
mcp = FastMCP("ehr_server")

# Load synthetic EHR Data from synthetic_records.json
import json
import os
import sys

EHR_DATA = {}
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "synthetic_records.json")
try:
    with open(json_path, "r", encoding="utf-8") as f:
        records_data = json.load(f)
        for record in records_data.get("ehr_records", []):
            p_id = record.get("patient_id")
            if p_id:
                EHR_DATA[p_id] = record
except Exception as e:
    print(f"Error loading synthetic_records.json: {e}", file=sys.stderr)

@mcp.tool()
def get_discharge_summary(patient_id: str, context_role: str = "clinical") -> str:
    """Retrieves the discharge status and diagnosis summary. Allowed for clinical and discharge roles."""
    if context_role not in ["clinical", "discharge"]:
        return "ERROR: Access denied. Role not permitted to access diagnosis."
    
    patient = EHR_DATA.get(patient_id)
    if not patient:
        return "Patient not found."
    return f"Status: {patient['discharge_status']}, Diagnosis: {patient['diagnosis_summary']}"

@mcp.tool()
def get_medication_list(patient_id: str, context_role: str = "clinical") -> str:
    """Retrieves the prescribed discharge medications. Allowed for clinical, discharge, and pharmacy roles."""
    import json
    if context_role not in ["clinical", "discharge", "pharmacy"]:
        return json.dumps([{"error": "Access denied. Role not permitted."}])
    
    patient = EHR_DATA.get(patient_id)
    if not patient:
        return json.dumps([])
    return json.dumps(patient.get("discharge_medications", []))

@mcp.tool()
def get_clinical_notes(patient_id: str, context_role: str = "clinical") -> str:
    """Retrieves the full clinical notes. Highly sensitive. Allowed for clinical role ONLY."""
    if context_role != "clinical":
        return "ERROR: Access denied. PHI Boundary Violation. Only clinical role can access clinical notes."
    
    patient = EHR_DATA.get(patient_id)
    if not patient:
        return "Patient not found."
    return patient.get("clinical_notes", "No notes available.")

if __name__ == "__main__":
    mcp.run()
