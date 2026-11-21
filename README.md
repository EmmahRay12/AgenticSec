# AgenticSec
**Capability-Preserving AI Agent Governance System**

AgenticSec is a lightweight, deterministic governance layer that sits between autonomous AI agents and the actions they propose. Before any action is executed, it checks the agent's operating contract, assesses context and impact, and returns a decision: **ALLOW**, **HUMAN REVIEW**, or **BLOCK**.

## 🚀 Live Demo
👉 **[https://agentic-sec-445t.vercel.app](https://agentic-sec-445t.vercel.app)**

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, Vanilla JavaScript (Custom Dark Dashboard UI)
- **Backend:** Python, FastAPI
- **Deployment:** Vercel (Serverless Architecture)
- **Storage:** JSON-based local audit logging (Simulated for serverless)

## ⚙️ The 5-Stage Governance Pipeline
1. **Contract Validator:** Checks explicit permissions and restrictions (Restrictions always take priority).
2. **Context Analyzer:** Flags actions targeting highly sensitive resources (e.g., `internal_database`, `backup_server`).
3. **Impact Assessor:** Evaluates severity and reversibility (e.g., destructive actions like `delete_server`).
4. **Decision Engine:** Combines all stages to make a final, deterministic decision.
5. **Simulator + Audit:** Logs the action safely and displays it in the Audit Dashboard.

## 🧪 Demo Scenarios
You can test these in the **Action Evaluation** tab:
- `delete_server — backup_server` ➔ **BLOCK** (Protected by restriction)
- `delete_server — noncritical_server` ➔ **HUMAN REVIEW** (Destructive action, but allowed)
- `list_servers — cloud_inventory` ➔ **ALLOW** (Safe read-only action)
- `read_internal_records — internal_database` ➔ **BLOCK** (Unauthorized resource)

## 💻 Local Setup
If you want to run this project locally:
```bash
git clone https://github.com/EmmahRay12/AgenticSec.git
cd AgenticSec
python -m venv venv
# Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload