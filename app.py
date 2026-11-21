import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from datetime import datetime

from engine.contract_validator import load_contracts, validate_action
from engine.context_analyzer import analyze_context
from engine.impact_assessor import assess_impact
from engine.decision_engine import make_decision
from storage.audit_logger import log_decision, get_all_logs

BASE_DIR = Path(__file__).parent
app = FastAPI(title="AgenticSec")
TEMP_LOGS = []

class EvaluateRequest(BaseModel):
    agent_id: str
    action: str
    resource: str
    reason: str = ""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    html_path = os.path.join(BASE_DIR, "templates", "index.html")
    if not os.path.exists(html_path):
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)
    return FileResponse(html_path)

@app.get("/api/health")
async def health():
    return {"status": "ok", "contracts_loaded": len(load_contracts())}

@app.get("/api/agents")
async def get_agents():
    contracts = load_contracts()
    agents_list = []
    for agent_id, c in contracts.items():
        agents_list.append({
            "agent_id": agent_id,
            "agent_name": c.get("agent_name", "Unknown Agent"),
            "agent_type": c.get("agent_type", "simulated"),
            "objective": c.get("objective", ""),
            "permissions_count": len(c.get("permissions", [])),
            "restrictions_count": len(c.get("restrictions", [])),
        })
    return {"agents": agents_list}

@app.post("/api/evaluate")
async def evaluate(req: EvaluateRequest):
    contracts = load_contracts()
    contract = contracts.get(req.agent_id)
    if contract is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {req.agent_id}")

    contract_result = validate_action(contract, req.action, req.resource)
    context_result = analyze_context(req.action, req.resource)
    impact_result = assess_impact(req.action, req.resource)
    final_result = make_decision(contract_result, context_result, impact_result)

    log_decision(req.agent_id, req.action, req.resource, final_result["decision"], final_result["explanation"])
    
    TEMP_LOGS.append({
        "timestamp": datetime.now().isoformat(),
        "agent_id": req.agent_id,
        "action": req.action,
        "resource": req.resource,
        "decision": final_result["decision"],
        "explanation": final_result["explanation"]
    })

    return {
        "agent_id": req.agent_id,
        "action": req.action,
        "resource": req.resource,
        "decision": final_result["decision"],
        "explanation": final_result["explanation"],
        "source": "simulated"
    }

@app.get("/api/audit")
async def get_audit():
    if TEMP_LOGS:
        return {"records": TEMP_LOGS}
    return {"records": get_all_logs()}

@app.get("/api/approvals")
async def get_approvals():
    return {"approvals": []}