from google.adk.a2a.agent import RemoteA2aAgent
from google.adk.agents import Agent

# The calculator is a separate service (serve_code_agent.py on port 8001).
# This agent only knows its address; it reads the rest from the agent card.
calculator = RemoteA2aAgent(
    name="calculator",
    description="Remote agent that does exact calculations by running Python code.",
    agent_card="http://localhost:8001/.well-known/agent-card.json",
)

root_agent = Agent(
    name="trip_planner",
    model="gemini-3.5-flash",
    description="Helps plan trips in Switzerland.",
    instruction="""
    You help plan trips in Switzerland. Keep answers short.
    For any calculation (costs, budgets, distances, times, currency), hand over to the calculator agent.
    """,
    sub_agents=[calculator],
)
