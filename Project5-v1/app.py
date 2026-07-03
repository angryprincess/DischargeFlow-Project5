from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import json
import os
import agent

app = FastAPI(title="Discharge Coordination UI")

class DischargeRequest(BaseModel):
    patient_id: Optional[str] = "P-1007"

@app.get("/api/patients")
async def get_patients():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "synthetic_records.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            records = []
            for record in data.get("ehr_records", []):
                records.append({
                    "patient_id": record.get("patient_id"),
                    "scenario": record.get("_scenario", "N/A"),
                    "test_type": record.get("_test_type", "success")
                })
            return {"patients": records}
    except Exception as e:
        return {"error": str(e), "patients": []}

@app.post("/api/discharge")
async def run_discharge(req: Optional[DischargeRequest] = None):
    patient_id = req.patient_id if req else "P-1007"
    # Execute the agent workflow and retrieve the structured logs
    logs = await agent.run_agent(patient_id)
    return {"logs": logs}

# Route to serve the demo-idea.html from parent directory
@app.get("/demo-idea.html")
async def serve_demo_idea():
    # Relative path from Project5-v1 to parent directory where demo-idea.html is located
    return FileResponse("../demo-idea.html")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
