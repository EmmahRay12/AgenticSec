"""
AgenticSec — FastAPI application serving the dashboard and governance API.
"""
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Import Engine Components
from engine.contract_validator import load_contracts, validate_action
from engine.context_analyzer import analyze_context
from engine.impact_assessor import assess_impact
from engine.decision_engine import make_decision
from storage.audit_logger import log_decision, get_all_logs

BASE_DIR = Path(__file__).parent

app = FastAPI(title="AgenticSec")

class EvaluateRequest(BaseModel):
    agent_id: str
    action: str
    resource: str
    reason: str = ""


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the dashboard HTML."""
    html_path = BASE_DIR / "templates" / "index.html"
    if not html_path.exists():
        return HTMLResponse("<h1>templates/index.html not found</h1>", status_code=500)
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "contracts_loaded": len(load_contracts())}


@app.get("/api/agents")
async def get_agents():
    """Fetch list of all registered agents."""
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
    """Evaluate an action based on agent contract, context, and impact."""
    contracts = load_contracts()
    contract = contracts.get(req.agent_id)
    
    if contract is None:
        raise HTTPException(status_code=404, detail=f"Unknown agent: {req.agent_id}")

    # Stage 1: Contract Validator (Restrictions first, then Permissions)
    contract_result = validate_action(contract, req.action, req.resource)
    
    # Stage 2: Context Analyzer (Is the resource sensitive?)
    context_result = analyze_context(req.action, req.resource)
    
    # Stage 3: Impact Assessor (Is it destructive/irreversible?)
    impact_result = assess_impact(req.action, req.resource)
    
    # Stage 4: Decision Engine (Combines all 3 stages)
    final_result = make_decision(contract_result, context_result, impact_result)

    # Save to Audit Log
    log_decision(
        agent_id=req.agent_id,
        action=req.action,
        resource=req.resource,
        decision=final_result["decision"],
        explanation=final_result["explanation"]
    )

    return {
        "agent_id": req.agent_id,
        "action": req.action,
        "resource": req.resource,
        "decision": final_result["decision"],
        "explanation": final_result["explanation"],
        "stages": {
            "contract": contract_result,
            "context": context_result,
            "impact": impact_result
        },
        "source": "simulated",
    }


@app.get("/api/audit")
async def get_audit():
    """Fetch real audit logs."""
    return {"records": get_all_logs()}


@app.get("/api/approvals")
async def get_approvals():
    """Fetch pending approvals (Not implemented yet)."""
    return {"approvals": []}


@app.post("/api/approvals/action")
async def approval_action(req: dict):
    """Handle approval actions (Not implemented yet)."""
    return {"ok": True}