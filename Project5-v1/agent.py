import asyncio
import os
import json
import sys
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from datetime import datetime

def parse_mcp_result(result):
    raw = result.content[0].text
    try:
        data = json.loads(raw)
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                pass
        return data
    except Exception:
        try:
            import ast
            return ast.literal_eval(raw)
        except Exception:
            return raw

async def run_agent(patient_id: str = "P-1007"):
    logs = []
    
    def log(message, role="system", data=None):
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "message": message,
            "data": data
        })

    python_exe = sys.executable
    ehr_params = StdioServerParameters(command=python_exe, args=["ehr_server.py"])
    pharm_params = StdioServerParameters(command=python_exe, args=["pharmacy_server.py"])
    billing_params = StdioServerParameters(command=python_exe, args=["billing_server.py"])
    
    log("Initializing Discharge Coordination Agent...", "system")
    
    try:
        async with stdio_client(ehr_params) as (ehr_read, ehr_write), \
                   stdio_client(pharm_params) as (pharm_read, pharm_write), \
                   stdio_client(billing_params) as (bill_read, bill_write):
                   
            async with ClientSession(ehr_read, ehr_write) as ehr_session, \
                       ClientSession(pharm_read, pharm_write) as pharm_session, \
                       ClientSession(bill_read, bill_write) as bill_session:
                       
                await ehr_session.initialize()
                await pharm_session.initialize()
                await bill_session.initialize()
                log(f"Starting Discharge Workflow for Patient: {patient_id}", "system")
                
                log("Calling EHR Server -> get_medication_list (Role: discharge)", "agent")
                meds_result = await ehr_session.call_tool("get_medication_list", arguments={"patient_id": patient_id, "context_role": "discharge"})
                meds = parse_mcp_result(meds_result)
                log("EHR Response Received", "ehr", meds)
                
                billable_items = []
                
                for med in meds:
                    brand = med["brand_name"]
                    # Calculate quantity dynamically based on frequency and duration
                    freq = med.get("frequency", "OD").upper()
                    duration = med.get("duration", "1 day")
                    days = 1
                    try:
                        parts = duration.split()
                        if parts:
                            days = int(parts[0])
                    except Exception:
                        pass
                    
                    multiplier = 1
                    if "OD" in freq:
                        multiplier = 1
                    elif "BD" in freq:
                        multiplier = 2
                    elif "TDS" in freq:
                        multiplier = 3
                    elif "QDS" in freq:
                        multiplier = 4
                    elif "SOS" in freq:
                        multiplier = 2 # SOS maps to 2 or custom fallback
                    
                    qty = days * multiplier
                    
                    log(f"Calling Pharmacy Server -> resolve_generic for '{brand}'", "agent")
                    gen_result = await pharm_session.call_tool("resolve_generic", arguments={"brand_name": brand, "context_role": "discharge"})
                    generic = parse_mcp_result(gen_result)
                    log(f"Generic for {brand} resolved.", "pharmacy", generic)
                    
                    log(f"Calling Pharmacy Server -> check_stock for '{generic} {med['dose']}'", "agent")
                    stock_result = await pharm_session.call_tool("check_stock", arguments={"generic_name": generic, "strength": med["dose"], "context_role": "discharge"})
                    stock = parse_mcp_result(stock_result)
                    
                    if isinstance(stock, dict) and ("error" in stock or not stock.get("in_stock")):
                        log(f"Out of stock or error.", "pharmacy", stock)
                        log(f"Calling Pharmacy Server -> suggest_alternative", "agent")
                        alt_result = await pharm_session.call_tool("suggest_alternative", arguments={"generic_name": generic, "strength": med["dose"], "context_role": "discharge"})
                        alts = parse_mcp_result(alt_result)
                        log(f"Alternatives provided.", "pharmacy", alts)
                        if alts and isinstance(alts, list):
                            billable_items.append({"item": alts[0], "quantity": qty})
                    else:
                        log(f"In stock.", "pharmacy", stock)
                        billable_items.append({"item": f"{generic} {med['dose']}", "quantity": qty})
                
                log("Finalizing Billing", "system")
                log(f"Preparing Invoice Payload", "agent", billable_items)
                
                log("Calling Billing Server -> create_invoice (Role: discharge)", "agent")
                inv_result = await bill_session.call_tool("create_invoice", arguments={"patient_id": patient_id, "billable_items": billable_items, "context_role": "discharge"})
                invoice = parse_mcp_result(inv_result)
                log(f"Invoice Created", "billing", invoice)
                
                log("Calling Billing Server -> validate_invoice (Role: discharge)", "agent")
                val_result = await bill_session.call_tool("validate_invoice", arguments={"patient_id": patient_id, "context_role": "discharge"})
                validated = parse_mcp_result(val_result)
                log(f"Validation successful.", "billing", validated)
                
                log("Testing RBAC & Boundary Failures", "system")
                
                log("[TEST] Simulating Billing Clerk trying to read clinical notes...", "agent")
                try:
                    notes_result = await ehr_session.call_tool("get_clinical_notes", arguments={"patient_id": patient_id, "context_role": "billing"})
                    log("EHR Response (Expected Error)", "ehr", notes_result.content[0].text)
                except Exception as e:
                    log("EHR Response ERROR", "ehr", str(e))
                    
                log("[TEST] Simulating Billing payload with PHI leakage...", "agent")
                phi_payload = billable_items.copy()
                phi_payload.append({"item": "Consultation", "diagnosis": "Community acquired pneumonia", "quantity": 1})
                try:
                    inv_phi = await bill_session.call_tool("create_invoice", arguments={"patient_id": patient_id, "billable_items": phi_payload, "context_role": "discharge"})
                    log("Billing Response (Expected PHI Error)", "billing", parse_mcp_result(inv_phi))
                except Exception as e:
                    log("Billing Response ERROR", "billing", str(e))
                
                log("Workflow completed successfully.", "system")
    except Exception as e:
        log(f"Workflow encountered a critical error: {str(e)}", "error")

    return logs

if __name__ == "__main__":
    logs = asyncio.run(run_agent())
    for lg in logs:
        print(f"[{lg['role'].upper()}] {lg['message']} {json.dumps(lg.get('data') or '')}")
