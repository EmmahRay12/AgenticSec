# AgenticSec
**Capability-Preserving AI Agent Governance System**

AgenticSec is a lightweight, deterministic governance layer that sits between autonomous AI agents and the actions they propose. Before any action is executed, it checks the agent's operating contract, assesses context and impact, and returns a decision: **ALLOW**, **HUMAN REVIEW**, or **BLOCK**.

## 🚀 Live Demo
👉 **[Click here to view the Live Dashboard](https://agentic-linmbztrq-emmahray12.vercel.app)**
*(Note: This is deployed on Vercel's serverless free tier. If it takes a few seconds to load the first time, please wait.)*

## 🎥 Demo Video
👉 **[Watch the 1-minute Demo Video](YOUR_YOUTUBE_LINK_HERE)**
*(Aap video banane ke baad yahan YouTube ka link daal dena)*

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS, Vanilla JavaScript (Custom Dark Dashboard UI)
- **Backend:** Python, FastAPI
- **Deployment:** Vercel (Serverless Architecture)
- **Storage:** In-memory audit logging (Simulated for serverless environment)

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

## ⚠️ Limitations
This is a hackathon educational prototype. It evaluates observable actions and does not read an agent's internal intentions. It is not a production security system.