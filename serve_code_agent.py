"""Runs code_agent as a standalone A2A service on http://localhost:8001.

Start it from the repository root with:
    uvicorn serve_code_agent:app --port 8001
"""

from dotenv import load_dotenv

load_dotenv("code_agent/.env")

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from code_agent.agent import root_agent

# Wraps the agent in an A2A server and publishes its agent card at
# http://localhost:8001/.well-known/agent-card.json
app = to_a2a(root_agent, port=8001)
